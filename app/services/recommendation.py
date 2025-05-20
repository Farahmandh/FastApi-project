from sqlalchemy.orm import Session
from ..models.book import Book
from typing import List, Dict, Any
import numpy as np

def get_book_recommendations(db: Session, user_preferences: Dict[str, Any]) -> List[Book]:
    """
    Recommends books based on user preferences using a simple scoring algorithm.
    
    Parameters:
    - db: Database session
    - user_preferences: Dictionary containing user preferences like:
        - preferred_categories: List of category IDs
        - preferred_authors: List of author IDs
        - min_rating: Minimum book rating
    
    Returns:
    - List of recommended books
    """
    # Get all books
    query = db.query(Book)
    
    # Filter by minimum rating if provided
    if user_preferences.get("min_rating"):
        query = query.filter(Book.rating >= user_preferences["min_rating"])
    
    books = query.all()
    
    # Calculate scores for each book
    scored_books = []
    preferred_categories = user_preferences.get("preferred_categories", [])
    preferred_authors = user_preferences.get("preferred_authors", [])
    
    for book in books:
        score = 0
        
        # Add points for preferred categories
        if book.category_id in preferred_categories:
            score += 2
            
        # Add points for preferred authors
        if book.author_id in preferred_authors:
            score += 3
            
        # Add points for rating (normalized to 0-1 range)
        if book.rating:
            score += book.rating / 5
        
        scored_books.append((book, score))
    
    # Sort books by score (descending)
    scored_books.sort(key=lambda x: x[1], reverse=True)
    
    # Return top 10 books
    return [book for book, _ in scored_books[:10]]