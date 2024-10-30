from playwright.sync_api import Page
from tests.EndToEndTests.Pages.BasePage import BasePage

class SchedulePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Refined locators within the tablist div for each tab button
        self.department_schedule_tab = "div[role='tablist'] button[role='tab'][aria-controls*='department']:has-text('Department Schedule')"
        self.team_schedule_tab = "div[role='tablist'] button[role='tab']:has-text('Team Schedule')"
        self.my_schedule_tab = "div[role='tablist'] button[role='tab']:has-text('My Schedule')"
        self.percentage_display = "span.font-bold.text-green-500"  # Locator for the percentage display
        self.my_team_tab = "button:has-text('My Team')"  # Locator for "My Team" tab
        self.team_members_i_manage_tab = "button:has-text('Team Members I Manage')"  # Locator for "Team Members I Manage" tab

    def navigate_to_schedule(self):
        """Navigate directly to the schedule page."""
        self.navigate("https://comebeckwfhtracker.systems/schedule")

    def is_department_schedule_tab_visible(self) -> bool:
        """Check if the 'Department Schedule' tab is visible."""
        return self.is_element_visible(self.department_schedule_tab)

    def is_percentage_display_visible(self) -> bool:
        """Check if the percentage display is visible."""
        percentage_display = self.page.locator(self.percentage_display)
        percentage_display.wait_for(state="visible", timeout=10000)
        return percentage_display.is_visible()

    def is_my_team_tab_visible(self) -> bool:
        """Check if the 'My Team' tab is visible."""
        my_team_tab = self.page.locator(self.my_team_tab)
        my_team_tab.wait_for(state="visible", timeout=10000)
        return my_team_tab.is_visible()

    def is_team_members_i_manage_tab_visible(self) -> bool:
        """Check if the 'Team Members I Manage' tab is visible."""
        team_members_i_manage_tab = self.page.locator(self.team_members_i_manage_tab)
        team_members_i_manage_tab.wait_for(state="visible", timeout=10000)
        return team_members_i_manage_tab.is_visible()

    def is_team_members_i_manage_tab_hidden(self) -> bool:
        """Check if the 'Team Members I Manage' tab is hidden or not present."""
        team_members_i_manage_tab = self.page.locator(self.team_members_i_manage_tab)
        self.page.wait_for_timeout(5000)
        return not team_members_i_manage_tab.is_visible()