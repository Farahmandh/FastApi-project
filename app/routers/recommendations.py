from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..database import get_db
from ..schemas.book import Book as BookSchema
from ..services.auth import get_current_active_user
from ..services.recommendation import get_book_recommendations

router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=List[BookSchema])
def get_recommendations(
    preferences: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Get book recommendations based on user preferences.
    
    Example request body:
    ```
    {
        "preferred_categories": [1, 3, 5],
        "preferred_authors": [2, 7],
        "min_rating": 4.0
    }
    ```
    """
    recommended_books = get_book_recommendations(db, preferences)
    return recommended_books