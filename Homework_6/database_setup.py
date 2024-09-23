from sqlalchemy import Column, Integer, String, Date, Table, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


# Base class for all ORM models
Base = declarative_base()


# Association table for the many-to-many relationship between books and authors
book_author_association = Table(
    'book_author',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True)
)


class Book(Base):
    """
    Represents a book in the database.

    Attributes:
        id (int): Primary key for the book.
        title (str): Title of the book.
        genre (str): Genre of the book.
        number_of_pages (int): Number of pages of the book.
        publish_date (date): Date the book was published.
        authors (relationship): Relationship linking the book to its authors.
    """
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    genre = Column(String)
    number_of_pages = Column(Integer)
    publish_date = Column(Date)
    authors = relationship('Author', secondary=book_author_association, back_populates='books')


class Author(Base):
    """
    Represents an author in the database.

    Attributes:
        id (int): Primary key for the author.
        name (str): Name of the author.
        lastname (str): Last name of the author.
        date_of_birth (date): Date of birth of the author.
        place_of_birth (str): Place of birth of the author.
        books (relationship): Relationship linking the author to their books.
    """
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lastname = Column(String)
    date_of_birth = Column(Date)
    place_of_birth = Column(String)
    books = relationship('Book', secondary=book_author_association, back_populates='authors')