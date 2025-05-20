from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.author import Author as AuthorModel
from ..schemas.author import Author, AuthorCreate
from ..schemas.detailed import AuthorWithBooks
from ..services.auth import get_current_active_user

router = APIRouter(
    prefix="/authors",
    tags=["authors"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=Author)
def create_author(author: AuthorCreate, db: Session = Depends(get_db), current_user = Depends(get_current_active_user)):
    db_author = AuthorModel(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

@router.get("/", response_model=List[Author])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = db.query(AuthorModel).offset(skip).limit(limit).all()
    return authors

@router.get("/{author_id}", response_model=AuthorWithBooks)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@router.put("/{author_id}", response_model=AuthorWithBooks)
def update_author(
    author_id: int, 
    author: AuthorCreate, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    for key, value in author.dict().items():
        setattr(db_author, key, value)
    
    db.commit()
    db.refresh(db_author)
    return db_author

@router.delete("/{author_id}", response_model=AuthorWithBooks)
def delete_author(
    author_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    db_author = db.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    
    db.delete(db_author)
    db.commit()
    return db_author