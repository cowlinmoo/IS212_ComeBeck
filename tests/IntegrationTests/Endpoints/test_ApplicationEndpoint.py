import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# Helper function to get the token
def get_bearer_token():
    form_data = {
        "username": "colinmok1000@gmail.com",
        "password": "password123"
    }
    response = client.post("http://localhost:8080/api/authenticate", data=form_data)
    assert response.status_code == 200
    return f"Bearer {response.json()['access_token']}"

# Fixture to create a new application for each test
@pytest.fixture
def create_application():
    token = get_bearer_token()
    headers = {"Authorization": token}
    application_data = {
        "location": "Home",
        "reason": "Work on site",
        "requested_date": "2024-11-01",
        "application_hour": "pm",
        "description": "On-site project work",
        "staff_id": 300000
    }

    # Create the application
    response = client.post("http://localhost:8080/api/application", json=application_data, headers=headers)
    assert response.status_code == 200, "Failed to create application for test setup"
    application_id = response.json()["application_id"]

    yield application_id  # Provide the application ID to the test

# Test to retrieve applications by staff ID
@pytest.mark.integration
def test_get_applications_by_staff_id(create_application):
    token = get_bearer_token()
    headers = {"Authorization": token}
    staff_id = 300000  # Replace with a valid staff ID in the test database

    response = client.get(f"http://localhost:8080/api/application/staff/{staff_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Assuming there is at least one application for this staff ID

# Test to retrieve applications by approver ID
@pytest.mark.integration
def test_get_applications_by_approver_id(create_application):
    token = get_bearer_token()
    headers = {"Authorization": token}
    approver_id = 130002  # Replace with a valid approver ID in the test database

    response = client.get(f"http://localhost:8080/api/application/approver/{approver_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# Test to retrieve applications by status
@pytest.mark.integration
def test_get_applications_by_status(create_application):
    token = get_bearer_token()
    headers = {"Authorization": token}
    status = "pending"  # You can test for other statuses such as "approved" or "withdrawn"

    response = client.get(f"http://localhost:8080/api/application/status/{status}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# Test to process (approve/reject) an application
@pytest.mark.integration
def test_process_application(create_application):
    token = get_bearer_token()
    headers = {"Authorization": token}
    application_id = create_application  # Use application created by fixture

    process_data = {
        "status": "approved",
        "approver_id": 130002,  # Replace with a valid approver ID
        "application_id": application_id,
        "outcome_reason": "Approved for work on site"
    }

    response = client.put(f"http://localhost:8080/api/application/process/{application_id}", json=process_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "approved"
    assert data["outcome_reason"] == process_data["outcome_reason"]

# Test to get all employee locations by manager ID
@pytest.mark.integration
def test_get_employee_locations_by_manager_id():
    token = get_bearer_token()
    headers = {"Authorization": token}
    manager_id = 400000  # Replace with a valid manager ID in the test database

    response = client.get(f"http://localhost:8080/api/application/location/{manager_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "location" in data[0]
        assert "employee_id" in data[0]

# Test to create a new application (Requires a bearer token)
@pytest.mark.integration
def test_create_application():
    token = get_bearer_token()
    headers = {"Authorization": token}
    application_data = {
        "location": "Office",
        "reason": "Client meeting",
        "requested_date": "2024-11-02",
        "application_hour": "am",
        "description": "Discuss project requirements",
        "staff_id": 300000  # Adjust with a valid staff ID for the test
    }

    response = client.post("http://localhost:8080/api/application", json=application_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["reason"] == application_data["reason"]
    assert data["description"] == application_data["description"]
    assert data["staff_id"] == application_data["staff_id"]
    assert data["events"][0]["location"] == application_data["location"]
    assert data["events"][0]["application_hour"] == application_data["application_hour"]
    assert data["events"][0]["requested_date"] == application_data["requested_date"]
