from playwright.sync_api import Page
from tests.EndToEndTests.Pages.BasePage import BasePage

class WithdrawArrangementPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Define selectors
        self.first_arrangement = "table tbody tr:first-child button[role='checkbox']"
        self.withdraw_button = "button:text('Withdraw Selected Events')"
        self.table_body = "table tbody"

    def navigate_to_withdraw_arrangement_page(self):
        """Navigate directly to the arrangement page."""
        self.navigate("https://comebeckwfhtracker.systems/managementViewWithdraw")

    def select_first_arrangement(self):
        """Select the first arrangement in the list."""
        self.page.locator(self.first_arrangement).click()

    def withdraw_selected_arrangement(self):
        """Withdraw the selected arrangement."""
        self.page.locator(self.withdraw_button).click()

    def is_table_empty(self):
        """Check if the table is empty."""
        return self.page.locator(f"{self.table_body} tr").count() == 0