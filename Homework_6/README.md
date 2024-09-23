# SQLAlchemy Books and Authors Database Generator
This project demonstrates the use of SQLAlchemy to create and manage a database of books and authors. 
It includes functionality to create database, populate it with randomly generated data,
and perform various queries.

## Features
The project demonstrates the following features:
- **Random Data Generation**:
  - Authors: Name, last name, date of birth, and place of birth.
  - Books: Title, genre, number of pages, and publish date.
- **Database Management**:
  - Create tables in SQLite database.
  - Define models with a many-to-many relationship (Books and Authors).
  - Populate the database with randomly generated authors and books.
  - Perform advanced queries to retrieve information.
- **Queries**:
  - Find the book(s) with the most pages.
  - Calculate the average number of pages.
  - Retrieve the youngest author(s).
  - List authors without published books.
  - Retrieve up to 5 authors with more than three books.

## Requirements

- Python 3.6+
- SQLite3
- [Faker](https://pypi.org/project/Faker/) library (`pip install Faker`)
- [SQLAlchemy](https://www.sqlalchemy.org/) library (`pip install SQLAlchemy`)

## Usage
To run the project, simply execute the `main.py` script. 
This will create the database, populate it with random data, and perform various queries, 
printing the results to the console.

## Project Structure
The project consists of the following files:
- `main.py`: The main script that runs the database operations.
- `database_setup.py`: Sets up the database and ORM models (Book and Author).
- `data_generator.py`: Contains the DataGenerator class for creating random books and authors.
- `database_manager.py`: Implements the DatabaseManager class for database operations.
- `requirements.txt`: Lists the project dependencies.
- `README.md`: Project description.
- `books_and_authors.db`: The SQLite database file generated and used by the application.
