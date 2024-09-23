import random

from sqlalchemy import create_engine, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Book, Author
from data_generator import DataGenerator


class DatabaseManager:
    """
    Manages database operations such as creating tables, populating data, and querying information.

    Attributes:
        filename (str): Name of the SQLite database file.
        engine (Engine): SQLAlchemy engine to connect to the database.
        session (Session): SQLAlchemy session for database operations.
    """

    def __init__(self, filename: str):
        """
        Initialize the DatabaseManager with the database filename.

        :param filename: Name of the database file.
        """
        self.filename = filename
        self.engine = create_engine(f'sqlite:///{self.filename}')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_tables(self):
        """ Create all tables in the database based on the ORM models. """
        try:
            Base.metadata.create_all(self.engine)
        except SQLAlchemyError as error:
            print(f'Error creating tables: {error}')
            raise

    def populate_database(self, number_of_authors: int, number_of_books: int):
        """
        Populate the database with random authors and books.

        :param number_of_authors: Number of authors to generate.
        :param number_of_books: Number of books to generate.
        :return:
        """
        generator = DataGenerator(number_of_authors, number_of_books)
        authors = generator.generate_authors()
        books = generator.generate_books()

        for book in books:
            num_authors = random.randint(1, min(3, len(authors)))
            book_authors = random.sample(authors, num_authors)
            book.authors.extend(book_authors)

        try:
            self.session.add_all(authors + books)
            self.session.commit()
        except SQLAlchemyError as error:
            print(f'Error populating database: {error}')
            raise

    def get_book_with_most_pages(self):
        """ Retrieve and print the book(s) with the most pages. """
        try:
            subquery = self.session.query(func.max(Book.number_of_pages)).scalar_subquery()
            books_with_most_pages = self.session.query(Book).filter(Book.number_of_pages == subquery).all()

            print(f'Book(s) with most pages:')
            for book in books_with_most_pages:
                author_names = ', '.join([f'{author.name} {author.lastname}' for author in book.authors])
                print(f'\t - "{book.title}" by {author_names} (genre: {book.genre}) '
                      f'with {book.number_of_pages} pages, '
                      f'published on {book.publish_date}.')
        except SQLAlchemyError as error:
            print(f'Error retrieving book with most pages: {error}')
            raise

    def get_average_number_of_pages(self):
        """ Calculate and print the average number of pages of all books. """
        try:
            average_number_of_pages = self.session.query(func.avg(Book.number_of_pages)).scalar()
            if average_number_of_pages:
                print(f'\nThe average number of pages of all the books is {average_number_of_pages:.2f}.')
            else:
                print('\nNo books found in the database.')
        except SQLAlchemyError as error:
            print(f'Error calculating average number of pages of all the books: {error}')
            raise

    def get_youngest_author(self):
        """ Retrieve and print the youngest author(s). """
        try:
            youngest_birthdate = self.session.query(func.max(Author.date_of_birth)).scalar()
            youngest_authors = self.session.query(Author).filter(Author.date_of_birth == youngest_birthdate).all()

            print('\nThe youngest author(s) is/are:')
            for author in youngest_authors:
                print(f'\t - {author.name} {author.lastname}, born on {author.date_of_birth}.')
        except SQLAlchemyError as error:
            print(f'Error retrieving youngest author: {error}')
            raise

    def get_authors_without_books(self):
        """ Retrieve and print authors who have not published any books. """
        try:
            authors_without_books = self.session.query(Author).filter(~Author.books.any()).all()
            print('\nAuthor(s) who have not published any books:')

            if authors_without_books:
                for author in authors_without_books:
                    print(f'\t - {author.name} {author.lastname}')
            else:
                print('\nAll authors have already published books.')
        except SQLAlchemyError as error:
            print(f'Error retrieving authors without books: {error}')
            raise

    def get_authors_with_more_than_three_books(self):
        """ Retrieve and print up to 5 authors who have published more than three books. """
        try:
            authors_with_more_than_three_books = (
                self.session.query(Author, func.count(Book.id).label('book_count'))
                .join(Author.books)
                .group_by(Author.id)
                .having(func.count(Book.id) > 3)
                .limit(5)
                .all()
            )

            print('\nAuthor(s) who have published more than three books:')
            if authors_with_more_than_three_books:
                for author, book_count in authors_with_more_than_three_books:
                    print(f'\t - {author.name} {author.lastname} has published {book_count} books.')
            else:
                print('No authors have published more than three books.')
        except SQLAlchemyError as error:
            print(f'Error retrieving authors with more than three books: {error}')
            raise