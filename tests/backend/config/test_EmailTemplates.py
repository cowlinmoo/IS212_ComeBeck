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
    get_application_outcome_approver_email_template, get_application_outcome_employee_email_template
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