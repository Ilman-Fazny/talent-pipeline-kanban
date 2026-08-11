import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# Setup an isolated, in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="session")
def session_fixture():
    # Re-create database schema for each test case
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(name="client")
def client_fixture(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_candidate(client):
    payload = {
        "name": "Jane Doe",
        "stage": "Applying Period",
        "application_date": "2023-10-31",
        "overall_score": 4.0,
        "referred": True,
        "assessment_status": "Completed",
    }
    response = client.post("/candidates", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane Doe"
    assert data["stage"] == "Applying Period"
    assert data["id"] is not None


def test_read_candidates(client):
    # Seed one candidate first
    payload = {
        "name": "Alex Smith",
        "stage": "Screening",
        "application_date": "2023-10-30",
        "overall_score": None,
        "referred": False,
        "assessment_status": "Not Started",
    }
    client.post("/candidates", json=payload)

    response = client.get("/candidates")
    assert response.status_code == 200
    data = response.json()
    # Lifespan seeds 14 candidates. Since override_get_db is used, the DB is empty
    # except for what we added in this test case.
    assert len(data) == 1
    assert data[0]["name"] == "Alex Smith"


def test_read_single_candidate(client):
    payload = {
        "name": "John Miller",
        "stage": "Interview",
        "application_date": "2023-10-28",
        "overall_score": 3.0,
        "referred": False,
        "assessment_status": "Completed",
    }
    created_res = client.post("/candidates", json=payload)
    candidate_id = created_res.json()["id"]

    response = client.get(f"/candidates/{candidate_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "John Miller"


def test_update_candidate(client):
    payload = {
        "name": "Sarah Connor",
        "stage": "Test",
        "application_date": "2023-10-25",
        "overall_score": None,
        "referred": False,
        "assessment_status": "Not Started",
    }
    created_res = client.post("/candidates", json=payload)
    candidate_id = created_res.json()["id"]

    update_payload = {"overall_score": 4.5, "assessment_status": "Completed"}
    response = client.put(f"/candidates/{candidate_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["overall_score"] == 4.5
    assert data["assessment_status"] == "Completed"


def test_update_candidate_stage(client):
    payload = {
        "name": "Kyle Reese",
        "stage": "Applying Period",
        "application_date": "2023-10-25",
    }
    created_res = client.post("/candidates", json=payload)
    candidate_id = created_res.json()["id"]

    # PATCH request to update stage
    response = client.patch(f"/candidates/{candidate_id}/stage", json={"stage": "Screening"})
    assert response.status_code == 200
    assert response.json()["stage"] == "Screening"


def test_delete_candidate(client):
    payload = {
        "name": "T-800",
        "stage": "Test",
        "application_date": "2023-10-20",
    }
    created_res = client.post("/candidates", json=payload)
    candidate_id = created_res.json()["id"]

    # Delete the candidate
    del_response = client.delete(f"/candidates/{candidate_id}")
    assert del_response.status_code == 200

    # Verify candidate is gone
    get_response = client.get(f"/candidates/{candidate_id}")
    assert get_response.status_code == 404
