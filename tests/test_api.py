import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# Use SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_read_main():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_read_services_empty():
    response = client.get("/services/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_service():
    response = client.post(
        "/services/",
        json={
            "name": "test-service",
            "owner": "test-owner",
            "endpoint_url": "https://example.com",
            "environment": "dev",
            "check_interval_seconds": 30
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "test-service"
    assert "id" in data
