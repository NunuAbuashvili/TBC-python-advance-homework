import random
from faker import Faker
from database_setup import Book, Author


class DataGenerator:
    """
    Generates random authors and books using the Faker library.

    Attributes:
        number_of_authors (int): Number of authors to generate.
        number_of_books (int): Number of books to generate.
    """

    def __init__(self, number_of_authors: int, number_of_books: int):
        """
        Initialize the DataGenerator with the number of authors and books to generate.

        :param number_of_authors: Number of authors to generate.
        :param number_of_books: Number of books to generate.
        """
        self.faker = Faker()
        self.number_of_authors = number_of_authors
        self.number_of_books = number_of_books

    def generate_authors(self) -> list[Author]:
        """
        Generate a list of random authors.

        :return: List of generated Author instances.
        """
        authors = []
        for _ in range(self.number_of_authors):
            author = Author(
                name = self.faker.first_name(),
                lastname = self.faker.last_name(),
                date_of_birth = self.faker.date_of_birth(minimum_age=20, maximum_age=100),
                place_of_birth = f'{self.faker.city()}, {self.faker.country()}'
            )
            authors.append(author)
        return authors

    def generate_books(self) -> list[Book]:
        """
        Generate a list of random books.

        :return: List of generated Book instances.
        """
        genres = [
            'Fiction', 'Non-Fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Thriller', 'Romance',
            'Historical Fiction', 'Biography', 'Autobiography', 'Self-Help', 'Philosophy', 'Poetry',
            'Drama', 'Horror', 'Young Adult', 'Dystopian', 'Adventure', 'Crime', 'Graphic Novel'
        ]
        books = []
        for _ in range(self.number_of_books):
            title_length = random.randint(1, 5)
            book = Book(
                title = self.faker.sentence(nb_words=title_length).rstrip('.').title(),
                genre = self.faker.random_element(genres),
                number_of_pages = self.faker.random_int(30, 1000),
                publish_date = self.faker.date_between(start_date='-80y', end_date='today')
            )
            books.append(book)
        return books