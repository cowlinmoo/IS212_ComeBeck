import pytest
from tests.EndToEndTests.Pages.LoginPage import LoginPage
from tests.EndToEndTests.Tests.BaseTest import BaseTest

class TestDepartmentScheduleVisibility(BaseTest):

    @pytest.mark.E2ETest
    def test_department_schedule_visibility_for_specific_user(self):
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()

        # Use specific credentials to log in (adjust based on your requirement)
        username = "colinmok1000@gmail.com"
        password = "password123"

        login_page.login(username, password)
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        self.page.wait_for_selector("text='Department Schedule'", timeout=5000)

        # Assert that "Department Schedule" tab is visible
        assert login_page.is_department_schedule_visible(), "Department Schedule tab is not visible for user with department access"

    @pytest.mark.E2ETest
    def test_department_schedule_not_visible_for_other_user(self):
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()

        # Use different credentials that should not have access to "Department Schedule"
        username = "colinmok3@gmail.com"
        password = "password123"

        login_page.login(username, password)
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        # Assert that "Department Schedule" tab is not visible
        assert not login_page.is_department_schedule_visible(), "Department Schedule tab is visible for user without department access"