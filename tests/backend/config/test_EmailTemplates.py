from collections import namedtuple
from unittest.mock import Mock

import pytest
from datetime import date, datetime

from backend.models.enums.ApplicationHourEnum import ApplicationHourEnum
from backend.schemas.EventSchema import EventCreateSchema
from backend.config.EmailTemplates import (
    get_new_application_manager_email_subject,
    get_new_application_employee_email_subject,
    get_application_withdrawn_manager_email_subject,
    get_application_withdrawn_employee_email_subject,
    get_application_auto_rejected_employee_email_subject,
    get_new_application_manager_email_template,
    get_new_application_employee_email_template,
    get_application_withdrawn_manager_email_template,
    get_application_withdrawn_employee_email_template,
    get_application_auto_rejected_employee_email_template, get_application_outcome_employee_email_subject,
    get_application_outcome_approver_email_subject, _format_event_details,
    get_application_outcome_approver_email_template, get_application_outcome_employee_email_template,
    get_change_request_employee_email_template, get_change_request_manager_email_template,
    get_change_request_employee_email_subject, get_change_request_manager_email_subject,
    get_cancel_request_manager_email_template, get_cancel_request_employee_email_template,
    get_cancellation_request_employee_email_template, get_cancellation_request_manager_email_subject,
    get_cancellation_request_employee_email_subject, get_cancellation_request_manager_email_template,
    format_application_details, get_change_request_outcome_employee_email_subject,
    get_change_request_outcome_manager_email_subject, get_event_withdrawn_manager_email_subject,
    get_event_withdrawn_employee_email_subject, get_event_cancellation_manager_email_subject,
    get_event_cancellation_employee_email_subject, get_cancel_one_request_outcome_manager_email_subject,
    get_cancel_one_request_outcome_employee_email_subject, get_cancel_one_request_outcome_manager_email_template,
    get_cancel_one_request_outcome_employee_email_template, get_change_request_outcome_employee_email_template,
    get_change_request_outcome_manager_email_template, get_event_withdrawn_manager_email_template,
    get_event_withdrawn_employee_email_template, get_event_cancellation_manager_email_template,
    get_event_cancellation_employee_email_template
)

def test_get_new_application_manager_email_subject():
    subject = get_new_application_manager_email_subject(12345, "John Doe")
    assert subject == "New Application Request from Employee ID: 12345 - John Doe"

def test_get_new_application_employee_email_subject():
    subject = get_new_application_employee_email_subject(67890)
    assert subject == "Application Submitted - Application ID: 67890"

def test_get_application_withdrawn_manager_email_subject():
    subject = get_application_withdrawn_manager_email_subject(12345, "John Doe", True)
    assert subject == "Application Withdrawn for Employee ID: 12345 - John Doe"

    subject = get_application_withdrawn_manager_email_subject(12345, "John Doe", False)
    assert subject == "Application Cancelled for Employee ID: 12345 - John Doe"

def test_get_application_withdrawn_employee_email_subject():
    subject = get_application_withdrawn_employee_email_subject(67890, True)
    assert subject == "WITHDRAWN: Application withdrawn - Application ID: 67890"

    subject = get_application_withdrawn_employee_email_subject(67890, False)
    assert subject == "CANCELLED: Application cancelled - Application ID: 67890"

def test_get_application_auto_rejected_employee_email_subject():
    subject = get_application_auto_rejected_employee_email_subject(67890)
    assert subject == "REJECTED: Application Auto Rejected - Application ID: 67890"

def test_get_new_application_manager_email_template():
    template = get_new_application_manager_email_template(
        manager_name="Jane Smith",
        employee_name="John Doe",
        employee_id=12345,
        application_id=67890,
        reason="Vacation",
        requested_date=date(2023, 7, 1),
        description="Summer vacation",
        status="Pending",
        created_on=date(2023, 6, 1),
        location="Hawaii"
    )
    assert "Dear Jane Smith," in template
    assert "Employee Name: John Doe" in template
    assert "Employee ID: 12345" in template
    assert "Application ID: 67890" in template
    assert "Reason: Vacation" in template
    assert "Requested Date: 2023-07-01" in template
    assert "Description: Summer vacation" in template
    assert "Status: Pending" in template
    assert "Submission Date: 2023-06-01" in template
    assert "Location: Hawaii" in template

