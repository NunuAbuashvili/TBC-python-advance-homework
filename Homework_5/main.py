from database_manager import DatabaseManager
from data_generator import DataGenerator


def main():
    """
    Main function to run the program.

    This function performs the following steps:
    1. Creates a new SQLite database.
    2. Generates random data for authors and books.
    3. Inserts the generated data into the database.
    4. Performs various queries on the database to analyze the data.
    """
    # Define the database filename
    filename = 'books_and_authors.db'

    # Use a context manager to handle the database connection
    with DatabaseManager(filename) as database:
        # Create the database schema (tables)
        database.create_sqlite_database()

        # Set the number of authors and books to generate
        number_of_authors = 500
        number_of_books = 1000

        # Create a DataGenerator instance
        data_generator = DataGenerator(number_of_authors, number_of_books)

        # Generate random data for authors and books
        authors = data_generator.generate_authors()
        books = data_generator.generate_books()

        # Insert the generated data into the database
        database.add_authors_to_database(authors)
        database.add_books_to_database(books)

        # Perform various queries on the database
        database.get_book_with_most_pages()
        database.get_average_number_of_pages()
        database.get_youngest_author()
        database.get_authors_without_books()
        database.get_authors_with_more_than_three_books()


if __name__ == '__main__':
    main()
