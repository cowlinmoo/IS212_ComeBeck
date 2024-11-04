import pytest
import requests

from tests.EndToEndTests.Pages.WithdrawArrangementPage import WithdrawArrangementPage
from tests.EndToEndTests.Pages.LoginPage import LoginPage
from tests.EndToEndTests.Tests.BaseTest import BaseTest

# Define constants
AUTH_URL = 'https://api.comebeckwfhtracker.systems/api/authenticate'
APPLICATION_URL = 'https://api.comebeckwfhtracker.systems/api/application'
DELETE_URL = 'https://api.comebeckwfhtracker.systems/api/application/delete/all_applications_by_staff_id/171013'
PROCESS_URL = 'https://api.comebeckwfhtracker.systems/api/application/process/{}'
USERNAME = 'Narong.Pillai@allinone.com.sg'
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
        "staff_id": 171013
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
        print("Cleanup successful: All applications deleted for staff_id 171013.")
    else:
        print("Cleanup failed:", delete_response.status_code, delete_response.text)
        raise Exception("Cleanup failed: Unable to delete applications")


@pytest.fixture(scope="function")
def create_and_approve_application(bearer_token, create_test_application):
    """
    Create an application for testing, approve it, yield its data, and delete it after the test.
    """
    application_data = create_test_application
    application_id = application_data.get('application_id')
    if not application_id:
        raise Exception("Created application does not have an 'application_id'.")

    # Define the process URL with the specific application_id
    process_url = PROCESS_URL.format(application_id)

    # Define the request body for approval
    approval_data = {
        "status": "approved",
        "approver_id": 171014,
        "application_id": application_id,
        "outcome_reason": "Approved for testing purposes"
    }

    # Approve the application
    approval_response = requests.put(
        process_url,
        headers={
            'accept': 'application/json',
            'Authorization': f'Bearer {bearer_token}',
            'Content-Type': 'application/json'
        },
        json=approval_data
    )

    if approval_response.status_code == 200:
        approved_data = approval_response.json()
        print("Application approved successfully:", approved_data)
    else:
        raise Exception(f"Failed to approve application: {approval_response.status_code} {approval_response.text}")

    # Yield the approved application data to the test
    yield approved_data

class TestManagerWithdrawArrangementManagement(BaseTest):

    @pytest.mark.E2ETest
    def test_manager_withdraw_arrangement(self, create_and_approve_application):
        # Log in to access the arrangement page
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        login_page.login(USERNAME, PASSWORD)
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        # Navigate to Arrangement Management page
        withdraw_arrangement_page = WithdrawArrangementPage(self.page)
        withdraw_arrangement_page.navigate_to_withdraw_arrangement_page()

        # Select the first arrangement in the list
        withdraw_arrangement_page.select_first_arrangement()

        # Withdraw the selected arrangement
        withdraw_arrangement_page.withdraw_selected_arrangement()

        withdraw_arrangement_page.page.wait_for_timeout(5000)

        # Verify that the table is now empty
        assert withdraw_arrangement_page.is_table_empty(), "Table is not empty; event was not successfully withdrawn."
        print("Event withdrawn successfully; table is now empty.")

