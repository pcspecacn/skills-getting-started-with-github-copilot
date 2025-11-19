import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_unregister():
    # Use a test activity and email
    activity_name = next(iter(client.get("/activities").json().keys()))
    email = "testuser@example.com"

    # Sign up
    signup_resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_resp.status_code == 200
    assert "Signed up" in signup_resp.json().get("message", "")

    # Unregister
    unregister_resp = client.post(f"/activities/{activity_name}/unregister?email={email}")
    assert unregister_resp.status_code == 200
    assert "Unregistered" in unregister_resp.json().get("message", "")

def test_signup_duplicate():
    activity_name = next(iter(client.get("/activities").json().keys()))
    email = "duplicate@example.com"
    # First signup
    client.post(f"/activities/{activity_name}/signup?email={email}")
    # Duplicate signup
    resp = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert resp.status_code == 400 or resp.status_code == 409
    # Cleanup
    client.post(f"/activities/{activity_name}/unregister?email={email}")
