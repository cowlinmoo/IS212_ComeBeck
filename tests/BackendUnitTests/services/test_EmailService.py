from datetime import datetime, date

import pytest
from unittest.mock import MagicMock, ANY

from fastapi import HTTPException
from pytest_mock import mocker

from backend.config.EmailTemplates import format_application_details, get_change_request_employee_email_subject, \
    get_change_request_employee_email_template, get_change_request_manager_email_subject, \
    get_change_request_manager_email_template, get_cancellation_request_manager_email_subject, \
    get_cancellation_request_manager_email_template, get_cancellation_request_employee_email_subject, \
    get_cancellation_request_employee_email_template, get_application_auto_rejected_employee_email_subject, \
    get_application_auto_rejected_employee_email_template, get_application_withdrawn_employee_email_subject, \
    get_application_withdrawn_employee_email_template, get_application_withdrawn_manager_email_subject, \
    get_application_withdrawn_manager_email_template, get_cancel_request_employee_email_template, \
    get_cancel_request_manager_email_template
from backend.models import Application, Employee, Event
from backend.models.enums.RecurrenceType import RecurrenceType
from backend.schemas.ApplicationSchema import ApplicationCreateSchema, ApplicationWithdrawSchema
from backend.services.EmailService import EmailService  # Adjust the import path as necessary


@pytest.fixture
def email_service(mocker):
    # Mock the EmployeeRepository
    mock_employee_repository = mocker.Mock()
    # Create an instance of EmailService with the mocked repository
    service = EmailService(employee_repository=mock_employee_repository)
    return service, mock_employee_repository


@pytest.mark.unit
def test_send_email_success(email_service, mocker):
    service, _ = email_service
    recipient_email = "test@example.com"
    subject = "Test Subject"
    body = "This is a test email."

    # Mock the SMTP server and its methods
    mock_smtp = mocker.patch("smtplib.SMTP")
    instance = mock_smtp.return_value.__enter__.return_value

    result = service.send_email(recipient_email, subject, body)

    # Assertions
    instance.send_message.assert_called_once()
    assert result is True


@pytest.mark.unit
def test_send_email_failure(email_service, mocker):
    service, _ = email_service
    recipient_email = "test@example.com"
    subject = "Test Subject"
    body = "This is a test email."

    # Mock the SMTP server to raise an exception
    mock_smtp = mocker.patch("smtplib.SMTP", side_effect=Exception("SMTP error"))

    result = service.send_email(recipient_email, subject, body)

    # Assertions
    assert result is False


@pytest.mark.unit
def test_send_application_creation_emails(email_service):
    service, mock_employee_repository = email_service

    # Mocking Application and Employee instances
    application = ApplicationCreateSchema(
        staff_id=1,
        application_hour="pm",  # Ensure you provide a value here
        events=[],
        recurring=False,
        reason="Test Reason",
        requested_date="2024-10-21",
        description="Test Description",
        status="pending",
        location="Test Location",
        end_date=None
    )

    new_application = Application(application_id=123, status="pending")
    manager = Employee(email="manager@example.com", staff_fname="Manager", staff_lname="Test")
    employee = Employee(email="employee@example.com", staff_fname="Employee", staff_lname="Test")
    staff_name = "Employee Test"

    # Mocking the email sending function
    service.send_email = MagicMock(return_value=True)

    service.send_application_creation_emails(application, new_application, manager, employee, staff_name)

    # Assertions
    assert service.send_email.call_count == 2  # One for manager, one for employee



@pytest.mark.unit
def test_send_outcome_emails_one_time(email_service):
    service, mock_employee_repository = email_service

    # Mocking Employee retrieval
    mock_employee_repository.get_employee.side_effect = [
        Employee(email="employee@example.com", staff_fname="Employee", staff_lname="Test"),
        Employee(email="approver@example.com", staff_fname="Approver", staff_lname="Test"),
    ]

    # Mocking the email sending function
    service.send_email = MagicMock(return_value=True)

    # Mocking Application instance with one event
    application = Application(
        application_id=123,
        staff_id=1,
        approver_id=2,
        status="approved",
        outcome_reason="Approved",
        description="Test Description",
        recurring=False,
        events=[Event(requested_date="2024-10-21", location="Test Location")]
    )

    # Call the method under test
    service.send_outcome_emails(application)

    # Assertions for one-time application
    assert service.send_email.called
    assert service.send_email.call_count == 2  # Two emails should be sent

