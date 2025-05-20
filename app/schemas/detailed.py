from pydantic import BaseModel
from typing import List, Optional
from datetime import date

from .book import Book, BookSimple
from .author import Author, AuthorSimple
from .category import Category, CategorySimple

class BookDetail(Book):
    author: AuthorSimple
    category: CategorySimple
    
    class Config:
        orm_mode = True
        from_attributes = True

class AuthorWithBooks(Author):
    books: List[BookSimple] = []
    
    class Config:
        orm_mode = True
        from_attributes = True

class CategoryWithBooks(Category):
    books: List[BookSimple] = []
    
    class Config:
        orm_mode = True
        from_attributes = True