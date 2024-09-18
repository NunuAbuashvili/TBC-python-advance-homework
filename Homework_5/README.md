# SQLite Books and Authors Database Generator

This project generates a SQLite database of books and authors, populates it with random data, and performs
various queries on the data.

## Features

- **Database Creation**: Creates a SQLite database with `authors` and `books` tables.
- **Data Generation**: Uses the `Faker` library to generate random data for authors and books.
- **Data Insertion**: Inserts generated data into the database.
- **Data Queries**: Retrieves and displays:
  - The book(s) with the most pages.
  - The average number of pages of all books.
  - The youngest author(s).
  - Authors who have not published any books.
  - Authors who have published more than three books.

## Requirements

- Python 3.6+
- SQLite3
- Faker library

## Usage

**Run the `main.py` script**:

    ```bash
    python main.py
    ```

This will create a SQLite database file named `books_and_authors.db`, 
generate random authors and books, insert them into the database, and print the results of the queries.

## File Structure

- **`database_manager.py`**: Contains the `DatabaseManager` class for managing database operations.
- **`data_generator.py`**: Contains the `DataGenerator` class for generating random authors and books.
- **`models.py`**: Defines the `Author` and `Book` classes used for data representation.
- **`main.py`**: The entry point for the application. Initializes the database, generates data, and performs queries.
- **`requirements.txt`**: Contains a list of packages or libraries needed to work on the project.
- **`README.md`**: Project description.
- **`books_and_authors.db`**: The SQLite database file generated and used by the application.

## Future Improvements

Currently, this project uses the `Faker` library to randomly generate information about authors and books. 
I plan to enhance the project by integrating real-world data sources. For example:

- **Open Library API**: Incorporate data from the [Open Library API](https://openlibrary.org/developers/api) to fetch real book and author details.
- **Google Books API**: Use the [Google Books API](https://developers.google.com/books) to retrieve comprehensive book data, including titles, authors, and publication details.