@pytest.mark.unit
def test_send_outcome_emails_recurring(email_service):
    service, mock_employee_repository = email_service

    # Mocking Employee retrieval
    mock_employee_repository.get_employee.side_effect = [
        Employee(email="employee@example.com", staff_fname="Employee", staff_lname="Test"),
        Employee(email="approver@example.com", staff_fname="Approver", staff_lname="Test"),
    ]

    # Mocking the email sending function
    service.send_email = MagicMock(return_value=True)

    # Mocking Application instance with recurring details
    application = Application(
        application_id=124,
        staff_id=1,
        approver_id=2,
        status="approved",
        outcome_reason="Approved",
        description="Test Description",
        recurring=True,
        recurrence_type=RecurrenceType.DAILY,  # Assuming RecurrenceType is defined
        events=[Event(requested_date="2024-10-21", location="Test Location")]
    )

    # Call the method under test
    service.send_outcome_emails(application)

    # Assertions for recurring application
    assert service.send_email.called
    assert service.send_email.call_count == 2  # Two emails should be sent

@pytest.mark.unit
def test_send_outcome_emails_multiple_dates(email_service):
    service, mock_employee_repository = email_service

    # Mocking Employee retrieval
    mock_employee_repository.get_employee.side_effect = [
        Employee(email="employee@example.com", staff_fname="Employee", staff_lname="Test"),
        Employee(email="approver@example.com", staff_fname="Approver", staff_lname="Test"),
    ]

    # Mocking the email sending function
    service.send_email = MagicMock(return_value=True)

    # Mocking Application instance with multiple events
    application = Application(
        application_id=125,
        staff_id=1,
        approver_id=2,
        status="approved",
        outcome_reason="Approved",
        description="Test Description",
        recurring=False,
        events=[
            Event(requested_date="2024-10-21", location="Location 1"),
            Event(requested_date="2024-10-22", location="Location 2")
        ]
    )

    # Call the method under test
    service.send_outcome_emails(application)

    # Assertions for multiple dates application
    assert service.send_email.called
    assert service.send_email.call_count == 2  # Two emails should be sent

@pytest.mark.unit
def test_send_outcome_emails_employee_not_found(email_service):
    service, mock_employee_repository = email_service

    # Mocking Employee retrieval to return None for the employee
    mock_employee_repository.get_employee.side_effect = [
        None,  # Employee not found
        Employee(email="approver@example.com", staff_fname="Approver", staff_lname="Test"),
    ]

    application = Application(
        application_id=125,
        staff_id=1,
        approver_id=2,
        status="approved",
        outcome_reason="Approved",
        description="Test Description",
        recurring=False,
        events=[Event(requested_date="2024-10-21", location="Test Location")]
    )

    with pytest.raises(HTTPException) as exc_info:
        service.send_outcome_emails(application)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Employee or approver not found"


@pytest.mark.unit
def test_send_outcome_emails_approver_not_found(email_service):
    service, mock_employee_repository = email_service

    # Mocking Employee retrieval to return None for the approver
    mock_employee_repository.get_employee.side_effect = [
        Employee(email="employee@example.com", staff_fname="Employee", staff_lname="Test"),
        None,  # Approver not found
    ]

    application = Application(
        application_id=126,
        staff_id=1,
        approver_id=2,
        status="approved",
        outcome_reason="Approved",
        description="Test Description",
        recurring=False,
        events=[Event(requested_date="2024-10-21", location="Test Location")]
    )

    with pytest.raises(HTTPException) as exc_info:
        service.send_outcome_emails(application)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Employee or approver not found"
