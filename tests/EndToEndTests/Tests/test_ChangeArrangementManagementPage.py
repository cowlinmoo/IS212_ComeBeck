import requests
import pytest

# Define constants
AUTH_URL = 'https://api.comebeckwfhtracker.systems/api/authenticate'
APPLICATION_URL = 'https://api.comebeckwfhtracker.systems/api/application'
DELETE_URL = 'https://api.comebeckwfhtracker.systems/api/application/delete/all_applications_by_staff_id/150348'
USERNAME = 'colinmok1000@gmail.com'
PASSWORD = 'password123'


@pytest.fixture(scope="session")
def bearer_token():
    """Obtain and return a Bearer token for authentication."""
    auth_response = requests.post(
        AUTH_URL,
        headers={'accept': 'application/json',
                 'Content-Type': 'application/x-www-form-urlencoded'},
        data={
            'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD,
            'scope': '',
            'client_id': 'string',
            'client_secret': 'string'
        }
    )

    token = auth_response.json().get('access_token')
    if not token:
        raise Exception("Authentication failed, could not retrieve access token")

    print(f"Obtained Bearer token: {token}")
    return token


@pytest.fixture(scope="function")
def create_test_application(bearer_token):
    """Create an application for testing, yield its data, and delete it after the test."""
    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {bearer_token}',
        'Content-Type': 'application/json'
    }
    data = {
        "location": "Home",
        "reason": "Vacation request",
        "requested_date": "2024-11-02",
        "application_hour": "fullday",
        "description": "Going on a family vacation",
        "staff_id": 150348
    }

    # Create the application
    response = requests.post(APPLICATION_URL, headers=headers, json=data)
    if response.status_code == 200:
        application_data = response.json()
        print("Application created successfully:", application_data)
    else:
        raise Exception(
            f"Failed to create application: {response.status_code} {response.json()}")

    # Yield the created application data to the test
    yield application_data

    # Debugging: Print token and headers before deletion
    print(f"Bearer token before deletion: {bearer_token}")
    print(f"Headers for deletion request: {headers}")

    # Cleanup: Delete all applications by staff_id
    delete_response = requests.delete(DELETE_URL, headers={
        'Authorization': f'Bearer {bearer_token}'})

    if delete_response.status_code == 200:
        print("Cleanup successful: All applications deleted for staff_id 150348.")
    else:
        print("Cleanup failed:", delete_response.status_code, delete_response.text)
        raise Exception("Cleanup failed: Unable to delete applications")


def test_create_application(create_test_application):
    """Test creating an application using the fixture."""
    application_data = create_test_application
    assert application_data is not None, "Application creation failed: No data returned."
    assert "application_id" in application_data, "Application creation failed: No application_id in response."
    assert application_data["reason"] == "Vacation request", "Unexpected reason value."
    assert application_data["events"][0][
               "location"] == "Home", "Unexpected location value."
    assert application_data["events"][0][
               "requested_date"] == "2024-11-02", "Unexpected requested date."
    assert application_data["events"][0][
               "application_hour"] == "fullday", "Unexpected application hour."
    assert application_data[
               "description"] == "Going on a family vacation", "Unexpected description."

    print("Application creation successful. Application data:", application_data)
