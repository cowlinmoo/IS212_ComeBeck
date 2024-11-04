import pytest
import requests

from tests.EndToEndTests.Pages.ArrangementApprovalsPage import ArrangementApprovalsPage
from tests.EndToEndTests.Pages.LoginPage import LoginPage
from tests.EndToEndTests.Tests.BaseTest import BaseTest

# Define constants
AUTH_URL = 'https://api.comebeckwfhtracker.systems/api/authenticate'
APPLICATION_URL = 'https://api.comebeckwfhtracker.systems/api/application'
DELETE_URL = 'https://api.comebeckwfhtracker.systems/api/application/delete/all_applications_by_staff_id/171018'
PROCESS_URL = 'https://api.comebeckwfhtracker.systems/api/application/process/{}'
USERNAME = 'Ji.Truong@allinone.com.sg'
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
        "staff_id": 171018
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
        print("Cleanup successful: All applications deleted for staff_id 171018.")
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
        "approver_id": 170166,
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

@pytest.fixture(scope="function")
def create_and_reject_application(bearer_token, create_test_application):
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
        "status": "rejected",
        "approver_id": 170166,
        "application_id": application_id,
        "outcome_reason": "Rejected for testing purposes"
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
        print("Application rejected successfully:", approved_data)
    else:
        raise Exception(f"Failed to approve application: {approval_response.status_code} {approval_response.text}")

    # Yield the approved application data to the test
    yield approved_data

# #     # Cleanup is handled by create_test_application fixture
# def test_create_and_approve_application(create_and_approve_application):
#     """Test if create_and_approve_application fixture creates and approves an application."""
#     approved_data = create_and_approve_application
#     assert approved_data.get('status') == "approved", "Application approval failed or incorrect status"
#     assert approved_data.get('application_id') is not None, "Approved application missing 'application_id'"
#     print("Application approved successfully with ID:", approved_data['application_id'])
#
# def test_create_and_reject_application(create_and_reject_application):
#     """Test if create_and_approve_application fixture creates and approves an application."""
#     approved_data = create_and_reject_application
#     assert approved_data.get('status') == "rejected", "Application rejection failed or incorrect status"
#     assert approved_data.get('application_id') is not None, "Rejected application missing 'application_id'"
#     print("Application rejected successfully with ID:", approved_data['application_id'])

class TestArrangementApprovals(BaseTest):

    @pytest.mark.E2ETest
    def test_pending_arrangement(self, create_test_application):
        # Log in to access the arrangement page
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        login_page.login(USERNAME, PASSWORD)
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        # Navigate to Arrangement Management page
        approvals_page = ArrangementApprovalsPage(self.page)
        approvals_page.navigate_to_approvals_page()

        # Select Pending Requests tab
        approvals_page.select_pending_requests()

        # Get the content of the first application card
        first_application_content = approvals_page.get_first_application_content()

        print("This is the content",first_application_content)

        # Verify the content of the first application card
        expected_content = {
            "Application ID": str(create_test_application['application_id']),
            "Application Type": "New Application",
            "Application Reason": create_test_application['reason'],
            "Approved by": "-",
            "Recurring": "No"
        }
        for key, expected_value in expected_content.items():
            actual_value = first_application_content.get(key)
            assert actual_value == expected_value, f"Expected '{key}: {expected_value}', but got '{actual_value}'"

        print("All content matches expected values.")

    @pytest.mark.E2ETest
    def test_approved_arrangement(self, create_and_approve_application):
        # Log in to access the arrangement page
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        login_page.login(USERNAME, PASSWORD)
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        # Navigate to Arrangement Management page
        approvals_page = ArrangementApprovalsPage(self.page)
        approvals_page.navigate_to_approvals_page()

        # Select Pending Requests tab
        approvals_page.select_approved_requests()

        # Get the content of the first application card
        first_application_content = approvals_page.get_first_approved_application_content()

        print("This is the content",first_application_content)

        # Verify the content of the first application card
        # Verify the content of the first application card
        expected_content = {
            "Application ID": str(create_and_approve_application['application_id']),
            "Application Type": "New Application",
            "Approval Reason": create_and_approve_application['outcome_reason'],
            "Approved by": str(create_and_approve_application['approver_id']),
            "Recurring": "No" if not create_and_approve_application[
                'recurring'] else "Yes"
        }

        for key, expected_value in expected_content.items():
            actual_value = first_application_content.get(key)
            assert actual_value == expected_value, f"Expected '{key}: {expected_value}', but got '{actual_value}'"

        print("All content matches expected values.")

    @pytest.mark.E2ETest
    def test_rejected_arrangement(self, create_and_reject_application):
        # Log in to access the arrangement page
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        login_page.login(USERNAME, PASSWORD)
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        # Navigate to Arrangement Management page
        approvals_page = ArrangementApprovalsPage(self.page)
        approvals_page.navigate_to_approvals_page()

        # Select Pending Requests tab
        approvals_page.select_rejected_requests()

        # Get the content of the first application card
        first_application_content = approvals_page.get_first_rejected_application_content()

        print("This is the content",first_application_content)

        # Verify the content of the first application card
        # Verify the content of the first application card
        expected_content = {
            "Application ID": str(create_and_reject_application['application_id']),
            "Application Type": "New Application",
            "Rejection Reason": create_and_reject_application['outcome_reason'],
            "Rejected by": str(create_and_reject_application['approver_id']),
            "Recurring": "No"
        }

        for key, expected_value in expected_content.items():
            actual_value = first_application_content.get(key)
            assert actual_value == expected_value, f"Expected '{key}: {expected_value}', but got '{actual_value}'"

        print("All content matches expected values.")