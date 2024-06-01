# Unotech Python Interview Challenge: Movie Database Application

## Objective
Create a simple movie database application using Python and MongoDB. The application should allow users to perform the following operations:
1. Add a new movie to the database.
2. Retrieve a list of all movies.
3. Update the details of an existing movie.
4. Delete a movie from the database.
5. Retrieve movies based on certain criteria (e.g., genre, release year, rating).

## Requirements

### Environment Setup
- Use Python (preferably 3.9+).
- Use MongoDB (you can use MongoDB Atlas - free tier [Does not require credit card]).
- Use `pymongo` library to interact with MongoDB.

### Movie Schema
Each movie document should have the following fields:
- `title` (string)
- `director` (string)
- `release_year` (integer)
- `genre` (string)
- `rating` (float)

### Functional Requirements
- **Add Movie**: Implement a function `add_movie(movie)` that takes a movie dictionary as input and adds it to the MongoDB collection.
- **Retrieve Movies**: Implement a function `get_all_movies()` that returns a list of all movies in the database.
- **Update Movie**: Implement a function `update_movie(title, update_fields)` that updates the details of the movie with the given title. `update_fields` is a dictionary with the fields to be updated.
- **Delete Movie**: Implement a function `delete_movie(title)` that deletes the movie with the given title from the database.
- **Query Movies**: Implement a function `find_movies_by_criteria(criteria)` that takes a dictionary of criteria (e.g., `{'genre': 'Action'}`) and returns a list of movies matching the criteria.

### Good-to-have Requirements (Brownie Points)
- Add checks to ensure that movie title are not duplicated if they are from the same release_year.
- Retrieve movies function should allow for full-text search.
- Provide a Web-based UI

## Instructions for Submission
- Fork this repository.
- Add your code to this fork.
- Provide a RUNME.md file to show how to run your code and test your submission. Include an updated requirements.txt file.
- Provide a SUBMISSION.md file to show the input and output to your functions.

## Evaluation Criteria
- Correctness and completeness of the implementation.
- Code readability and organization.
- Proper use of MongoDB and pymongo.
- Demonstrated ability to learn and apply new technology (MongoDB) effectively.
- Brownie points for completing tasks under the `Good to have requirements` tag.
