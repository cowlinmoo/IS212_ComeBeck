import pytest
import requests

from tests.EndToEndTests.Pages.PendingArrangementsPage import PendingArrangementPage
from tests.EndToEndTests.Pages.LoginPage import LoginPage
from tests.EndToEndTests.Tests.BaseTest import BaseTest

# Define constants
AUTH_URL = 'https://api.comebeckwfhtracker.systems/api/authenticate'
APPLICATION_URL = 'https://api.comebeckwfhtracker.systems/api/application'
DELETE_URL = 'https://api.comebeckwfhtracker.systems/api/application/delete/all_applications_by_staff_id/170216'
PROCESS_URL = 'https://api.comebeckwfhtracker.systems/api/application/process/{}'
USERNAME = 'Seng.Kesavan@allinone.com.sg'
PASSWORD = 'password123'


@pytest.fixture(scope="session")
def bearer_token():
    """Obtain and return a Bearer token for authentication."""
    auth_response = requests.post(
        AUTH_URL,
        headers={
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'grant_type': 'password',
            'username': USERNAME,
            'password': PASSWORD,
            'scope': '',
            'client_id': 'string',
            'client_secret': 'string'
        }
    )

    if auth_response.status_code != 200:
        raise Exception(f"Authentication failed: {auth_response.status_code} {auth_response.text}")

    token = auth_response.json().get('access_token')
    if not token:
        raise Exception("Authentication failed, could not retrieve access token")

    print(f"Obtained Bearer token: {token}")
    return token


@pytest.fixture(scope="function")
def create_test_application(bearer_token):
    """
    Create an application for testing, yield its data, and delete it after the test.
    """
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
        "staff_id": 170216
    }

    # Create the application
    response = requests.post(APPLICATION_URL, headers=headers, json=data)
    if response.status_code == 200:
        application_data = response.json()
        print("Application created successfully:", application_data)
    else:
        raise Exception(f"Failed to create application: {response.status_code} {response.text}")

    # Yield the created application data to the test
    yield application_data

    # Cleanup: Delete all applications by staff_id
    delete_response = requests.delete(
        DELETE_URL,
        headers={'Authorization': f'Bearer {bearer_token}'}
    )

    if delete_response.status_code == 200:
        print("Cleanup successful: All applications deleted for staff_id 170216.")
    else:
        print("Cleanup failed:", delete_response.status_code, delete_response.text)
        raise Exception("Cleanup failed: Unable to delete applications")


def verify_application_status(application_id, bearer_token, expected_status):
    """Verify the status of the application on the backend."""
    response = requests.get(
        f"{APPLICATION_URL}/{application_id}",
        headers={
            'accept': 'application/json',
            'Authorization': f'Bearer {bearer_token}'
        }
    )

    assert response.status_code == 200, f"Failed to fetch application: {response.status_code} {response.text}"

    application_data = response.json()
    actual_status = application_data.get("status")
    assert actual_status == expected_status, f"Expected status '{expected_status}', but got '{actual_status}'"

    print(f"Application {application_id} status verified as '{actual_status}'.")


class TestManagerReviewArrangementManagement(BaseTest):

    @pytest.mark.E2ETest
    def test_manager_approve_arrangement(self, create_test_application, bearer_token):
        # Log in to access the arrangement page
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        login_page.login(USERNAME, PASSWORD)
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        # Navigate to Arrangement Management page
        pending_arrangement_page = PendingArrangementPage(self.page)
        pending_arrangement_page.navigate_to_pending_arrangement_page()

        # Click review button and fill up reason
        pending_arrangement_page.click_review_button()
        pending_arrangement_page.enter_reason("Approved")

        # Click approve button
        pending_arrangement_page.click_approve_button()

        pending_arrangement_page.page.wait_for_timeout(5000)

        # Verify status on backend
        application_id = create_test_application["application_id"]
        verify_application_status(application_id, bearer_token, "approved")

    @pytest.mark.E2ETest
    def test_manager_reject_arrangement(self, create_test_application, bearer_token):
        # Log in to access the arrangement page
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        login_page.login(USERNAME, PASSWORD)
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        # Navigate to Arrangement Management page
        pending_arrangement_page = PendingArrangementPage(self.page)
        pending_arrangement_page.navigate_to_pending_arrangement_page()

        # Click review button and fill up reason
        pending_arrangement_page.click_review_button()
        pending_arrangement_page.enter_reason("Rejected")

        # Click approve button
        pending_arrangement_page.click_rejected_button()

        pending_arrangement_page.page.wait_for_timeout(5000)

        # Verify status on backend
        application_id = create_test_application["application_id"]
        verify_application_status(application_id, bearer_token, "rejected")