def test_get_new_application_employee_email_template():
    template = get_new_application_employee_email_template(
        employee_name="John Doe",
        application_id=67890,
        reason="Vacation",
        requested_date=date(2023, 7, 1),
        description="Summer vacation",
        status="Pending",
        created_on=date(2023, 6, 1),
        location="Hawaii"
    )
    assert "Dear John Doe," in template
    assert "Application ID: 67890" in template
    assert "Reason: Vacation" in template
    assert "Requested Date: 2023-07-01" in template
    assert "Description: Summer vacation" in template
    assert "Status: Pending" in template
    assert "Submission Date: 2023-06-01" in template
    assert "Location: Hawaii" in template

def test_get_application_withdrawn_manager_email_template():
    template = get_application_withdrawn_manager_email_template(
        manager_name="Jane Smith",
        employee_name="John Doe",
        employee_id=12345,
        application_id=67890,
        reason="Vacation",
        status="Withdrawn",
        withdrawn_on=datetime(2023, 6, 15, 10, 30),
        withdrawn_by="employee"
    )
    assert "Dear Jane Smith," in template
    assert "Employee Name: John Doe" in template
    assert "Employee ID: 12345" in template
    assert "Application ID: 67890" in template
    assert "Reason: Vacation" in template
    assert "Status: Withdrawn" in template
    assert "Withdrawn On: 2023-06-15 10:30:00" in template
    assert "Withdrawn By: Employee" in template

def test_get_application_withdrawn_employee_email_template():
    template = get_application_withdrawn_employee_email_template(
        employee_name="John Doe",
        application_id=67890,
        reason="Vacation",
        status="Withdrawn",
        withdrawn_on=datetime(2023, 6, 15, 10, 30),
        withdrawn_by="you"
    )
    assert "Dear John Doe," in template
    assert "Application ID: 67890" in template
    assert "Reason: Vacation" in template
    assert "Status: Withdrawn" in template
    assert "Withdrawn On: 2023-06-15 10:30:00" in template
    assert "Withdrawn By: You" in template

def test_get_application_auto_rejected_employee_email_template():
    template = get_application_auto_rejected_employee_email_template(
        employee_name="John Doe",
        application_id=67890,
        reason="Vacation",
        status="Auto Rejected",
        date_req=datetime(2023, 4, 1, 9, 0)
    )
    assert "Dear John Doe," in template
    assert "Application ID: 67890" in template
    assert "Reason: Vacation" in template
    assert "Status: Auto Rejected" in template
    assert "Date Requested: 2023-04-01 09:00:00" in template
    assert "auto rejected as 2 months has passed" in template

@pytest.mark.parametrize("recurring,recurrence_type,end_date,events,expected_text", [
    (True, "Weekly", date(2023, 7, 31), None, "Recurrence Type: Weekly"),
    (False, None, None, [EventCreateSchema(requested_date=date(2023, 7, 1), application_hour=ApplicationHourEnum.FULLDAY), EventCreateSchema(requested_date=date(2023, 7, 8), application_hour=ApplicationHourEnum.FULLDAY)], "Multiple Dates:"),
    (False, None, None, None, "Requested Date: 2023-07-01"),
])
def test_get_new_application_manager_email_template_variations(recurring, recurrence_type, end_date, events, expected_text):
    template = get_new_application_manager_email_template(
        manager_name="Jane Smith",
        employee_name="John Doe",
        employee_id=12345,
        application_id=67890,
        reason="Vacation",
        requested_date=date(2023, 7, 1),
        description="Summer vacation",
        status="Pending",
        created_on=date(2023, 6, 1),
        location="Hawaii",
        recurring=recurring,
        recurrence_type=recurrence_type,
        end_date=end_date,
        events=events
    )
    assert expected_text in template

@pytest.mark.parametrize("recurring,recurrence_type,end_date,events,expected_text", [
    (True, "Weekly", date(2023, 7, 31), None, "Recurrence Type: Weekly"),
    (False, None, None, [EventCreateSchema(requested_date=date(2023, 7, 1), application_hour=ApplicationHourEnum.FULLDAY), EventCreateSchema(requested_date=date(2023, 7, 8), application_hour=ApplicationHourEnum.FULLDAY)], "Multiple Dates:"),
    (False, None, None, None, "Requested Date: 2023-07-01"),
])
def test_get_new_application_employee_email_template_variations(recurring, recurrence_type, end_date, events, expected_text):
    template = get_new_application_employee_email_template(
        employee_name="John Doe",
        application_id=67890,
        reason="Vacation",
        requested_date=date(2023, 7, 1),
        description="Summer vacation",
        status="Pending",
        created_on=date(2023, 6, 1),
        location="Hawaii",
        recurring=recurring,
        recurrence_type=recurrence_type,
        end_date=end_date,
        events=events
    )
    assert expected_text in template

