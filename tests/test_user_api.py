import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from database.database import get_db
from database.models import Base, User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

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


def test_create_user(client_with_db, session):
    user_data = {"username": "testuser", "password": "testpassword"}
    response = client_with_db.post("/user/create_user", json=user_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["username"] == user_data["username"]
    db_user = session.query(User).filter(User.username == user_data["username"]).first()
    assert db_user is not None
    assert db_user.username == user_data["username"]
