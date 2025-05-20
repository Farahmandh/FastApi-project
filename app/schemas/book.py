from pydantic import BaseModel, Field
from typing import Optional, List, ForwardRef
from datetime import date

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    publication_date: Optional[date] = None
    isbn: str
    price: Optional[float] = None
    rating: Optional[float] = None
    author_id: int
    category_id: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    
    class Config:
        orm_mode = True
        from_attributes = True

# Use this for simple book representation
class BookSimple(BaseModel):
    id: int
    title: str
    isbn: str
    rating: Optional[float] = None
    
    class Config:
        orm_mode = True
        from_attributes = True

# BookDetail will be defined after AuthorSimple and CategorySimple are defined