def test_get_application_outcome_employee_email_subject():
    assert get_application_outcome_employee_email_subject(12345, "approved") == "Application APPROVED - ID: 12345"
    assert get_application_outcome_employee_email_subject(67890, "rejected") == "Application REJECTED - ID: 67890"

def test_get_application_outcome_approver_email_subject():
    assert get_application_outcome_approver_email_subject(12345, "approved", "John Doe") == "Confirmation: Application APPROVED - ID: 12345 - John Doe"
    assert get_application_outcome_approver_email_subject(67890, "rejected", "Jane Smith") == "Confirmation: Application REJECTED - ID: 67890 - Jane Smith"


def test_get_application_outcome_employee_email_template():
    template = get_application_outcome_employee_email_template(
        employee_name="John Doe",
        application_id=12345,
        status="approved",
        reason="Valid request",
        description="Time off request",
        decided_on=datetime(2023, 7, 1, 10, 0),
        decided_by="Manager",
        app_type="one_time",
        event_info={"date": "2023-08-01", "location": "Office"}
    )

    assert "Dear John Doe," in template
    assert "Application ID: 12345" in template
    assert "Status: APPROVED" in template
    assert "Reason: Valid request" in template
    assert "Description: Time off request" in template
    assert "Decision made on: 2023-07-01 10:00:00" in template
    assert "Decision made by: Manager" in template  # Changed from "Decided by: Manager"
    assert "Date: 2023-08-01" in template
    assert "Location: Office" in template
    assert "This email is to inform you that a decision has been made regarding your application." in template
    assert "If you have any questions about this decision, please contact your manager or the HR department." in template
    assert "Thank you for using our application system." in template
    assert "Best regards," in template
    assert "HR Department" in template
    assert "This is an automated message. Please do not reply directly to this email." in template


def test_get_application_outcome_approver_email_template():
    template = get_application_outcome_approver_email_template(
        approver_name="Jane Smith",
        employee_name="John Doe",
        employee_id="EMP001",
        application_id=12345,
        status="rejected",
        reason="Insufficient staff",
        description="Time off request",
        decided_on=datetime(2023, 7, 1, 10, 0),
        app_type="one_time",
        event_info={"date": "2023-08-01", "location": "Office"}
    )

    assert "Dear Jane Smith," in template
    assert "Application ID: 12345" in template
    assert "Employee: John Doe (ID: EMP001)" in template
    assert "Status: REJECTED" in template
    assert "Reason for rejection: Insufficient staff" in template
    assert "Description: Time off request" in template
    assert "Decision made on: 2023-07-01 10:00:00" in template
    assert "Date: 2023-08-01" in template
    assert "Location: Office" in template


@pytest.mark.parametrize("app_type,event_info,expected_output", [
    (
        "recurring",
        {"recurrence_type": "Weekly", "start_date": "2023-08-01", "end_date": "2023-08-31"},
        """
Recurring Application Details:
------------------------------
Recurrence Type: Weekly
Start Date: 2023-08-01
End Date: 2023-08-31
        """
    ),
    (
        "multiple_dates",
        [{"date": "2023-08-01", "location": "Office"}, {"date": "2023-08-15", "location": "Home"}],
        """
Multiple Dates Application:
Event 1: Date: 2023-08-01, Location: Office
Event 2: Date: 2023-08-15, Location: Home
        """
    ),
    (
        "one_time",
        {"date": "2023-08-01", "location": "Office"},
        """
Application Details:
--------------------
Date: 2023-08-01
Location: Office
        """
    )
])
def test_format_event_details(app_type, event_info, expected_output):
    assert _format_event_details(app_type, event_info).strip() == expected_output.strip()

def test_get_cancellation_request_manager_email_subject():
    assert get_cancellation_request_manager_email_subject(12345, "John Doe") == "Cancellation Request for Employee ID: 12345 - John Doe"

