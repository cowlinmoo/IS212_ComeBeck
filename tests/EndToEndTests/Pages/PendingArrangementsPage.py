from playwright.sync_api import Page
from tests.EndToEndTests.Pages.BasePage import BasePage

class PendingArrangementPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Define selectors
        self.review_button = "button:text('Review')"
        self.approve_button = "button:text('Approve')"
        self.reject_button = "button:text('Reject')"
        self.reason_textarea = "textarea[placeholder='Enter your reason here']"

    def navigate_to_pending_arrangement_page(self):
        """Navigate directly to the arrangement page."""
        self.navigate("https://comebeckwfhtracker.systems/managementViewPending")

    def click_review_button(self):
        """Click the review button."""
        self.page.locator(self.review_button).click()

    def click_approve_button(self):
        """Click the approve button."""
        self.page.locator(self.approve_button).click()

    def click_rejected_button(self):
        """Click the rejected button."""
        self.page.locator(self.reject_button).click()

    def enter_reason(self, reason: str):
        """Enter a reason for the arrangement."""
        self.page.locator(self.reason_textarea).fill(reason)