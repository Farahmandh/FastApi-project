from pydantic import BaseModel, Field
from typing import Optional, List, ForwardRef
from datetime import date

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    
    class Config:
        orm_mode = True
        from_attributes = True

# Simple author representation without books
class AuthorSimple(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True
        from_attributes = True