@pytest.mark.unit
def test_send_event_withdrawal_emails(email_service):
    service, mock_employee_repository = email_service

    # Mocking event and employee instances
    withdrawn_event = Event(event_id=1, application_id=123, requested_date="2024-10-21", location="Test Location")
    employee = Employee(email="employee@example.com", staff_fname="John", staff_lname="Doe")
    manager = Employee(email="manager@example.com", staff_fname="Jane", staff_lname="Doe")

    current_time = "2024-10-21T10:00:00Z"  # Example current time

    # Mocking the email sending function
    service.send_email = MagicMock(return_value=True)

    # Call the method under test
    service.send_event_withdrawal_emails(withdrawn_event, employee, manager, is_employee=True, current_time=current_time)

    # Assertions for emails being sent
    assert service.send_email.call_count == 2  # One for manager, one for employee

@pytest.mark.unit
def test_send_cancel_one_request_emails(email_service):
    service, mock_employee_repository = email_service

    # Mocking event and employee instances
    event = Event(event_id=1, requested_date="2024-10-21", location="Test Location")
    employee = Employee(email="employee@example.com", staff_fname="John", staff_lname="Doe")
    manager = Employee(email="manager@example.com", staff_fname="Jane", staff_lname="Doe")
    cancellation_reason = "Change of plans"

    # Mocking the email sending function
    service.send_email = MagicMock(return_value=True)

    # Call the method under test
    service.send_cancel_one_request_emails(event, employee, manager, cancellation_reason)

    # Assertions for emails being sent
    assert service.send_email.call_count == 2  # One for manager, one for employee

@pytest.mark.unit
def test_send_cancel_one_request_outcome_emails(email_service):
    service, mock_employee_repository = email_service

    # Mocking event and employee instances
    event = Event(original_event_id=1, application=Application(staff_id=1))
    outcome = "approved"

    # Mocking Employee retrieval
    mock_employee_repository.get_employee.side_effect = [
        Employee(email="employee@example.com", staff_fname="John", staff_lname="Doe"),
        Employee(email="manager@example.com", staff_fname="Jane", staff_lname="Doe"),
    ]

    # Mocking the email sending function
    service.send_email = MagicMock(return_value=True)

    # Call the method under test
    service.send_cancel_one_request_outcome_emails(event, outcome)

    # Assertions for emails being sent
    assert service.send_email.call_count == 2  # One for manager, one for employee

@pytest.mark.unit
def test_send_change_request_outcome_emails_success(email_service):
    service, mock_employee_repository = email_service

    # Mocking Employee and Manager
    employee = Employee(email="employee@example.com", staff_fname="John", staff_lname="Doe")
    manager = Employee(email="manager@example.com", staff_fname="Jane", staff_lname="Doe")

    # Mocking Employee retrieval
    mock_employee_repository.get_employee.side_effect = [employee, manager]

    # Mocking the original application
    original_application = Application(
        application_id=2,
        staff_id=employee.staff_id,
        approver_id=manager.staff_id,
        reason="Previous Reason",
        status="pending",
        outcome_reason="Pending Review",
        original_application=None  # or whatever is appropriate for your test
    )

    # Mocking the modified application
    modified_application = Application(
        application_id=1,
        staff_id=employee.staff_id,
        approver_id=manager.staff_id,
        reason="Work From Home",
        status="approved",
        outcome_reason="Change Approved",
        original_application=original_application  # Set to the mock original application
    )

    # Mocking the email sending function
    service.send_email = MagicMock(return_value=True)

    # Call the method under test
    service.send_change_request_outcome_emails(modified_application)

    # Assertions
    assert service.send_email.call_count == 2  # One for employee, one for manager
    # You can also add more assertions to check the arguments passed to send_email

@pytest.mark.unit
def test_send_change_request_outcome_emails_employee_not_found(email_service):
    service, mock_employee_repository = email_service

    # Mocking Employee retrieval to return None for the employee
    mock_employee_repository.get_employee.side_effect = [None, Employee(email="manager@example.com", staff_fname="Jane", staff_lname="Doe")]

    modified_application = Application(
        application_id=1,
        staff_id=1,
        approver_id=2,
        status="approved",
        outcome_reason="Change Approved",
        original_application=None
    )

    with pytest.raises(HTTPException) as exc_info:
        service.send_change_request_outcome_emails(modified_application)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Employee or manager not found"


