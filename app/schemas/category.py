from pydantic import BaseModel, Field
from typing import Optional, List, ForwardRef
from datetime import date

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    
    class Config:
        orm_mode = True
        from_attributes = True

# Simple category representation without books
class CategorySimple(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True
        from_attributes = True

class CategoryWithBooks(BaseModel):
    books: List["Book"] = []
    
    class Config:
        orm_mode = True