import pytest
from fastapi.testclient import TestClient
from backend.main import app  # assuming this is the app instance of FastAPI

client = TestClient(app)

@pytest.mark.integration
def test_login_for_access_token_success():
    # Define valid form data for authentication
    form_data = {
        "username": "colinmok1000@gmail.com",
        "password": "password123"
    }

    # Send POST request to the backend running on localhost
    response = client.post("http://localhost:8080/api/authenticate", data=form_data)

    # Assert that the response indicates success
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["email"] == form_data["username"]

@pytest.mark.integration
def test_login_for_access_token_failure():
    # Define invalid credentials
    form_data = {
        "username": "invaliduser@example.com",
        "password": "wrongpassword"
    }

    # Send POST request to the backend with invalid credentials
    response = client.post("http://localhost:8080/api/authenticate", data=form_data)

    print("this is the response: ",response.json())
    # Assert that the response indicates unauthorized access
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}