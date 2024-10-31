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


# Expected data in the database for department IDs and their respective data
expected_data = {
    "CEO": 1,
    "Sales": 2,
    "Solutioning": 3,
    "Engineering": 4,
    "HR": 5,
    "Finance": 6,
    "Consultancy": 7,
    "IT": 8,
    "Testing": 9,
}



# Test to get a department by department_id
@pytest.mark.integration
@pytest.mark.parametrize("department_name, department_id", expected_data.items())
def test_get_department_by_department_id(department_name, department_id):
    token = get_bearer_token()
    headers = {"Authorization": token}

    response = client.get(f"http://localhost:8080/api/department/{department_id}",
                          headers=headers)
    assert response.status_code == 200
    data = response.json()

    # Validate the response data
    assert data["department_id"] == department_id
    assert data["name"] == department_name


# Test to get all departments
@pytest.mark.integration
def test_get_all_departments():
    token = get_bearer_token()
    headers = {"Authorization": token}

    response = client.get("http://localhost:8080/api/department", headers=headers)
    assert response.status_code == 200
    data = response.json()

    # Validate the response data length
    assert isinstance(data, list)
    assert len(data) == len(
        expected_data)  # Ensure it matches the number of departments

    # Check that each department exists in the response
    for department in data:
        assert department["name"] in expected_data
        assert department["department_id"] == expected_data[department["name"]]
