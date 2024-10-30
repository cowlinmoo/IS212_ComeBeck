import pytest
from tests.EndToEndTests.Pages.LoginPage import LoginPage
from tests.EndToEndTests.Pages.SchedulePage import SchedulePage
from tests.EndToEndTests.Tests.BaseTest import BaseTest

class TestSchedulePage(BaseTest):

    @pytest.mark.E2ETest
    def test_department_schedule_tab_visible_for_authorized_user(self):
        # Initialize LoginPage and log in as a user with "Department Schedule" access
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        login_page.login("colinmok1000@gmail.com", "password123")

        # Wait until redirected to the schedule page
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        # Initialize SchedulePage and check if the "Department Schedule" tab is visible
        schedule_page = SchedulePage(self.page)
        schedule_page.navigate_to_schedule()

        # Wait for the specific "Department Schedule" tab within the role="tablist" div
        department_schedule_tab = self.page.locator(
            "div[role='tablist'] button[role='tab'][aria-controls*='department']:has-text('Department Schedule')"
        )
        department_schedule_tab.wait_for(state="visible", timeout=10000)

        assert schedule_page.is_department_schedule_tab_visible(), (
            "Department Schedule tab should be visible for this user"
        )

    @pytest.mark.E2ETest
    def test_department_schedule_tab_not_visible_for_unauthorized_user(self):
        # Initialize LoginPage and log in as a user without "Department Schedule" access
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        login_page.login("colinmok3@gmail.com", "password123")

        # Wait until redirected to the schedule page
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        # Initialize SchedulePage and check if the "Department Schedule" tab is not visible
        schedule_page = SchedulePage(self.page)
        schedule_page.navigate_to_schedule()

        # Look for the specific "Department Schedule" tab within the role="tablist" div
        department_schedule_tab = self.page.locator(
            "div[role='tablist'] button[role='tab'][aria-controls*='department']:has-text('Department Schedule')"
        )
        self.page.wait_for_timeout(5000)
        # Check for absence or non-visibility of the tab
        assert not department_schedule_tab.is_visible(), (
            "Department Schedule tab should not be visible for this user"
        )

    @pytest.mark.E2ETest
    def test_team_schedule_page_elements_visible_for_manager(self):
        # Initialize LoginPage and log in as a manager to access the team schedule
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        self.page.wait_for_load_state("networkidle")

        # Use manager credentials to log in
        username = "colinmok1000@gmail.com"
        password = "password123"
        login_page.login(username, password)

        # Wait until redirected to the team schedule page
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")
        self.page.wait_for_load_state("networkidle")

        # Initialize TeamSchedulePage and check for the percentage display and tabs
        team_schedule_page = SchedulePage(self.page)

        # Assert that the percentage display is present
        assert team_schedule_page.is_percentage_display_visible(), "Percentage display is not visible on Team Schedule page."

        # Assert that both "My Team" and "Team Members I Manage" tabs are visible
        assert team_schedule_page.is_my_team_tab_visible(), "'My Team' tab is not visible on Team Schedule page."
        assert team_schedule_page.is_team_members_i_manage_tab_visible(), "'Team Members I Manage' tab is not visible on Team Schedule page."

    @pytest.mark.E2ETest
    def test_team_schedule_page_elements_visible_for_normal_employee(self):
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        self.page.wait_for_load_state("networkidle")

        username = "colinmok3@gmail.com"
        password = "password123"
        login_page.login(username, password)
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")
        self.page.wait_for_load_state("networkidle")

        team_schedule_page = SchedulePage(self.page)
        assert team_schedule_page.is_percentage_display_visible(), "Percentage display is not visible on Team Schedule page."
        assert team_schedule_page.is_my_team_tab_visible(), "'My Team' tab is not visible on Team Schedule page."
        assert team_schedule_page.is_team_members_i_manage_tab_hidden(), "'Team Members I Manage' tab is visible for normal employee, but it should not be."