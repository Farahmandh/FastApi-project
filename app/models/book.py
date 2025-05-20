from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    publication_date = Column(Date, nullable=True)
    isbn = Column(String, unique=True, index=True)
    price = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    
    author_id = Column(Integer, ForeignKey("authors.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    author = relationship("Author", back_populates="books")
    category = relationship("Category", back_populates="books")