def test_get_cancellation_request_employee_email_subject():
    assert get_cancellation_request_employee_email_subject(67890) == "Cancellation Request Submitted - Application ID: 67890"

def test_get_cancellation_request_manager_email_template():
    result = get_cancellation_request_manager_email_template(
        manager_name="Jane Smith",
        employee_name="John Doe",
        employee_id=12345,
        application_id=67890,
        original_reason="Vacation",
        requested_date=date(2023, 7, 15),
        description="Summer vacation",
        status="Approved",
        created_on=datetime(2023, 7, 1, 10, 30),
        location="New York",
        recurring=False,
        cancellation_reason="Change of plans"
    )
    assert "Dear Jane Smith" in result
    assert "Employee Name: John Doe" in result
    assert "Employee ID: 12345" in result
    assert "Application ID: 67890" in result
    assert "Reason for Cancellation: Change of plans" in result
    assert "Date: 2023-07-15" in result
def test_get_cancellation_request_manager_email_template_recurring():
    result = get_cancellation_request_manager_email_template(
        manager_name="Robert Johnson",
        employee_name="Alice Brown",
        employee_id=54321,
        application_id=98765,
        original_reason="Weekly Team Meeting",
        requested_date=date(2023, 8, 1),
        description="Team sync-up",
        status="Approved",
        created_on=datetime(2023, 7, 25, 14, 45),
        location="Conference Room A",
        recurring=True,
        recurrence_type="Weekly",
        end_date=date(2023, 12, 31),
        cancellation_reason="Schedule conflict"
    )
    assert "Dear Robert Johnson" in result
    assert "Employee Name: Alice Brown" in result
    assert "Employee ID: 54321" in result
    assert "Application ID: 98765" in result
    assert "Reason for Cancellation: Schedule conflict" in result
    assert "Recurring Details:" in result
    assert "Recurrence Type: Weekly" in result
    assert "Start Date: 2023-08-01" in result
    assert "End Date: 2023-12-31" in result

def test_get_cancellation_request_employee_email_template():
    result = get_cancellation_request_employee_email_template(
        employee_name="John Doe",
        application_id=67890,
        original_reason="Vacation",
        requested_date=date(2023, 7, 15),
        description="Summer vacation",
        status="Approved",
        created_on=datetime(2023, 7, 1, 10, 30),
        location="New York",
        recurring=False,
        cancellation_reason="Change of plans"
    )
    assert "Dear John Doe" in result
    assert "Application ID: 67890" in result
    assert "Reason for Cancellation: Change of plans" in result
    assert "Date: 2023-07-15" in result

def test_get_cancel_request_employee_email_template():
    result = get_cancel_request_employee_email_template(
        employee_name="John Doe",
        application_id=67890,
        status="approved",
        outcome_reason="",
        current_time=datetime(2023, 7, 2, 14, 30),
        is_recurring=False,
        recurrence_type=None
    )
    assert "Dear John Doe" in result
    assert "Application ID: 67890" in result
    assert "has been approved" in result
    assert "This is a one-time application." in result


def test_get_cancel_request_employee_email_template_rejected():
    result = get_cancel_request_employee_email_template(
        employee_name="John Doe",
        application_id=67890,
        status="rejected",
        outcome_reason="",
        current_time=datetime(2023, 7, 2, 14, 30),
        is_recurring=False,
        recurrence_type=None
    )
    assert "Dear John Doe" in result
    assert "Application ID: 67890" in result
    assert "has been rejected" in result
    assert "This is a one-time application." in result

def test_get_cancellation_request_employee_email_template_recurring():
    result = get_cancellation_request_employee_email_template(
        employee_name="Alice Brown",
        application_id=98765,
        original_reason="Weekly Team Meeting",
        requested_date=date(2023, 8, 1),
        description="Team sync-up",
        status="Approved",
        created_on=datetime(2023, 7, 25, 14, 45),
        location="Conference Room A",
        recurring=True,
        recurrence_type="Weekly",
        end_date=date(2023, 12, 31),
        cancellation_reason="Schedule conflict"
    )
    assert "Dear Alice Brown" in result
    assert "Application ID: 98765" in result
    assert "Status: Approved" in result
    assert "Location: Conference Room A" in result
    assert "Reason: Weekly Team Meeting" in result
    assert "Description: Team sync-up" in result
    assert "Recurring Details:" in result
    assert "Recurrence Type: Weekly" in result
    assert "Start Date: 2023-08-01" in result
    assert "End Date: 2023-12-31" in result
    assert "Reason for Cancellation: Schedule conflict" in result
    assert "Submission Date of Cancellation Request: 2023-07-25 14:45:00" in result
