import pytest
from tests.EndToEndTests.Pages.LoginPage import LoginPage
from tests.EndToEndTests.Tests.BaseTest import BaseTest

class TestLogin(BaseTest):

    @pytest.mark.E2ETest
    def test_successful_login(self):
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        login_page.login("colinmok1000@gmail.com", "password123")
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")
        assert self.page.url == "https://comebeckwfhtracker.systems/schedule", "User was not redirected to the expected page after login"

    @pytest.mark.E2ETest
    def test_login_failed_message(self):
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        login_page.login("invalid_user@example.com", "invalid_password")
        assert login_page.get_error_message_text() == "Login failed", "Error message text does not match expected"