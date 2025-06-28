
import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the Enhanced Event Scheduler API!" in response.data

def test_create_event(client):
    event_data = {
        "title": "Test Meeting",
        "description": "Test description",
        "start_time": "2025-07-01T09:00:00",
        "end_time": "2025-07-01T10:00:00"
    }
    response = client.post("/events", json=event_data)
    assert response.status_code == 201
    assert "event" in response.get_json()
