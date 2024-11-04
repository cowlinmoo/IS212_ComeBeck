from playwright.sync_api import Page
from tests.EndToEndTests.Pages.BasePage import BasePage

class ArrangementApprovalsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        # Define selectors
        self.pending_request_tab = "button[role='tab']:has-text('Pending Requests')"
        self.approved_requests_tab = "button[role='tab']:has-text('Approved')"
        self.rejected_requests_tab = "button[role='tab']:has-text('Rejected')"
        self.applications_panel = "div[data-state='active'][role='tabpanel']"
        self.first_application = "div.rounded-xl.border.bg-card"

    def navigate_to_approvals_page(self):
        """Navigate directly to the arrangement page."""
        self.navigate("https://comebeckwfhtracker.systems/approvals")

    def select_pending_requests(self):
        """Select the 'Pending Requests' tab."""
        self.page.locator(self.pending_request_tab).click()

    def select_approved_requests(self):
        """Select the 'Approved Requests' tab."""
        self.page.locator(self.approved_requests_tab).click()

    def select_rejected_requests(self):
        """Select the 'Rejected Requests' tab."""
        self.page.locator(self.rejected_requests_tab).click()

    def get_first_application_content(self):
        """Extract and dynamically format the content of the first application card."""
        # Locate the first application card
        first_card = self.page.locator(
            f"{self.applications_panel} >> {self.first_application}").first

        # Extract raw content fields
        application_id = first_card.locator("h3").inner_text()
        application_type = first_card.locator("p:text('Application Type')").inner_text()
        application_reason = first_card.locator(
            "p:text('Application Reason')").inner_text()
        approved_by = first_card.locator("p:text('Approved by')").inner_text()
        recurring_status = first_card.locator("p:text('Recurring')").inner_text()

        # List of raw text content to be split and added to the dictionary
        raw_fields = [application_id, application_type, application_reason, approved_by,
                      recurring_status]

        # Initialize the content dictionary
        content = {}

        # Split each field at the first colon to separate key and value
        for field in raw_fields:
            split_field = field.split(":", 1)  # Split at the first colon
            if len(split_field) == 2:
                key = split_field[0].strip()
                value = split_field[1].strip()
                content[key] = value
            else:
                content[
                    field] = ""  # In case there's no colon, keep the whole field as key with an empty value

        # Print the formatted content for verification
        formatted_content = "\nExtracted Application Content:\n" + "\n".join(
            [f"  {k}: {v}" for k, v in content.items()]
        )
        print(formatted_content)

        return content

    def get_first_approved_application_content(self):
        """Extract and dynamically format the content of the first application card."""
        # Locate the first application card
        first_card = self.page.locator(
            f"{self.applications_panel} >> {self.first_application}").first

        # Extract raw content fields
        application_id = first_card.locator("h3").inner_text()
        application_type = first_card.locator("p:text('Application Type')").inner_text()
        application_reason = first_card.locator(
            "p:text('Approval Reason')").inner_text()
        approved_by = first_card.locator("p:text('Approved by')").inner_text()
        recurring_status = first_card.locator("p:text('Recurring')").inner_text()

        # List of raw text content to be split and added to the dictionary
        raw_fields = [application_id, application_type, application_reason, approved_by,
                      recurring_status]

        # Initialize the content dictionary
        content = {}

        # Split each field at the first colon to separate key and value
        for field in raw_fields:
            split_field = field.split(":", 1)  # Split at the first colon
            if len(split_field) == 2:
                key = split_field[0].strip()
                value = split_field[1].strip()
                content[key] = value
            else:
                content[
                    field] = ""  # In case there's no colon, keep the whole field as key with an empty value

        # Print the formatted content for verification
        formatted_content = "\nExtracted Application Content:\n" + "\n".join(
            [f"  {k}: {v}" for k, v in content.items()]
        )
        print(formatted_content)

        return content

    def get_first_rejected_application_content(self):
        """Extract and dynamically format the content of the first application card."""
        # Locate the first application card
        first_card = self.page.locator(
            f"{self.applications_panel} >> {self.first_application}").first

        # Extract raw content fields
        application_id = first_card.locator("h3").inner_text()
        application_type = first_card.locator("p:text('Application Type')").inner_text()
        application_reason = first_card.locator(
            "p:text('Rejection Reason')").inner_text()
        approved_by = first_card.locator("p:text('Rejected by')").inner_text()
        recurring_status = first_card.locator("p:text('Recurring')").inner_text()

        # List of raw text content to be split and added to the dictionary
        raw_fields = [application_id, application_type, application_reason, approved_by,
                      recurring_status]

        # Initialize the content dictionary
        content = {}

        # Split each field at the first colon to separate key and value
        for field in raw_fields:
            split_field = field.split(":", 1)  # Split at the first colon
            if len(split_field) == 2:
                key = split_field[0].strip()
                value = split_field[1].strip()
                content[key] = value
            else:
                content[
                    field] = ""  # In case there's no colon, keep the whole field as key with an empty value

        # Print the formatted content for verification
        formatted_content = "\nExtracted Application Content:\n" + "\n".join(
            [f"  {k}: {v}" for k, v in content.items()]
        )
        print(formatted_content)

        return content