@pytest.mark.unit
def test_send_change_request_outcome_emails_manager_not_found(email_service):
    service, mock_employee_repository = email_service

    # Mocking Employee retrieval to return None for the manager
    mock_employee_repository.get_employee.side_effect = [Employee(email="employee@example.com", staff_fname="John", staff_lname="Doe"), None]

    modified_application = Application(
        application_id=1,
        staff_id=1,
        approver_id=2,
        status="approved",
        outcome_reason="Change Approved",
        original_application=None
    )

    with pytest.raises(HTTPException) as exc_info:
        service.send_change_request_outcome_emails(modified_application)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Employee or manager not found"

@pytest.mark.unit
def test_send_change_request_emails(email_service):
    service, mock_employee_repository = email_service

    # Mocking Employee and Manager
    employee = Employee(email="employee@example.com", staff_fname="John", staff_lname="Doe")
    employee.staff_id = 123  # Ensure the staff_id is set
    manager = Employee(email="manager@example.com", staff_fname="Jane", staff_lname="Doe")

    # Mocking the existing and new applications
    existing_application = Application(
        application_id=1,
        staff_id=employee.staff_id,
        reason="Old Reason",
        status="pending",
        outcome_reason="Pending Review",
        original_application=None  # or whatever is appropriate for your test
    )

    new_application = Application(
        application_id=2,
        staff_id=employee.staff_id,
        reason="New Reason",
        status="approved",
        outcome_reason="Change Approved",
        original_application=None  # or whatever is appropriate for your test
    )

    # Mocking the change request with required fields
    change_request = ApplicationCreateSchema(
        reason="New Reason",
        status="approved",
        requested_date=date.today(),  # Use only the date part
        application_hour="fullday",    # Set as per the expected enum values
        staff_id=employee.staff_id,      # Ensure staff_id is set
        location= "Home",
        description="Change Request Description",
        recurring=False
    )

    current_time = datetime.now()  # You can mock this if needed

    # Mocking the email sending function
    service.send_email = MagicMock(return_value=True)

    # Call the method under test
    service.send_change_request_emails(existing_application, new_application, change_request, employee, manager, current_time)

    # Assertions
    assert service.send_email.call_count == 2  # One for employee, one for manager

    # Check calls to send_email for manager
    manager_subject = get_change_request_manager_email_subject(employee.staff_id, f"{employee.staff_fname} {employee.staff_lname}")
    manager_body = get_change_request_manager_email_template(
        manager_name=f"{manager.staff_fname} {manager.staff_lname}",
        employee_name=f"{employee.staff_fname} {employee.staff_lname}",
        employee_id=employee.staff_id,
        original_application_id=existing_application.application_id,
        new_application_id=new_application.application_id,
        original_details=format_application_details(existing_application),
        updated_details=format_application_details(change_request),
        current_time=current_time
    )
    service.send_email.assert_any_call(manager.email, manager_subject, manager_body)

    # Check calls to send_email for employee
    employee_subject = get_change_request_employee_email_subject(new_application.application_id)
    employee_body = get_change_request_employee_email_template(
        employee_name=f"{employee.staff_fname} {employee.staff_lname}",
        original_application_id=existing_application.application_id,
        new_application_id=new_application.application_id,
        original_details=format_application_details(existing_application),
        updated_details=format_application_details(change_request),
        current_time=current_time
    )
    service.send_email.assert_any_call(employee.email, employee_subject, employee_body)


