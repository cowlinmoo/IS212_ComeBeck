from playwright.sync_api import Page
from tests.EndToEndTests.Pages.BasePage import BasePage

class DepartmentSchedulePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Selector for the department schedule table rows
        self.table_rows_selector = "table.w-full tbody tr"

    def navigate_to_department_schedule(self):
        """Navigate directly to the department schedule page."""
        self.navigate("https://comebeckwfhtracker.systems/overview")

    def get_table_rows(self):
        """Retrieve all rows in the department schedule table."""
        return self.page.locator(self.table_rows_selector)
