import pytest
from tests.EndToEndTests.Pages.DepartmentSchedulePage import DepartmentSchedulePage
from tests.EndToEndTests.Pages.LoginPage import LoginPage
from tests.EndToEndTests.Tests.BaseTest import BaseTest

class TestDepartmentSchedule(BaseTest):

    @pytest.mark.E2ETest
    def test_department_schedule_visibility_for_specific_user(self):
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()

        # Wait for the page to fully load before interacting with it
        self.page.wait_for_load_state("networkidle")

        # Use specific credentials to log in
        username = "colinmok1000@gmail.com"
        password = "password123"
        login_page.login(username, password)

        # Wait until redirected to the schedule page and for all network requests to complete
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")
        self.page.wait_for_load_state("networkidle")

        # Assert that "Department Schedule" tab is visible
        assert login_page.is_department_schedule_visible(), "Department Schedule tab is not visible for user with department access"

    @pytest.mark.E2ETest
    def test_department_schedule_not_visible_for_other_user(self):
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        self.page.wait_for_load_state("networkidle")

        username = "colinmok3@gmail.com"
        password = "password123"
        login_page.login(username, password)
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")
        self.page.wait_for_load_state("networkidle")

        assert login_page.is_department_schedule_hidden(), "Department Schedule tab is visible for user without department access"

    @pytest.mark.E2ETest
    def test_department_schedule_table(self):
        # Expected department names and their "Total" values
        expected_data = {
            "CEO": 8,
            "Sales": 63,
            "Solutioning": 75,
            "Engineering": 246,
            "HR": 64,
            "Finance": 43,
            "Consultancy": 27,
            "IT": 28,
            "Testing": 3,
        }

        # Initialize LoginPage and perform login
        login_page = LoginPage(self.page)
        login_page.navigate_to_login()
        username = "colinmok1000@gmail.com"
        password = "password123"
        login_page.login(username, password)
        self.wait_for_url("https://comebeckwfhtracker.systems/schedule")

        # Initialize DepartmentSchedulePage and navigate to the department schedule
        dept_schedule_page = DepartmentSchedulePage(self.page)
        dept_schedule_page.navigate_to_department_schedule()

        # Wait for all network requests to complete
        self.page.wait_for_load_state("networkidle")

        # Wait for the Department Summary table to be present
        department_section = self.page.locator("div").filter(
            has=self.page.locator("h3:has-text('Department Summary')")
        )
        department_table = department_section.locator("table")

        # Ensure the table is found
        assert department_table.count() > 0, "Department Summary table not found"

        # Wait for the table rows to be present
        department_table.locator("tbody tr").first.wait_for(state='visible',
                                                            timeout=10000)

        # Get the rows from the Department Summary table
        table_rows = department_table.locator("tbody tr")

        # Loop through each department and check its "Total" value
        for department, expected_total in expected_data.items():
            # Filter the rows that have the department name in the first cell
            row = table_rows.filter(
                has=self.page.locator(f"td:nth-child(1):text('{department}')")
            ).first

            print("This is the row ",row)

            # Ensure the row is found
            assert row.count() > 0, f"Row for department '{department}' not found"

            # Select the "Total" cell (4th column)
            total_cell = row.locator("td:nth-child(4)")

            print("This is the total cell ",total_cell)
            # Ensure the "Total" cell is visible
            assert total_cell.is_visible(), f"Total cell for department '{department}' is not visible"

            # Get the total value
            total_value = int(total_cell.inner_text().strip())

            print("This is the total value ",total_value)
            # Assert the total value matches the expected value
            assert total_value == expected_total, (
                f"Total for {department} does not match. Expected: {expected_total}, Found: {total_value}"
            )

        print("All department names and total values are correct.")