@pytest.mark.unit
def test_send_cancellation_request_emails():
    # Arrange
    service = EmailService()  # Assuming this is the class containing the method

    # Mocking Employee objects
    employee = Employee(
        email="employee@example.com",
        staff_fname="John",
        staff_lname="Doe",
        staff_id=123
    )

    manager = Employee(
        email="manager@example.com",
        staff_fname="Jane",
        staff_lname="Doe"
    )

    # Mocking the existing application
    existing_application = Application(
        application_id=1,
        staff_id=employee.staff_id,
        reason="Old Reason",
        description="Application Description",
        status="pending",
        recurring=False,
        recurrence_type=None,
        end_date=None,
        events=[  # Mocking event details
            Event(requested_date=datetime(2024, 1, 15), location="Office")
        ]
    )

    # Mocking the cancellation request
    cancellation_request = ApplicationWithdrawSchema(
        withdraw_reason="Changed my mind",
        status="withdrawn",
        editor_id=employee.staff_id,
        application_id=existing_application.application_id
    )

    current_time = datetime.now()

    # Mocking the send_email method
    service.send_email = MagicMock(return_value=True)

    # Act
    service.send_cancellation_request_emails(existing_application, cancellation_request, employee, manager,
                                             current_time)

    # Assert: Check if the send_email method was called for the manager
    manager_subject = get_cancellation_request_manager_email_subject(existing_application.staff_id,
                                                                     f"{employee.staff_fname} {employee.staff_lname}")
    manager_body = get_cancellation_request_manager_email_template(
        manager_name=f"{manager.staff_fname} {manager.staff_lname}",
        employee_name=f"{employee.staff_fname} {employee.staff_lname}",
        employee_id=existing_application.staff_id,
        application_id=existing_application.application_id,
        original_reason=existing_application.reason,
        requested_date=existing_application.events[0].requested_date,
        description=existing_application.description,
        status=existing_application.status,
        created_on=current_time,
        location=existing_application.events[0].location,
        recurring=existing_application.recurring,
        recurrence_type=existing_application.recurrence_type,
        end_date=existing_application.end_date,
        cancellation_reason=cancellation_request.withdraw_reason
    )

    service.send_email.assert_any_call(manager.email, manager_subject, manager_body)

    # Assert: Check if the send_email method was called for the employee
    employee_subject = get_cancellation_request_employee_email_subject(existing_application.application_id)
    employee_body = get_cancellation_request_employee_email_template(
        employee_name=f"{employee.staff_fname} {employee.staff_lname}",
        application_id=existing_application.application_id,
        original_reason=existing_application.reason,
        requested_date=existing_application.events[0].requested_date,
        description=existing_application.description,
        status=existing_application.status,
        created_on=current_time,
        location=existing_application.events[0].location,
        recurring=existing_application.recurring,
        recurrence_type=existing_application.recurrence_type,
        end_date=existing_application.end_date,
        cancellation_reason=cancellation_request.withdraw_reason
    )

    service.send_email.assert_any_call(employee.email, employee_subject, employee_body)

    # Verify the number of email sent calls
    assert service.send_email.call_count == 2  # One for employee, one for manager


@pytest.mark.unit
def test_send_rejection_emails():
    # Arrange
    service = EmailService()  # Assuming this is the class containing the method

    # Mocking an Application object
    application = Application(
        application_id=1,
        staff_id=123,
        outcome_reason="Application not meeting requirements",
        status="rejected"
    )

    req_date = datetime.now()

    # Mocking the EmployeeRepository and Employee objects
    employee = Employee(
        email="employee@example.com",
        staff_fname="John",
        staff_lname="Doe"
    )

    service.employee_repository = MagicMock()
    service.employee_repository.get_employee = MagicMock(return_value=employee)

    # Mocking the send_email method
    service.send_email = MagicMock(return_value=True)

    # Act
    service.send_rejection_emails(application, req_date)

    # Assert
    employee_subject = get_application_auto_rejected_employee_email_subject(application.application_id)
    employee_body = get_application_auto_rejected_employee_email_template(
        employee_name=f"{employee.staff_fname} {employee.staff_lname}",
        application_id=application.application_id,
        reason=application.outcome_reason,
        status=application.status,
        date_req=req_date
    )

    service.send_email.assert_called_once_with(employee.email, employee_subject, employee_body)

