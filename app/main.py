# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import books, authors, categories, users, recommendations
from .database import engine, Base

# Import all models to ensure they're registered with Base
from .models.book import Book
from .models.author import Author
from .models.category import Category
from .models.user import User

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Catalog API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(authors.router)
app.include_router(categories.router)
app.include_router(books.router)
app.include_router(recommendations.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Book Catalog API"}