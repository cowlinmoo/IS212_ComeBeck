import pytest
from playwright.sync_api import Browser, Page, Playwright

class BaseTest:
    @pytest.fixture(scope="function", autouse=True)
    def setup_page(self, playwright: Playwright):
        """Fixture to set up browser and page context for each test."""
        self.browser: Browser = playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context()  # Separate context for parallel compatibility
        self.page: Page = self.context.new_page()
        yield self.page  # Provide the page to each test
        self.context.close()
        self.browser.close()

    def navigate_to(self, url: str):
        """Navigate to a specified URL."""
        self.page.goto(url)

    def wait_for_url(self, url: str):
        """Wait for the page to load the specified URL."""
        self.page.wait_for_url(url)