@pytest.mark.unit
def test_send_withdrawal_emails():
    # Arrange
    service = EmailService()  # Assuming this is the class containing the method

    # Mocking an Application object
    withdrawn_application = Application(
        application_id=1,
        staff_id=123,
        outcome_reason="Changed my mind",
        status="withdrawn"
    )

    current_time = datetime.now()

    # Mocking Employee objects
    employee = Employee(
        email="employee@example.com",
        staff_fname="John",
        staff_lname="Doe"
    )

    editor = Employee(
        email="editor@example.com",
        staff_fname="Jane",
        staff_lname="Smith"
    )

    manager = Employee(
        email="manager@example.com",
        staff_fname="Alice",
        staff_lname="Johnson"
    )

    is_employee = True  # or False based on your test case

    # Mocking the send_email method
    service.send_email = MagicMock(return_value=True)

    # Act
    service.send_withdrawal_emails(withdrawn_application, employee, editor, manager, is_employee, current_time)

    # Assert: Check if the send_email method was called for the manager
    if manager and manager.email:
        manager_subject = get_application_withdrawn_manager_email_subject(
            withdrawn_application.staff_id, f"{employee.staff_fname} {employee.staff_lname}", is_employee
        )
        manager_body = get_application_withdrawn_manager_email_template(
            manager_name=f"{manager.staff_fname} {manager.staff_lname}",
            employee_name=f"{employee.staff_fname} {employee.staff_lname}",
            employee_id=withdrawn_application.staff_id,
            application_id=withdrawn_application.application_id,
            reason=withdrawn_application.outcome_reason,
            status=withdrawn_application.status,
            withdrawn_on=current_time,
            withdrawn_by="employee" if is_employee else "you"
        )

        service.send_email.assert_any_call(manager.email, manager_subject, manager_body)

    # Assert: Check if the send_email method was called for the employee
    employee_subject = get_application_withdrawn_employee_email_subject(
        withdrawn_application.application_id, is_employee
    )
    employee_body = get_application_withdrawn_employee_email_template(
        employee_name=f"{employee.staff_fname} {employee.staff_lname}",
        application_id=withdrawn_application.application_id,
        reason=withdrawn_application.outcome_reason,
        status=withdrawn_application.status,
        withdrawn_on=current_time,
        withdrawn_by="you" if is_employee else f"{editor.staff_fname} {editor.staff_lname}"
    )

    service.send_email.assert_any_call(employee.email, employee_subject, employee_body)

    # Verify the number of email sent calls
    assert service.send_email.call_count == (2 if manager and manager.email else 1)  # One for employee, one for manager if applicable

@pytest.mark.unit
def test_send_cancel_request_outcome_emails_with_withdrawn_status():
    # Arrange
    service = EmailService()  # Assuming this is the class containing the method

    # Mocking an Application object with initial status 'withdrawn'
    modified_application = Application(
        application_id=1,
        staff_id=123,
        approver_id=456,
        outcome_reason="Need to change my schedule",
        status="withdrawn",
        recurring=False,
        recurrence_type=None
    )

    # Mocking Employee objects
    employee = Employee(
        email="employee@example.com",
        staff_fname="John",
        staff_lname="Doe"
    )

    manager = Employee(
        email="manager@example.com",
        staff_fname="Alice",
        staff_lname="Johnson"
    )

    # Mocking the employee_repository
    service.employee_repository = MagicMock()
    service.employee_repository.get_employee = MagicMock(side_effect=[employee, manager])

    # Mocking the send_email_to_employee and send_email_to_manager methods
    service.send_email_to_employee = MagicMock(return_value=True)
    service.send_email_to_manager = MagicMock(return_value=True)

    # Act
    service.send_cancel_request_outcome_emails(modified_application)

    # Assert
    # Check if the send_email_to_employee and send_email_to_manager methods were called
    service.send_email_to_employee.assert_called_once_with(employee, modified_application, "approved", ANY)
    service.send_email_to_manager.assert_called_once_with(manager, employee, modified_application, "approved", ANY)

    # Assert that the modified_application status is still 'withdrawn'
    assert modified_application.status == "withdrawn"

