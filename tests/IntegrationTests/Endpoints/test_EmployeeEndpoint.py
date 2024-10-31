import time

import pytest
from fastapi.testclient import TestClient
from backend.main import app

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
def generate_unique_email():
    timestamp = int(time.time() * 1000)  # Unique identifier based on current timestamp
    return f"johndoe_{timestamp}@example.com"

# Sample employee data with a unique email
sample_employee_create = {
    "staff_fname": "John",
    "staff_lname": "Doe",
    "position": "Software Engineer",
    "team_id": 1,
    "country": "USA",
    "email": generate_unique_email(),
    "role": 1,  # STAFF role ID
    "password": "securepassword"
}

sample_employee_update = {
    "staff_fname": "John",
    "staff_lname": "Smith",
    "position": "Lead Engineer",
    "country": "Canada"
}

# Fixture to create and clean up a dummy employee
@pytest.fixture
def dummy_employee():
    # Create employee
    response = client.post("/api/employee", json=sample_employee_create)
    assert response.status_code == 200
    employee_data = response.json()

    print(f"Created employee: {employee_data}")
    # Yield the created employee data to be used in the test
    yield employee_data

    # Delete the employee after the test
    token = get_bearer_token()
    headers = {"Authorization": token}

# Test to get all employees
@pytest.mark.integration
def test_get_all_employees():
    token = get_bearer_token()
    headers = {"Authorization": token}

    response = client.get("/api/employee", headers=headers)
    assert response.status_code == 200
    data = response.json()

    # Check if the response is a list
    assert isinstance(data, list)

    # Check that the data contains employee entries
    if data:
        assert "staff_id" in data[0]
        assert "staff_fname" in data[0]

# Test to get a specific employee by staff_id
@pytest.mark.integration
def test_get_employee_by_staff_id(dummy_employee):
    token = get_bearer_token()
    headers = {"Authorization": token}

    # Retrieve the dummy employee by their staff_id
    response = client.get(f"/api/employee/{dummy_employee['staff_id']}", headers=headers)
    assert response.status_code == 200
    data = response.json()

    # Verify returned data structure
    assert data["staff_id"] == dummy_employee["staff_id"]
    assert data["staff_fname"] == dummy_employee["staff_fname"]
    assert data["email"] == dummy_employee["email"]