import sqlite3


class DatabaseManager:
    """
    A class to manage database operations for the books and authors database.

    This class handles the connection to the SQLite database, creates tables,
    adds data to the tables, and performs various queries on the data.
    """

    def __init__(self, filename):
        """
        Initialize the DatabaseManager object.

        :param filename: The name of the SQLite database file.
        """
        self.filename = filename

    def __enter__(self) -> 'DatabaseManager':
        """
        Enter the runtime context for the DatabaseManager.

        This method is called when entering a 'with' statement. It establishes
        the database connection and enables foreign key support.

        :return: DatabaseManager object.
        :raise: sqlite3.Error if there's an error connecting to the database.
        """
        try:
            self.connection = sqlite3.connect(self.filename)
            self.connection.execute("PRAGMA foreign_keys = ON")
            return self
        except sqlite3.Error as error:
            print(f'Could not connect to database: {error}')
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context for the DatabaseManager.

        This method is called when exiting a 'with' statement. It closes
        the database connection.

        :param exc_type: The exception type, if an exception was raised.
        :param exc_val: The exception value, if an exception was raised.
        :param exc_tb: The traceback, if an exception was raised.
        """
        if self.connection:
            try:
                self.connection.close()
            except sqlite3.Error as error:
                print(f'Could not close connection to database: {error}')

    def create_sqlite_database(self):
        """
        Create the authors and books tables in the SQLite database.

        This method creates two tables:
        1. authors: Stores information about authors.
        2. books: Stores information about books, with a foreign key to authors.
        """
        cursor = self.connection.cursor()
        try:
            with self.connection:
                cursor.execute("""CREATE TABLE IF NOT EXISTS authors (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               name TEXT NOT NULL,
                               lastname TEXT NOT NULL,
                               date_of_birth INTEGER NOT NULL,
                               place_of_birth TEXT
                )""")

                cursor.execute("""CREATE TABLE IF NOT EXISTS books (
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               title TEXT NOT NULL,
                               genre TEXT,
                               number_of_pages INTEGER NOT NULL,
                               publish_date INTEGER NOT NULL,
                               author_id INTEGER,
                               FOREIGN KEY(author_id) REFERENCES authors (id)
                )""")
        except sqlite3.Error as error:
            print(f'Error while creating database: {error}')
            raise

    def add_authors_to_database(self, authors: list[tuple]):
        """
        Add multiple authors to the database.

        :param authors: A list of tuples, where each tuple contains the details of an author.
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.executemany("""
                       INSERT INTO authors (name, lastname, date_of_birth, place_of_birth)
                       VALUES (?, ?, ?, ?)
                """, authors)
        except sqlite3.Error as error:
            print(f'Error while adding authors data to the database: {error}')
            raise

    def add_books_to_database(self, books: list[tuple]):
        """
        Add multiple books to the database.

        :param books: A list of tuples, where each tuple contains the details of a book.
        """
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.executemany("""
                       INSERT INTO books (title, genre, number_of_pages, publish_date, author_id)
                       VALUES (?, ?, ?, ?, ?)
                """, books)
        except sqlite3.Error as error:
            print(f'Error while adding books data to the database: {error}')
            raise

    def get_book_with_most_pages(self):
        """ Retrieve and print details of the book(s) with the maximum number of pages. """
        cursor = self.connection.cursor()
        cursor.execute("""
               SELECT title, genre, number_of_pages, publish_date, author_id 
               FROM books 
               WHERE number_of_pages = (SELECT MAX(number_of_pages) FROM books)
        """)
        books_with_most_pages = cursor.fetchall()
        print('Book(s) with most pages:')

        for book in books_with_most_pages:
            title, genre, number_of_pages, publish_date, author_id = book
            cursor.execute("SELECT name, lastname FROM authors WHERE id = ?", (author_id,))
            author_name, author_lastname = cursor.fetchone()
            print(
                f'\t - "{title}" by {author_name} {author_lastname} with {number_of_pages} pages, '
                f'published on {publish_date}.'
            )

    def get_average_number_of_pages(self):
        """ Calculate and print the average number of pages across all books. """
        cursor = self.connection.cursor()
        cursor.execute("""
             SELECT AVG(number_of_pages) 
             FROM books
        """)
        average_number_of_pages = cursor.fetchone()[0]

        if average_number_of_pages:
            print(f'\nThe average number of pages of all the books is {average_number_of_pages:.2f}.')
        else:
            print('\nNo books found in the database.')

    def get_youngest_author(self):
        """ Retrieve and print the details of the youngest author(s). """
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT name, lastname, date_of_birth
            FROM authors
            WHERE date_of_birth = (SELECT MAX(date_of_birth) FROM authors)
        """)
        youngest_authors = cursor.fetchall()
        print('\nThe youngest author(s) is/are:')

        for author in youngest_authors:
            name, lastname, date_of_birth = author
            print(f'\t - {name} {lastname}, born on {date_of_birth}.')

    def get_authors_without_books(self):
        """ Retrieve and print the names of authors who have not published any books. """
        cursor = self.connection.cursor()
        cursor.execute("""
             SELECT a.name, a.lastname FROM authors a
             LEFT JOIN books b ON a.id = b.author_id
             WHERE b.author_id IS NULL
        """)
        authors_without_books = cursor.fetchall()
        print('\nAuthor(s) who have not published any books:')

        if authors_without_books:
            for name, lastname in authors_without_books:
                print(f'\t - {name} {lastname}')
        else:
            print('\nAll authors have already published books.')

    def get_authors_with_more_than_three_books(self):
        """ Retrieve and print the names of authors who have published more than three books. """
        cursor = self.connection.cursor()
        cursor.execute("""
             SELECT a.name, a.lastname, COUNT(b.author_id) AS book_count
             FROM authors a
             JOIN books b ON a.id = b.author_id
             GROUP BY a.id
             HAVING COUNT(b.author_id) > 3
        """)
        authors_with_more_than_three_books = cursor.fetchall()
        print('\nAuthor(s) who have published more than three books:')

        if authors_with_more_than_three_books:
            for name, lastname, book_count in authors_with_more_than_three_books:
                print(f'\t - {name} {lastname} has published {book_count} books.')
        else:
            print('No authors have published more than three books.')