@pytest.mark.unit
def test_send_cancel_request_outcome_emails_with_approved_status():
    # Arrange
    service = EmailService()  # Assuming this is the class containing the method

    # Mocking an Application object with initial status 'approved'
    modified_application = Application(
        application_id=2,
        staff_id=123,
        approver_id=456,
        outcome_reason="Changed my mind",
        status="approved",  # Start with 'approved' to test this case
        recurring=False,
        recurrence_type=None
    )

    # Mocking Employee objects
    employee = Employee(
        email="employee@example.com",
        staff_fname="John",
        staff_lname="Doe"
    )

    manager = Employee(
        email="manager@example.com",
        staff_fname="Alice",
        staff_lname="Johnson"
    )

    # Mocking the employee_repository
    service.employee_repository = MagicMock()
    service.employee_repository.get_employee = MagicMock(side_effect=[employee, manager])

    # Mocking the send_email_to_employee and send_email_to_manager methods
    service.send_email_to_employee = MagicMock(return_value=True)
    service.send_email_to_manager = MagicMock(return_value=True)

    # Act
    service.send_cancel_request_outcome_emails(modified_application)

    # Assert
    # Check if the send_email_to_employee and send_email_to_manager methods were called
    service.send_email_to_employee.assert_called_once_with(employee, modified_application, "rejected", ANY)
    service.send_email_to_manager.assert_called_once_with(manager, employee, modified_application, "rejected", ANY)

    # Assert that the modified_application status is still 'approved'
    assert modified_application.status == "approved"

@pytest.mark.unit
def test_send_email_to_employee():
    # Arrange
    service = EmailService()  # Assuming this is the class containing the method

    # Mocking an Application object
    application = Application(
        application_id=1,
        outcome_reason="Need to change my schedule",
        recurring=False,
        recurrence_type=None
    )

    employee = Employee(
        email="employee@example.com",
        staff_fname="John",
        staff_lname="Doe"
    )

    status = "approved"
    current_time = datetime.now()

    # Mocking the send_email method
    service.send_email = MagicMock(return_value=True)

    # Act
    service.send_email_to_employee(employee, application, status, current_time)

    # Assert
    subject = f"Cancel Request {status.capitalize()} for Application #{application.application_id}"
    body = get_cancel_request_employee_email_template(
        employee_name=employee.staff_fname,
        application_id=application.application_id,
        status=status,
        outcome_reason=application.outcome_reason,
        current_time=current_time,
        is_recurring=application.recurring,
        recurrence_type=application.recurrence_type.value if application.recurrence_type else None
    )

    service.send_email.assert_called_once_with(employee.email, subject, body)

@pytest.mark.unit
def test_send_email_to_manager():
    # Arrange
    service = EmailService()  # Assuming this is the class containing the method

    # Mocking an Application object
    application = Application(
        application_id=1,
        outcome_reason="Need to change my schedule",
        recurring=False,
        recurrence_type=None
    )

    employee = Employee(
        email="employee@example.com",
        staff_fname="John",
        staff_lname="Doe"
    )

    manager = Employee(
        email="manager@example.com",
        staff_fname="Alice",
        staff_lname="Johnson"
    )

    status = "approved"
    current_time = datetime.now()

    # Mocking the send_email method
    service.send_email = MagicMock(return_value=True)

    # Act
    service.send_email_to_manager(manager, employee, application, status, current_time)

    # Assert
    subject = f"Cancel Request {status.capitalize()} for {employee.staff_fname} {employee.staff_lname}"
    body = get_cancel_request_manager_email_template(
        manager_name=manager.staff_fname,
        employee_name=f"{employee.staff_fname} {employee.staff_lname}",
        application_id=application.application_id,
        status=status,
        outcome_reason=application.outcome_reason,
        current_time=current_time,
        is_recurring=application.recurring,
        recurrence_type=application.recurrence_type.value if application.recurrence_type else None
    )

    service.send_email.assert_called_once_with(manager.email, subject, body)
