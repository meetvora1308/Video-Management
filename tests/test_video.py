import io

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from database.database import get_db
from database.models import Base
from users.auth import get_current_user

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Apply the override to the FastAPI app
app.dependency_overrides[get_db] = override_get_db


# Mock current user dependency for testing
def override_get_current_user():
    class MockUser:
        id = 1

    return MockUser()


app.dependency_overrides[get_current_user] = override_get_current_user

# Create the test client
client = TestClient(app)

# Create the database and tables
Base.metadata.create_all(bind=engine)


@pytest.fixture
def session():
    # Set up the database session for each test
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client_with_db(session):
    # Override the get_db dependency to use the session
    def get_db_override():
        yield session

    app.dependency_overrides[get_db] = get_db_override
    yield client
    app.dependency_overrides[get_db] = get_db


def test_upload_video(client_with_db):
    # Create a test video file

    data = ""
    with open("file_example_AVI_480_750kB.avi", "rb") as buffer:
        data = buffer.read()

    # Send a POST request to the /upload_video endpoint
    files = {"file": ("test_file.avi", io.BytesIO(data), "video/avi")}
    response = client_with_db.post("/video/upload_video", files=files)
    # Check the response status code and data
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["message"] == "video uploaded successfully"


def test_search_video(client_with_db):
    query_params = {"name": "test_file"}
    response = client_with_db.get("/video/search_video", params=query_params)
    assert isinstance(response.json(), list)
