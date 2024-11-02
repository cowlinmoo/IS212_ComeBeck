from playwright.sync_api import Page
from tests.EndToEndTests.Pages.BasePage import BasePage

class ArrangementManagementPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Define selectors
        self.arrangement_type_label = "label:text('Arrangement Type:')"
        self.submit_button = "button[type='submit']"

    def navigate_to_arrangement_page(self):
        """Navigate directly to the arrangement page."""
        self.navigate("https://comebeckwfhtracker.systems/arrangement")

    def select_multiple_dates(self, is_multiple: bool):
        """Select 'Yes' or 'No' for 'Is this for multiple dates?'."""
        if is_multiple:
            self.page.locator("button[role='radio'][value='Yes']").click()
        else:
            self.page.locator("button[role='radio'][value='No']").click()

    def select_date(self, date_str: str = "6"):
        """Open the date picker and select a specific day."""
        # Click on the "Pick a date" button to open the date picker
        self.page.locator("button:has-text('Pick a date')").click()

        # Wait for the date picker pop-up to appear
        date_picker_popup = self.page.locator("div[role='dialog']")
        date_picker_popup.wait_for(state="visible")

        # Click on the specific date within the date picker
        date_picker_popup.locator(f"button:has-text('{date_str}')").click()

    def select_dates(self, date_list):
        """Open the date picker and select multiple days."""
        # Click on the "Pick a date" button to open the date picker
        self.page.locator("button:has-text('Pick at least 2 dates')").click()

        # Wait for the date picker pop-up to appear
        date_picker_popup = self.page.locator("div[role='dialog']")
        date_picker_popup.wait_for(state="visible")

        # Click on each date in the provided list
        for date_str in date_list:
            date_picker_popup.locator(f"button:has-text('{date_str}')").click()

    def select_time_slot(self, time_slot: str):
        """Select all occurrences of a specified time slot (e.g., 'Full Day', 'AM', 'PM')."""
        time_slot_value = time_slot.lower()
        if time_slot_value in ["fullday", "am", "pm"]:
            # Locate all radio buttons with the specified value
            time_slot_buttons = self.page.locator(
                f"button[role='radio'][value='{time_slot_value}']")
            count = time_slot_buttons.count()

            # Click each occurrence of the specified time slot
            for i in range(count):
                time_slot_buttons.nth(i).click()

    def fill_reason(self, reason: str):
        """Fill the reason for the arrangement."""
        # Use a simpler selector by locating the textarea based on its placeholder text
        self.page.locator("textarea[placeholder='Please provide a reason for your arrangement request.']").fill(reason)

    def submit_application(self):
        """Submit the arrangement application."""
        self.page.locator(self.submit_button).click()

    def select_recurring_arrangement(self, is_recurring: bool):
        """Select 'Yes' or 'No' for 'Is a recurring arrangement?'."""
        recurring_section = self.page.locator(
            "div:has-text('Is a recurring arrangement?')")

        if is_recurring:
            # Find the radio button specifically for 'Yes' within the recurring arrangement section
            recurring_section.locator(
                "button[role='radio'][value='Yes']:below(:text('Is a recurring arrangement?'))").click()
        else:
            # Find the radio button specifically for 'No' within the recurring arrangement section
            recurring_section.locator(
                "button[role='radio'][value='No']:below(:text('Is a recurring arrangement?'))").click()

    def select_recurring_type(self, recurring_type: str):
        """Select the type of recurrence (e.g., 'Weekly' or 'Monthly')."""
        self.page.locator(f"button[role='radio'][value='{recurring_type}']").click()

    def select_end_date(self, end_date: str):
        """Open the date picker and select an end date for the recurring arrangement."""
        self.page.locator("button:has-text('Pick a date')").click()

        # Wait for the date picker pop-up to appear
        date_picker_popup = self.page.locator("div[role='dialog']")
        date_picker_popup.wait_for(state="visible")

        # Click on the specified end date
        date_picker_popup.locator(f"button:has-text('{end_date}')").nth(1).click()