import tkinter as tk
from tkinter import ttk, messagebox
from pymongo import MongoClient
from bson import ObjectId

uri = "mongodb+srv://junaidhashmi71:RT6Tn1aYqMVB5hxh@database1.fxqwhim.mongodb.net/?retryWrites=true&w=majority&appName=DataBase1"


class MovieApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Movie Search App")

        # MongoDB connection
        self.client = MongoClient(uri)
        self.db = self.client['Movies']
        self.movies_collection = self.db['movies_data']

        self.center_window(self.master)
        self.setup_styles()
        self.create_widgets()
        self.configure_styles()

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('SkyBlue.TLabel', background='sky blue', foreground='black')
        self.style.configure('SkyBlue.TFrame', background='sky blue')

    def center_window(self, window):
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        window_width = 900  # Set your desired window width
        window_height = 700  # Set your desired window height

        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        window.geometry(f'{window_width}x{window_height}+{x}+{y}')

    def create_widgets(self):
        # Create a frame to contain the search bar components
        self.search_frame = ttk.Frame(self.master, name="search_frame")
        self.search_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.search_frame.grid_propagate(False)  # Prevent the frame from resizing automatically
        self.search_frame.config(width=850, height=200)      

        # Search bar with label
        self.search_label = ttk.Label(self.search_frame, text="Movie Name:")
        self.search_label.grid(row=0, column=0, padx=10, pady=10)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)  

        # Actor search
        self.actor_label = ttk.Label(self.search_frame, text="Actor:")
        self.actor_label.grid(row=1, column=0, padx=10, pady=10)
        self.actor_var = tk.StringVar()
        self.add_actor_var = tk.StringVar()
        self.update_actor_var = tk.StringVar()
        self.actor_entry = ttk.Entry(self.search_frame, textvariable=self.actor_var)
        self.actor_entry = ttk.Entry(self.search_frame, textvariable=self.add_actor_var)
        self.actor_entry = ttk.Entry(self.search_frame, textvariable=self.update_actor_var)
        self.actor_entry.grid(row=1, column=1, padx=10, pady=10)

        # Director search
        self.director_label = ttk.Label(self.search_frame, text="Director:")
        self.director_label.grid(row=2, column=0, padx=10, pady=10)
        self.director_var = tk.StringVar()
        self.add_director_var = tk.StringVar()
        self.update_director_var = tk.StringVar()
        self.director_entry = ttk.Entry(self.search_frame, textvariable=self.director_var)
        self.director_entry = ttk.Entry(self.search_frame, textvariable=self.add_director_var)
        self.director_entry = ttk.Entry(self.search_frame, textvariable=self.update_director_var)
        self.director_entry.grid(row=2, column=1, padx=10, pady=10)

        # Sort order frame containing radio buttons
        self.sort_order_frame = ttk.Frame(self.search_frame, name="order_by_frame")
        self.sort_order_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky=tk.E)

        self.sort_var = tk.StringVar()
        self.sort_var.set("by movie name")  # Default selection

        self.movie_name_radio = ttk.Radiobutton(self.sort_order_frame, text="By Movie Name", variable=self.sort_var, value="by movie name")
        self.movie_name_radio.grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)

        self.year_radio = ttk.Radiobutton(self.sort_order_frame, text="By Year", variable=self.sort_var, value="by year")
        self.year_radio.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)

        # Buttons row
        self.buttons_frame = ttk.Frame(self.search_frame)
        self.buttons_frame.grid(row=1, column=3, columnspan=2, padx=200, pady=10, sticky=tk.E)

        self.search_button = ttk.Button(self.buttons_frame, text="Search", command=self.search_movies)
        self.search_button.grid(row=0, column=0, padx=10, pady=10)

        self.clear_button = ttk.Button(self.buttons_frame, text="Clear", command=self.clear_search)
        self.clear_button.grid(row=0, column=1, padx=10, pady=10)  
        
        self.clear_button = ttk.Button(self.buttons_frame, text="Add", command=self.add_movie)
        self.clear_button.grid(row=0, column=2, padx=10, pady=10)         

        # Results treeview
        self.tree = ttk.Treeview(self.master, columns=("Title", "IMDB Rating", "Tomatoes Rating", "Directors"), selectmode="browse")
        self.tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Set the column headings
        self.tree.heading("#0", text="Year")
        self.tree.heading("Title", text="Title")
        self.tree.heading("IMDB Rating", text="IMDB Rating")
        self.tree.heading("Tomatoes Rating", text="Tomatoes Rating")
        self.tree.heading("Directors", text="Directors")

        # Set the initial width for each column
        self.tree.column("#0", width=80)
        self.tree.column("Title", width=290)
        self.tree.column("IMDB Rating", width=80)
        self.tree.column("Tomatoes Rating", width=105)
        self.tree.column("Directors", width=300)

        # Poster display
        self.plot_frame = ttk.Frame(self.master, name="plot_frame")
        self.plot_frame.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="w")
        self.plot_frame.config(width=850, height=325)
        self.plot_frame.grid_propagate(False)
        self.plot_frame.configure(style='SkyBlue.TFrame')

        self.plot_text = tk.Text(self.plot_frame, wrap="word", height=18, width=82)
        self.plot_text.config(state="disabled")
        self.plot_text.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="w")
        
        self.poster_label = ttk.Label(self.plot_frame, image=None)
        self.poster_label.image = None
        self.poster_label.grid(row=0, column=4, columnspan=4, padx=10, pady=10)

        # Add buttons row
        self.buttons_frame = ttk.Frame(self.search_frame)
        self.buttons_frame.grid(row=1, column=3, columnspan=2, padx=200, pady=10, sticky=tk.E)

        self.search_button = ttk.Button(self.buttons_frame, text="Search", command=self.search_movies)
        self.search_button.grid(row=0, column=0, padx=10, pady=10)

        self.clear_button = ttk.Button(self.buttons_frame, text="Clear", command=self.clear_search)
        self.clear_button.grid(row=0, column=1, padx=10, pady=10)  

        self.add_button = ttk.Button(self.buttons_frame, text="Add", command=self.add_movie)
        self.add_button.grid(row=0, column=2, padx=10, pady=10)

        # Add update and delete buttons
        self.update_button = ttk.Button(self.buttons_frame, text="Update", command=self.update_selected_movie)
        self.update_button.grid(row=0, column=3, padx=10, pady=10)

        self.delete_button = ttk.Button(self.buttons_frame, text="Delete", command=self.delete_selected_movie)
        self.delete_button.grid(row=1, column=0, padx=10, pady=10)  


    def configure_styles(self):
        self.search_label.configure(style='SkyBlue.TLabel')
        self.actor_label.configure(style='SkyBlue.TLabel')
        self.director_label.configure(style='SkyBlue.TLabel')
        self.search_frame.configure(style='SkyBlue.TFrame')


    def clear_search(self):
        # Clear the Treeview
        self.tree.delete(*self.tree.get_children())
        self.clear_movie_details()
        self.search_var.set("")
        self.actor_var.set("")
        self.director_var.set("")


    def clear_movie_details(self):
        try:
            if hasattr(self, 'plot_frame') and isinstance(self.plot_frame, (tk.Frame, ttk.Frame)):
                self.plot_text.config(state="normal")
                self.plot_text.delete("1.0", "end")
                self.plot_text.config(state="disabled")
                self.poster_label.configure(image=None)
                self.poster_label.image = None
        except AttributeError:
            pass


    def add_movie(self):
        # Clear the Treeview
        self.tree.delete(*self.tree.get_children())

        # Prepare the search queries
        title_query = {"title": self.search_var.get()}
        actor_query = {"cast": self.add_actor_var.get()}
        director_query = {"directors": self.add_director_var.get()}

        # Combine all queries with an AND operator
        query = dict()
        if self.search_var.get():
            query.update(title_query)
        if self.add_actor_var.get():
            query.update(actor_query)
        if self.add_director_var.get():
            query.update(director_query)

        # Perform the search query if at least one condition is specified
        if query:
            # Projection to include additional fields
            movies = self.movies_collection.insert_one(query)

        else:
            # Show a message if no search criteria are provided
            messagebox.showinfo("Info", "Please provide at least one adding parameter")


    def search_movies(self):
        # Clear the Treeview
        self.tree.delete(*self.tree.get_children())

        # Prepare the search queries
        title_query = {"title": {"$regex": self.search_var.get(), "$options": "i"}}
        actor_query = {"cast": {"$regex": self.actor_var.get(), "$options": "i"}}
        director_query = {"directors": {"$regex": self.director_var.get(), "$options": "i"}}

        # Combine all queries with an AND operator
        query = dict()
        if self.search_var.get():
            query.update(title_query)
        if self.actor_var.get():
            query.update(actor_query)
        if self.director_var.get():
            query.update(director_query)

        # Perform the search query if at least one condition is specified
        if query:
            # Add sorting based on sort_var
            sort_criteria = [("title", 1)]  # Default sorting by title
            if self.sort_var.get() == "by year":
                sort_criteria = [("year", 1)]

            # Projection to include additional fields
            projection = {"_id": 1, "title": 1, "year": 1, "genres": 1, "poster": 1, "imdb.rating": 1, "tomatoes.viewer.rating": 1, "directors": 1}

            movies = self.movies_collection.find(query, projection).sort(sort_criteria)
            
            # Populate the Treeview with the search results
            for movie in movies:
                movie_id = movie.get("_id")
                year = movie.get("year", "")
                imdb_rating = movie.get("imdb", {}).get("rating", "")
                tomatoes_rating = movie.get("tomatoes", {}).get("viewer", {}).get("rating", "")
                directors = ", ".join(movie.get("directors", [])) if type(movie.get("directors")) == list() else movie.get("directors")

                self.tree.insert("", "end", text=year, values=(movie["title"], imdb_rating, tomatoes_rating, directors, movie_id))

        else:
            # Show a message if no search criteria are provided
            messagebox.showinfo("Info", "Please provide at least one search parameter")


    def update_selected_movie(self):
        """
        This function will extract the movie id of the selected item in the search result view.
        """
        selected_item = self.tree.selection()
        if selected_item:
            movie_id = self.tree.item(selected_item, "values")[-1]  # Extracting movie ID from the selected item
            self.update_movie(movie_id)
        else:
            messagebox.showinfo("Info", "Please select a movie to update.")


    def delete_selected_movie(self):
        """
        This function will extract the movie id of the selected item in the search result view.
        """
        selected_item = self.tree.selection()
        if selected_item:
            movie_id = self.tree.item(selected_item, "values")[-1]  # Extracting movie ID from the selected item
            self.delete_movie(movie_id)
            self.clear_search()  # Clear the search results after deletion
        else:
            messagebox.showinfo("Info", "Please select a movie to delete.")


    def update_movie(self, movie_id):
        """
        Update movie details in the database.
        Args:
            movie_id (str): The ObjectId of the movie document to update.
            new_data (dict): A dictionary containing the new data to update.
        """
        new_data = dict()
        title_query = {"title": self.search_var.get()}
        actor_query = {"cast": self.update_actor_var.get()}
        director_query = {"directors": self.update_director_var.get()}
        if self.search_var.get():
            new_data.update(title_query)
        if self.update_actor_var.get():
            new_data.update(actor_query)
        if self.update_director_var.get():
            new_data.update(director_query)
        # Perform the search query if at least one condition is specified
        if new_data:
            # Projection to include additional fields
            
            self.movies_collection.update_one({"_id": ObjectId(movie_id)}, {"$set": new_data})
            messagebox.showinfo("Info", "Movie details updated successfully.")


    def delete_movie(self, movie_id):
        """
        Delete a movie record from the database.
        Args:
            movie_id (str): The ObjectId of the movie document to delete.
        """
        self.movies_collection.delete_one({"_id": ObjectId(movie_id)})
        messagebox.showinfo("Info", "Movie deleted successfully.")   


def main():

    root = tk.Tk()
    app = MovieApp(root)
    root.mainloop()


if __name__ == "__main__":
    # Call the main function to start the application
    main()