def test_get_cancel_request_manager_email_template():
    result = get_cancel_request_manager_email_template(
        manager_name="Jane Smith",
        employee_name="John Doe",
        application_id=67890,
        status="rejected",
        outcome_reason="Insufficient staffing",
        current_time=datetime(2023, 7, 2, 14, 30),
        is_recurring=True,
        recurrence_type="weekly"
    )
    assert "Dear Jane Smith" in result
    assert "Employee: John Doe" in result
    assert "Application ID: 67890" in result
    assert "have rejected the cancellation request" in result
    assert "This is a recurring application with weekly recurrence." in result
    assert "Reason for rejection: Insufficient staffing" in result

def test_get_change_request_manager_email_subject():
    assert get_change_request_manager_email_subject(12345, "John Doe") == "Change Request for Application from 12345 - John Doe"

def test_get_change_request_employee_email_subject():
    assert get_change_request_employee_email_subject(67890) == "Change Request Submitted for Application ID: 67890"

def test_get_change_request_manager_email_template():
    result = get_change_request_manager_email_template(
        manager_name="Jane Smith",
        employee_name="John Doe",
        employee_id=12345,
        original_application_id=67890,
        new_application_id=67891,
        original_details="Original details",
        updated_details="Updated details",
        current_time=datetime(2023, 7, 3, 9, 0)
    )
    assert "Dear Jane Smith" in result
    assert "Employee: John Doe (ID: 12345)" in result
    assert "New Application ID: 67891" in result
    assert "Original Application ID: 67890" in result
    assert "Updated Application Details:" in result
    assert "Original Application Details:" in result

def test_get_change_request_employee_email_template():
    result = get_change_request_employee_email_template(
        employee_name="John Doe",
        original_application_id=67890,
        new_application_id=67891,
        original_details="Original details",
        updated_details="Updated details",
        current_time=datetime(2023, 7, 3, 9, 0)
    )
    assert "Dear John Doe" in result
    assert "New Application ID: 67891" in result
    assert "Original Application ID: 67890" in result
    assert "Updated Application Details:" in result
    assert "Original Application Details:" in result

def test_format_application_details_basic():
    application = Mock(
        reason="Vacation",
        description="Annual leave",
        recurring=False,
        location="Beach",
        requested_date="2023-07-01",
        events=[]  # Ensure `events` is iterable
    )
    expected_output = (
        "Reason: Vacation\n"
        "Description: Annual leave\n"
        "Recurring: No\n"
        "Location: Beach\n"
        "Requested Date: 2023-07-01"
    )
    assert format_application_details(application) == expected_output


def test_format_application_details_no_description():
    # Mock the required attributes only (without location or requested_date)
    application = Mock(reason="Meeting", description=None, recurring=False)
    application.configure_mock(location=None, requested_date=None, events=[])

    expected_output = (
        "Reason: Meeting\n"
        "Description: N/A\n"
        "Recurring: No\n"
        "No location or event information available."
    )

    # Call the function and compare the result
    assert format_application_details(application) == expected_output


@pytest.fixture
def mock_application():
    return Mock(spec=['reason', 'description', 'recurring', 'recurrence_type', 'end_date', 'events'])


def test_format_application_details_recurring(mock_application, monkeypatch):
    mock_application.reason = "Team Meeting"
    mock_application.description = "Weekly sync"
    mock_application.recurring = True
    mock_application.recurrence_type = "WEEKLY"
    mock_application.end_date = "2023-12-31"
    mock_application.events = []

    def mock_hasattr(obj, attr):
        return attr in ['reason', 'description', 'recurring', 'recurrence_type', 'end_date', 'events']

    monkeypatch.setattr('builtins.hasattr', mock_hasattr)

    expected_output = (
        "Reason: Team Meeting\n"
        "Description: Weekly sync\n"
        "Recurring: Yes\n"
        "Recurrence Type: WEEKLY\n"
        "End Date: 2023-12-31"
    )
    assert format_application_details(mock_application) == expected_output


