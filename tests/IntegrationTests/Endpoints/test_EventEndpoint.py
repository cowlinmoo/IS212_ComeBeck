import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.schemas.EventSchema import EventSchema

client = TestClient(app)

# Helper function to get the bearer token
def get_bearer_token():
    form_data = {
        "username": "colinmok1000@gmail.com",
        "password": "password123"
    }
    response = client.post("http://localhost:8080/api/authenticate", data=form_data)
    assert response.status_code == 200
    return f"Bearer {response.json()['access_token']}"

# Test to get all events
@pytest.mark.integration
def test_get_all_events():
    token = get_bearer_token()
    headers = {"Authorization": token}

    response = client.get("/api/event", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()

    # Verify the response is a list
    assert isinstance(data, list), "Expected response to be a list"

    # If there are events in the list, check for known fields in each event
    if data:
        event_sample = data[0]
        assert "event_id" in event_sample, "Field 'event_id' is missing in event data"
        assert "requested_date" in event_sample, "Field 'requested_date' is missing in event data"
        assert "application_hour" in event_sample, "Field 'application_hour' is missing in event data"
        assert "location" in event_sample, "Field 'location' is missing in event data"
        assert "application_id" in event_sample, "Field 'application_id' is missing in event data"

# Test to get a specific event by event_id
@pytest.mark.integration
def test_get_event_by_event_id():
    token = get_bearer_token()
    headers = {"Authorization": token}

    # Using a sample event_id, adjust based on the database content
    sample_event_id = 1  # This should be an existing event ID in the test database
    response = client.get(f"/api/event/{sample_event_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()

    # Verify the returned data structure matches the expected fields
    assert data["event_id"] == sample_event_id
    assert "requested_date" in data
    assert "application_hour" in data
    assert "location" in data
    assert "application_id" in data

    # Optional: Add any further checks if the expected values are known
    # e.g., assert data["location"] == "Home"


# Additional test case: Testing for 404 if event ID does not exist
@pytest.mark.integration
def test_get_event_by_nonexistent_event_id():
    token = get_bearer_token()
    headers = {"Authorization": token}

    nonexistent_event_id = 999999  # ID unlikely to exist
    response = client.get(f"/api/event/{nonexistent_event_id}", headers=headers)
    assert response.status_code == 404
