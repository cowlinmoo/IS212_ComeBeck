from playwright.sync_api import Page
from tests.End2EndTests.Pages.BasePage import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)  # Initialize BasePage with the current page instance
        self.username_input = "#username"
        self.password_input = "#password"
        self.login_button = "button[type='submit']"
        self.error_message_text = "Login failed"  # Text content for the error message
        self.department_schedule_tab = "text='Department Schedule'"  # Locator for "Department Schedule" tab

    def navigate_to_login(self):
        """Navigate to the login page."""
        self.navigate("https://comebeckwfhtracker.systems/login")

    def login(self, username: str, password: str):
        """Log in using provided username and password."""
        self.fill_input(self.username_input, username)
        self.fill_input(self.password_input, password)
        self.click_element(self.login_button)

    def is_department_schedule_visible(self):
        """Check if the "Department Schedule" tab is visible."""
        return self.is_element_visible(self.department_schedule_tab)

    def get_error_message_text(self):
        """Return the text of the error message if it appears."""
        # Check for the error message using the text directly
        error_message = self.page.locator(f"text={self.error_message_text}")
        print("This is the error message ",error_message.text_content())
        # Wait for the error message to become visible and return text if present
        if error_message.is_visible(timeout=5000):  # Wait up to 5 seconds
            print("This is the error message ",error_message.text_content())
            return error_message.text_content()
        return ""