def test_format_application_details_recurring_with_events(mock_application, monkeypatch):
    mock_application.reason = "Team Meeting"
    mock_application.description = "Weekly sync"
    mock_application.recurring = True
    mock_application.recurrence_type = "WEEKLY"
    mock_application.end_date = "2023-12-31"

    # Create a mock event
    first_event = Mock(location="Conference Room", requested_date="2023-07-01")

    # Set up events as a list with a single event
    mock_application.events = [first_event]

    def mock_hasattr(obj, attr):
        return attr in ['reason', 'description', 'recurring', 'recurrence_type', 'end_date', 'events']

    monkeypatch.setattr('builtins.hasattr', mock_hasattr)

    expected_output = (
        "Reason: Team Meeting\n"
        "Description: Weekly sync\n"
        "Recurring: Yes\n"
        "Location: Conference Room\n"
        "Requested Date: 2023-07-01\n"
        "Recurrence Type: WEEKLY\n"
        "End Date: 2023-12-31"
    )
    assert format_application_details(mock_application) == expected_output


def test_format_application_details_non_recurring_with_events(mock_application, monkeypatch):
    mock_application.reason = "Conference"
    mock_application.description = "Annual conference"
    mock_application.recurring = False
    mock_application.events = [
        Mock(requested_date="2023-07-01"),
        Mock(requested_date="2023-07-02")
    ]

    def mock_hasattr(obj, attr):
        return attr in ['reason', 'description', 'recurring', 'events']

    monkeypatch.setattr('builtins.hasattr', mock_hasattr)

    expected_output = (
        "Reason: Conference\n"
        "Description: Annual conference\n"
        "Recurring: No\n"
        "\nEvents:\n"
        "- Date: 2023-07-01\n"
        "- Date: 2023-07-02"
    )
    assert format_application_details(mock_application) == expected_output

def test_change_request_outcome_employee_email():
    result = get_change_request_outcome_employee_email_subject(12345, "approved")
    assert result == "Change Request Approved - ID: 12345"

    result = get_change_request_outcome_employee_email_subject(67890, "rejected")
    assert result == "Change Request Rejected - ID: 67890"
def test_get_change_request_outcome_employee_email_template():
    # Arrange
    employee_name = "John Doe"
    application_id = 12345
    status = "approved"
    outcome_reason = "Valid request"
    current_time = datetime(2023, 7, 1, 12, 0)
    original_details = "Original details here"
    updated_details = "Updated details here"

    # Act
    result = get_change_request_outcome_employee_email_template(
        employee_name,
        application_id,
        status,
        outcome_reason,
        current_time,
        original_details,
        updated_details
    )

    # Assert
    expected_output = f"""\
Dear John Doe,

Your change request for Application ID: 12345 has been approved.

Status: Approved
Reason: Valid request
Decision Time: 2023-07-01 12:00:00

Updated Application Details:
----------------------------
Updated details here

Original Application Details:
-----------------------------
Original details here

If you have any questions, please contact your manager.

Best regards,
HR Department"""

    # Remove all whitespace and compare
    assert ''.join(result.split()) == ''.join(expected_output.split())

    # Test for rejected status
    result_rejected = get_change_request_outcome_employee_email_template(
        employee_name, application_id, "rejected", outcome_reason,
        current_time, original_details, updated_details
    )
    assert "Note: The original approved application remains valid." in result_rejected
def test_get_change_request_outcome_manager_email_template():
    # Arrange
    manager_name = "Jane Smith"
    employee_name = "John Doe"
    application_id = 12345
    status = "approved"
    outcome_reason = "Valid request"
    current_time = datetime(2023, 7, 1, 12, 0)
    original_details = "Original details here"
    updated_details = "Updated details here"

    # Act
    result = get_change_request_outcome_manager_email_template(
        manager_name,
        employee_name,
        application_id,
        status,
        outcome_reason,
        current_time,
        original_details,
        updated_details
    )

    # Assert
    expected_output = f"""\
Dear Jane Smith,

The change request for John Doe's Application ID: 12345 has been approved.

Status: Approved
Reason: Valid request
Decision Time: 2023-07-01 12:00:00

Employee: John Doe
Application ID: 12345

Updated Application Details:
----------------------------
Updated details here

Original Application Details:
----------------------------
Original details here

Best regards,
HR Department"""

    # Remove all whitespace and compare
    assert ''.join(result.split()) == ''.join(expected_output.split())

    # Test with different status
    result_rejected = get_change_request_outcome_manager_email_template(
        manager_name, employee_name, application_id, "rejected", outcome_reason,
        current_time, original_details, updated_details
    )
    assert "has been rejected" in result_rejected
    assert "Status: Rejected" in result_rejected

    # Test with different inputs
    result_different = get_change_request_outcome_manager_email_template(
        "Manager2", "Employee2", 54321, "pending", "Under review",
        datetime(2023, 8, 1, 9, 0), "Old details", "New details"
    )
    assert "Dear Manager2," in result_different
    assert "Employee2's Application ID: 54321" in result_different
    assert "Status: Pending" in result_different
    assert "Reason: Under review" in result_different
    assert "Decision Time: 2023-08-01 09:00:00" in result_different
    assert "Old details" in result_different
    assert "New details" in result_different
