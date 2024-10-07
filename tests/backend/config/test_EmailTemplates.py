import pytest
from datetime import date, datetime
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
    get_application_auto_rejected_employee_email_template
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
    (False, None, None, [EventCreateSchema(requested_date=date(2023, 7, 1)), EventCreateSchema(requested_date=date(2023, 7, 8))], "Multiple Dates:"),
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
    (False, None, None, [EventCreateSchema(requested_date=date(2023, 7, 1)), EventCreateSchema(requested_date=date(2023, 7, 8))], "Multiple Dates:"),
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