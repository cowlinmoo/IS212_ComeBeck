from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        """Navigate to a specified URL."""
        self.page.goto(url)

    def is_element_visible(self, locator: str) -> bool:
        """Check if an element is visible on the page by locator text or selector."""
        return self.page.locator(locator).is_visible()

    def click_element(self, locator: str):
        """Click an element by its locator."""
        self.page.locator(locator).click()

    def fill_input(self, locator: str, value: str):
        """Fill an input field by its locator."""
        self.page.locator(locator).fill(value)
