import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_for_activity():
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.delete(f"/activities/{activity}/participants/{email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    # Should now be present
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400

def test_remove_participant():
    email = "removeme@mergington.edu"
    activity = "Chess Club"
    # Add participant
    client.post(f"/activities/{activity}/signup?email={email}")
    # Remove participant
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 204
    # Should not be present
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]

    # Removing again should fail
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 404
