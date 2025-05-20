from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import pytest
from ..database import Base, get_db
from ..main import app
from ..models.book import Book
from ..models.author import Author
from ..models.category import Category
from ..models.user import User
from ..services.auth import get_password_hash

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def test_db():
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    
    # Create test data
    db = TestingSessionLocal()
    
    # Create a test user
    hashed_password = get_password_hash("testpassword")
    test_user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(test_user)
    
    # Create test author
    test_author = Author(name="Test Author", bio="Test Bio")
    db.add(test_author)
    
    # Create test category
    test_category = Category(name="Test Category", description="Test Description")
    db.add(test_category)
    
    db.commit()
    
    # Create test book
    test_book = Book(
        title="Test Book",
        description="Test Description",
        isbn="1234567890",
        author_id=1,
        category_id=1
    )
    db.add(test_book)
    db.commit()
    
    yield db
    
    # Teardown
    db.close()
    Base.metadata.drop_all(bind=engine)

def test_create_book(test_db):
    # Login to get token
    response = client.post(
        "/users/token",
        data={"username": "testuser", "password": "testpassword"}
    )
    token = response.json()["access_token"]
    
    # Create a book
    response = client.post(
        "/books/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "New Book",
            "description": "New Description",
            "isbn": "0987654321",
            "author_id": 1,
            "category_id": 1
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Book"
    assert data["isbn"] == "0987654321"

def test_read_books(test_db):
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Test Book"