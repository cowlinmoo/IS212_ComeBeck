import pytest
from tests.EndToEndTests.Pages.LoginPage import LoginPage
from tests.EndToEndTests.Pages.ArrangementManagementPage import ArrangementManagementPage
from tests.EndToEndTests.Tests.BaseTest import BaseTest

class TestArrangementManagement(BaseTest):

    @pytest.mark.E2ETest
    def test_submit_single_date_application(self):
        # Log in to access the arrangement page
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        login_page.login("colinmok1000@gmail.com", "password123")
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        # Navigate to Arrangement Management page
        arrangement_page = ArrangementManagementPage(self.page)
        arrangement_page.navigate_to_arrangement_page()

        # Fill in the form fields
        arrangement_page.select_multiple_dates(False)  # Select 'No' for multiple dates
        arrangement_page.select_date()  # Choose a specific date
        arrangement_page.select_time_slot("AM")  # Select 'AM' time slot
        arrangement_page.fill_reason("Requesting WFH for project focus")

        # Submit the form
        arrangement_page.submit_application()

        # Assert successful submission (customize as per actual success indication)
        success_message = self.page.locator("text=Your WFH request has been successfully submitted.")  # Placeholder for actual success text
        success_message.wait_for(state="visible",
                                 timeout=15000)  # Wait up to 10 seconds
        assert success_message.is_visible(), "Application submission failed or success message not visible"

    @pytest.mark.E2ETest
    def test_submit_multiple_date_application(self):
        # Log in to access the arrangement page
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        login_page.login("colinmok1000@gmail.com", "password123")
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        # Navigate to Arrangement Management page
        arrangement_page = ArrangementManagementPage(self.page)
        arrangement_page.navigate_to_arrangement_page()

        # Select multiple dates
        arrangement_page.select_multiple_dates(True)  # Select 'Yes' for multiple dates
        arrangement_page.select_dates(["11", "12"])  # Choose specific dates (ensure
        # these are weekdays for 2024)

        # Fill other form fields
        arrangement_page.select_time_slot("AM")  # Select 'AM' time slot for all selected dates
        arrangement_page.fill_reason("Requesting multiple WFH days for project deadlines")

        # Submit the form
        arrangement_page.submit_application()

        # Assert successful submission (customize as per actual success indication)
        success_message = self.page.locator("text=Your WFH request has been successfully submitted.")
        success_message.wait_for(state="visible", timeout=15000)  # Wait up to 15 seconds
        assert success_message.is_visible(), "Multiple-date application submission failed or success message not visible"

    @pytest.mark.E2ETest
    def test_submit_recurring_arrangement_application(self):
        # Log in to access the arrangement page
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        login_page.login("colinmok1000@gmail.com", "password123")
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        # Navigate to Arrangement Management page
        arrangement_page = ArrangementManagementPage(self.page)
        arrangement_page.navigate_to_arrangement_page()

        # Select options for recurring arrangement
        arrangement_page.select_multiple_dates(False)  # Select 'No' for multiple dates
        arrangement_page.select_date("13")  # Select a specific start date (e.g., 13th)
        arrangement_page.select_time_slot("AM")  # Select 'AM' time slot

        # Choose recurring options
        arrangement_page.select_recurring_arrangement(True)  # Select 'Yes' for recurring arrangement
        arrangement_page.select_recurring_type("Weekly")  # Choose 'Weekly' recurrence
        arrangement_page.select_end_date("27")  # Select an end date for the recurrence

        # Fill reason for recurring arrangement
        arrangement_page.fill_reason("Recurring WFH arrangement for project")

        # Submit the form
        arrangement_page.submit_application()

        # Assert successful submission (customize as per actual success indication)
        success_message = self.page.locator("text=Your WFH request has been successfully submitted.")
        success_message.wait_for(state="visible", timeout=15000)  # Wait up to 15 seconds
        assert success_message.is_visible(), "Recurring arrangement submission failed or success message not visible"