import pytest
from Pages.LoginPage import LoginPage

@pytest.fixture(scope="function")
def setup_page(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    yield page
    browser.close()

def test_successful_login(setup_page):
    page = setup_page
    login_page = LoginPage(page)
    login_page.navigate()
    # Use valid credentials to log in successfully
    login_page.login("colinmok1000@gmail.com", "password123")
    page.wait_for_url("https://comebeckwfhtracker.systems/schedule")
    # Assert that the user is redirected to the schedule page
    assert page.url == "https://comebeckwfhtracker.systems/schedule", "User was not redirected to the expected page after login"


def test_login_failed_message(setup_page):
    page = setup_page
    login_page = LoginPage(page)
    login_page.navigate()
    
    # Use invalid credentials to trigger the error message
    login_page.login("invalid_user@example.com", "invalid_password")
    
    # Assert that the error message appears
    assert login_page.error_message.text_content() == "Login failed", "Error message text does not match expected"
