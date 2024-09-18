import random
from faker import Faker
from data_classes import Author, Book


class DataGenerator:
    """
    A class to generate random data for authors and books.

    This class uses the Faker library to create random data for populating
    the authors and books tables in the database.
    """

    def __init__(self, number_of_authors: int, number_of_books: int):
        """
        Initialize the DataGenerator instance.

        :param number_of_authors: The number of authors to generate.
        :param number_of_books: The number of books to generate.
        """
        self.faker = Faker()
        self.number_of_authors = number_of_authors
        self.number_of_books = number_of_books

    def generate_authors(self) -> list[tuple]:
        """
        Generate a list of random authors.

        :return: A list of tuples, where each tuple contains the details of an author.
        """
        authors = []
        for _ in range(self.number_of_authors):
            author = Author(
                name = self.faker.first_name(),
                lastname = self.faker.last_name(),
                date_of_birth = self.faker.date_of_birth(minimum_age=20, maximum_age=100).strftime("%Y-%m-%d"),
                place_of_birth = f'{self.faker.city()}, {self.faker.country()}'
            )
            authors.append(author.convert_to_tuple())
        return authors

    def generate_books(self) -> list[tuple]:
        """
        Generate a list of random books.

        :return: A list of tuples, where each tuple contains the details of a book.
        """
        genres = [
            'Fiction', 'Non-Fiction', 'Science Fiction', 'Fantasy', 'Mystery', 'Thriller', 'Romance',
            'Historical Fiction', 'Biography', 'Autobiography', 'Self-Help', 'Philosophy', 'Poetry',
            'Drama', 'Horror', 'Young Adult', 'Dystopian', 'Adventure', 'Crime', 'Graphic Novel'
        ]
        title_length = random.randint(1, 5)
        books = []
        for _ in range(self.number_of_books):
            book = Book(
                title = self.faker.sentence(nb_words=title_length).rstrip('.'),
                genre = self.faker.random_element(genres),
                number_of_pages = self.faker.random_int(30, 1000),
                publish_date = self.faker.date_between(start_date='-80y', end_date='today').strftime("%Y-%m-%d"),
                author_id = self.faker.random_int(1, self.number_of_authors),
            )
            books.append(book.convert_to_tuple())
        return books
