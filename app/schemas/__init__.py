# Import basic models
from .book import Book, BookCreate, BookSimple
from .author import Author, AuthorCreate, AuthorSimple
from .category import Category, CategoryCreate, CategorySimple
from .user import User, UserCreate, Token, TokenData

# Import detailed models with relationships
from .detailed import BookDetail, AuthorWithBooks, CategoryWithBooks