def test_change_request_outcome_manager_email():
    result = get_change_request_outcome_manager_email_subject("John", "approved")
    assert result == f"Change Request Approved for John"

    result = get_change_request_outcome_manager_email_subject("John", "rejected")
    assert result == f"Change Request Rejected for John"

def test_event_withdrawal_manager_email():
    result = get_event_withdrawn_manager_email_subject(12345, 1)
    assert result == "Event Withdrawn - Event ID: 12345 (Application ID: 1)"

def test_event_withdrawal_employee_email():
    result = get_event_withdrawn_employee_email_subject(12345, 1)
    assert result == "Event Withdrawal Confirmation - Event ID: 12345"


def test_event_cancellation_manager_email_subject():
    result = get_event_cancellation_manager_email_subject(12345, "John Doe")
    assert result == "Event Cancellation Request - Event ID: 12345 - John Doe"


def test_event_cancellation_employee_email_subject():
    result = get_event_cancellation_employee_email_subject(12345)
    assert result == "Event Cancellation Submitted - Event ID: 12345"

def test_cancel_one_request_outcome_manager_email_subject():
    result = get_cancel_one_request_outcome_manager_email_subject(12345, "approved")
    assert result == "Cancellation Request Approved - Event ID: 12345"
    result = get_cancel_one_request_outcome_manager_email_subject(12345, "rejected")
    assert result == "Cancellation Request Rejected - Event ID: 12345"

def test_cancel_one_request_outcome_employee_email_subject():
    result = get_cancel_one_request_outcome_employee_email_subject(12345, "approved")
    assert result == "Cancellation Request Approved - Event ID: 12345"
    result = get_cancel_one_request_outcome_employee_email_subject(12345, "rejected")
    assert result == "Cancellation Request Rejected - Event ID: 12345"

def test_cancel_one_request_outcome_manager_email_template():
    result = get_cancel_one_request_outcome_manager_email_template("Jane Smith", "John Doe", 12345, "approved",
                                                                   datetime.now())
    assert "Dear Jane Smith" in result
    assert "Employee Name: John Doe" in result
    assert "Event ID: 12345" in result
    assert "approved" in result
    assert "Date and Time:" in result
    assert "Please contact the HR department if you have any questions." in result
    assert "HR Department" in result
    assert "This is an automated message. Please do not reply directly to this email." in result

def test_cancel_one_request_outcome_employee_email_template():
    result = get_cancel_one_request_outcome_employee_email_template("John Doe", 12345, "approved",
                                                                    datetime.now())
    assert "Dear John Doe" in result
    assert "Event ID: 12345" in result
    assert "approved" in result
    assert "Date and Time:" in result
    assert "Please contact your manager if you have any questions." in result
    assert "HR Department" in result
    assert "This is an automated message. Please do not reply directly to this email." in result

def test_get_event_withdrawn_manager_email_template():
    # Arrange
    manager_name = "Jane Smith"
    employee_name = "John Doe"
    event_id = 1001
    application_id = 5001
    requested_date = date(2023, 7, 15)
    location = "Conference Room A"
    withdrawn_on = datetime(2023, 7, 1, 14, 30)
    withdrawn_by = "John Doe"

    # Act
    result = get_event_withdrawn_manager_email_template(
        manager_name, employee_name, event_id, application_id,
        requested_date, location, withdrawn_on, withdrawn_by
    )

    # Assert
    expected_content = [
        f"Dear {manager_name},",
        "This is to inform you that an event associated with an application has been withdrawn.",
        f"Employee Name: {employee_name}",
        f"Event ID: {event_id}",
        f"Application ID: {application_id}",
        f"Requested Date: {requested_date}",
        f"Location: {location}",
        f"Withdrawn On: {withdrawn_on}",
        f"Withdrawn By: {withdrawn_by}",
        "If you have any questions regarding this withdrawal, please contact the HR department.",
        "Best regards,",
        "HR Department",
        "This is an automated message. Please do not reply directly to this email."
    ]

    for content in expected_content:
        assert content in result

