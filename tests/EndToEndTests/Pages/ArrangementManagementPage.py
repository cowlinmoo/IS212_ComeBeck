from asyncio import timeout

from playwright.sync_api import Page
from tests.EndToEndTests.Pages.BasePage import BasePage

class ArrangementManagementPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Define selectors
        self.arrangement_type_label = "label:text('Arrangement Type:')"
        self.submit_button = "button[type='submit']"
        self.change_tab = "button[role='tab']:has-text('Change arrangement')"

        # Change arrangement tab selectors
        self.pending_approval_radio = "button[role='radio'][value='Pending Approval']"
        self.application_table = "table"
        self.reason_textarea = "textarea[placeholder='Please provide a reason for your change request.']"
        self.withdraw_reason_textarea = "textarea[placeholder='Please provide a reason for your withdrawal/cancellation request.']"
        self.application_row_selector = "tr:has(td:text('{}'))"  # Placeholder for application ID
        self.confirm_button = "button:text('Confirm Change')"
        self.first_radio_button_in_table = "table tbody tr:first-child button[role='radio']"

        # Withdraw arrangement tab selectors
        self.withdraw_tab = "button[role='tab']:has-text('Withdraw arrangement')"
        self.withdraw_button = "button:text('Confirm Withdraw')"
    def navigate_to_arrangement_page(self):
        """Navigate directly to the arrangement page."""
        self.navigate("https://comebeckwfhtracker.systems/arrangement")

    def select_multiple_dates(self, is_multiple: bool):
        """Select 'Yes' or 'No' for 'Is this for multiple dates?'."""
        if is_multiple:
            self.page.locator("button[role='radio'][value='Yes']").click()
        else:
            self.page.locator("button[role='radio'][value='No']").click()

    def select_date(self, date_str: str):
        """Open the date picker and select a specific day."""
        # Open the date picker
        self.page.locator("button:has-text('Pick a date')").click()

        # Wait for the date picker to appear
        date_picker_popup = self.page.locator("div[role='dialog']")
        date_picker_popup.wait_for(state="visible")

        # Combine selectors to exclude disabled dates
        specific_date_locator = date_picker_popup.locator(
            f"button[role='gridcell']:has-text('{date_str}'):not([disabled])"
        )

        # Verify if the date is interactable
        if specific_date_locator.count() > 0:
            specific_date_locator.first.click()
        else:
            raise Exception(f"Date '{date_str}' is not available or is disabled.")

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
        date_picker_popup.locator(f"button:has-text('{end_date}')").click()

    def switch_to_change_tab(self):
        """Switch to the 'Change arrangement' tab."""
        self.page.locator(self.change_tab).click()

    def switch_to_withdraw_tab(self):
        """Switch to the 'Withdraw arrangement' tab."""
        self.page.locator(self.withdraw_tab).click()

    def select_pending_approval(self):
        """Ensure 'Pending Approval' radio button is selected in the change tab."""
        if not self.page.locator(self.pending_approval_radio).get_attribute("aria-checked") == "true":
            self.page.locator(self.pending_approval_radio).click()

    def select_approve(self):
        """Select the 'Approve' radio button."""
        self.page.locator("button[role='radio'][value='Approved']").click()

    def verify_application_in_table(self, application_id: str):
        """Check if the application with the given ID is in the table and select it."""
        application_row = self.page.locator(self.application_row_selector.format(application_id))
        assert application_row.is_visible(timeout=10000), f"Application ID {application_id} not found in the table."
        application_row.locator("button[role='radio']").click()

    def fill_reason_for_change(self, reason: str):
        """Fill the reason for the change request."""
        self.page.locator(self.reason_textarea).fill(reason)

    def select_first_arrangement_to_change(self):
        """Select the first available arrangement in the table."""
        self.page.locator(self.first_radio_button_in_table).click()  # Click the specific radio button in the table

    def submit_change(self):
        """Submit the change request."""
        self.page.locator(self.confirm_button).click()

    def confirm_withdraw(self):
        """Confirm the withdrawal of the arrangement."""
        self.page.locator(self.withdraw_button).click()

    def fill_reason_for_withdraw(self, reason: str):
        """Fill the reason for the withdrawal."""
        self.page.locator(self.withdraw_reason_textarea).fill(reason)
