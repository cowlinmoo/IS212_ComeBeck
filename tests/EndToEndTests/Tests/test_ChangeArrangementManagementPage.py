import pytest
import requests

from tests.EndToEndTests.Pages.LoginPage import LoginPage
from tests.EndToEndTests.Pages.ArrangementManagementPage import ArrangementManagementPage
from tests.EndToEndTests.Tests.BaseTest import BaseTest

# Define constants
AUTH_URL = 'https://api.comebeckwfhtracker.systems/api/authenticate'
APPLICATION_URL = 'https://api.comebeckwfhtracker.systems/api/application'
DELETE_URL = 'https://api.comebeckwfhtracker.systems/api/application/delete/all_applications_by_staff_id/171043'
USERNAME = 'Rithy.Luong@allinone.com.sg'
PASSWORD = 'password123'


@pytest.fixture(scope="session")
def bearer_token():
    """Obtain and return a Bearer token for authentication."""
    auth_response = requests.post(
        AUTH_URL,
        headers={'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'},
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
        "staff_id": 171043
    }

    # Create the application
    response = requests.post(APPLICATION_URL, headers=headers, json=data)
    if response.status_code == 200:
        application_data = response.json()
        print("Application created successfully:", application_data)
    else:
        raise Exception(f"Failed to create application: {response.status_code} {response.json()}")

    # Yield the created application data to the test
    yield application_data

    # Cleanup: Delete all applications by staff_id
    delete_response = requests.delete(DELETE_URL, headers={
        'Authorization': f'Bearer {bearer_token}'})

    if delete_response.status_code == 200:
        print("Cleanup successful: All applications deleted for staff_id 171043.")
    else:
        print("Cleanup failed:", delete_response.status_code, delete_response.text)
        raise Exception("Cleanup failed: Unable to delete applications")


@pytest.mark.usefixtures("create_test_application")
class TestChangeArrangementManagement(BaseTest):
    
    @pytest.mark.E2ETest
    def test_submit_single_date_change(self, create_test_application):
        # Log in to access the arrangement page
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        login_page.login(USERNAME, PASSWORD)
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        # Navigate to Arrangement Management page
        arrangement_page = ArrangementManagementPage(self.page)
        arrangement_page.navigate_to_arrangement_page()

        # Switch to the "Change arrangement" tab
        arrangement_page.switch_to_change_tab()

        # Select "Pending Approval" filter
        arrangement_page.select_pending_approval()

        # Select the first arrangement to change
        arrangement_page.select_first_arrangement_to_change()

        # Select the date to change
        arrangement_page.select_date("27")

        # Select the time slot
        arrangement_page.select_time_slot("AM")  # Select 'AM' time slot

        # Fill reason for change
        arrangement_page.fill_reason_for_change("Change from 2 November to 27 November")

        # Submit the change
        arrangement_page.submit_change()

        success_message = self.page.locator("text=Your change request has been  successfully submitted.")  # Placeholder for actual success text

        success_message.wait_for(state="visible",
                                 timeout=15000)  # Wait up to 10 seconds
        assert success_message.is_visible(), "Change submission failed or success message not visible"
