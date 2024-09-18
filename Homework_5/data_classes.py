class Author:
    """
    A class to represent an author.

    Attributes:
        name (str): The name of the author.
        lastname (str): The last name of the author.
        date_of_birth (str): The date of birth of the author (format: 'YYYY-MM-DD').
        place_of_birth (str): The place of birth of the author (city, country).
    """

    def __init__(self, name, lastname, date_of_birth, place_of_birth):
        """
        Initialize an Author object.

        :param name: The first name of the author.
        :param lastname: The last name of the author.
        :param date_of_birth: The date of birth of the author.
        :param place_of_birth: The place of birth of the author.
        """
        self.name = name
        self.lastname = lastname
        self.date_of_birth = date_of_birth
        self.place_of_birth = place_of_birth

    def convert_to_tuple(self) -> tuple:
        """
        Convert the Author object to a tuple.

        :return: A tuple containing the author's details.
        """
        return self.name, self.lastname, self.date_of_birth, self.place_of_birth


class Book:
    """
    A class to represent a book.

    Attributes:
        title (str): The title of the book.
        genre (str): The genre of the book.
        number_of_pages (int): The number of pages of the book.
        publish_date (str): The publication date of the book (format: 'YYYY-MM-DD').
        author_id (int): The ID of the author who wrote the book.
    """
    def __init__(self, title, genre, number_of_pages, publish_date, author_id):
        """
        Initialize a Book object.

        :param title: The title of the book.
        :param genre: The genre of the book.
        :param number_of_pages: The number of pages of the book.
        :param publish_date: The publication date of the book.
        :param author_id: The ID of the author who wrote the book.
        """
        self.title = title
        self.genre = genre
        self.number_of_pages = number_of_pages
        self.publish_date = publish_date
        self.author_id = author_id

    def convert_to_tuple(self) -> tuple:
        """
        Convert the Book object to a tuple.

        :return: A tuple containing the book's details.
        """
        return self.title, self.genre, self.number_of_pages, self.publish_date, self.author_id
