from database_manager import DatabaseManager


def main():
    """ Main function to run the database operations. """
    filename = 'books_and_authors.db'
    number_of_books = 1000
    number_of_authors = 500

    database = DatabaseManager(filename)
    database.create_tables()
    database.populate_database(number_of_authors, number_of_books)

    database.get_book_with_most_pages()
    database.get_average_number_of_pages()
    database.get_youngest_author()
    database.get_authors_without_books()
    database.get_authors_with_more_than_three_books()


if __name__ == '__main__':
    main()