def test_get_event_withdrawn_employee_email_template():
    # Arrange
    employee_name = "John Doe"
    event_id = 1001
    application_id = 5001
    requested_date = date(2023, 7, 15)
    location = "Conference Room A"
    withdrawn_on = datetime(2023, 7, 1, 14, 30)
    withdrawn_by = "John Doe"

    # Act
    result = get_event_withdrawn_employee_email_template(
        employee_name, event_id, application_id,
        requested_date, location, withdrawn_on, withdrawn_by
    )

    # Assert
    expected_content = [
        f"Dear {employee_name},",
        "This email confirms that your event has been withdrawn.",
        f"Event ID: {event_id}",
        f"Application ID: {application_id}",
        f"Requested Date: {requested_date}",
        f"Location: {location}",
        f"Withdrawn On: {withdrawn_on}",
        f"Withdrawn By: {withdrawn_by}",
        "If you need to submit a new event or have any questions, please contact the HR department.",
        "Thank you for using our application system.",
        "Best regards,",
        "HR Department",
        "This is an automated message. Please do not reply directly to this email."
    ]

    for content in expected_content:
        assert content in result

def test_get_event_cancellation_manager_email_template():
    # Arrange
    manager_name = "Jane Smith"
    employee_name = "John Doe"
    employee_id = 12345
    event_id = 1001
    requested_date = date(2023, 7, 15)
    location = "Conference Room A"
    cancellation_reason = "Scheduling conflict"
    current_time = datetime(2023, 7, 1, 14, 30)

    # Act
    result = get_event_cancellation_manager_email_template(
        manager_name, employee_name, employee_id, event_id,
        requested_date, location, cancellation_reason, current_time
    )

    # Assert
    expected_content = [
        f"Dear {manager_name},",
        f"An event cancellation request has been submitted by {employee_name}.",
        f"Employee Name: {employee_name}",
        f"Employee ID: {employee_id}",
        f"Event ID: {event_id}",
        f"Requested Date: {requested_date}",
        f"Location: {location}",
        f"Cancellation Reason: {cancellation_reason}",
        f"Submission Date and Time: {current_time}",
        "Please review this cancellation request and take appropriate action.",
        "Best regards,",
        "HR Department",
        "This is an automated message. Please do not reply directly to this email."
    ]

    for content in expected_content:
        assert content in result

    # Test with no cancellation reason
    result_no_reason = get_event_cancellation_manager_email_template(
        manager_name, employee_name, employee_id, event_id,
        requested_date, location, "", current_time
    )
    assert "Cancellation Reason: No reason provided" in result_no_reason

def test_get_event_cancellation_employee_email_template():
    # Arrange
    employee_name = "John Doe"
    event_id = 1001
    requested_date = date(2023, 7, 15)
    location = "Conference Room A"
    cancellation_reason = "Scheduling conflict"
    current_time = datetime(2023, 7, 1, 14, 30)

    # Act
    result = get_event_cancellation_employee_email_template(
        employee_name, event_id, requested_date, location,
        cancellation_reason, current_time
    )

    # Assert
    expected_content = [
        f"Dear {employee_name},",
        "Your event cancellation request has been submitted successfully.",
        f"Event ID: {event_id}",
        f"Requested Date: {requested_date}",
        f"Location: {location}",
        f"Cancellation Reason: {cancellation_reason}",
        f"Submission Date and Time: {current_time}",
        "Your request will be reviewed by your manager. You will be notified of any updates.",
        "If you have any questions, please contact the HR department.",
        "Best regards,",
        "HR Department",
        "This is an automated message. Please do not reply directly to this email."
    ]

    for content in expected_content:
        assert content in result

    # Test with no cancellation reason
    result_no_reason = get_event_cancellation_employee_email_template(
        employee_name, event_id, requested_date, location, "", current_time
    )
    assert "Cancellation Reason: No reason provided" in result_no_reason