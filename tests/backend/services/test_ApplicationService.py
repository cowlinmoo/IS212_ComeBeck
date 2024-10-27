import pytest
from datetime import datetime, timedelta, date
from unittest.mock import Mock, patch, create_autospec, ANY
from fastapi import HTTPException
from dateutil.relativedelta import relativedelta

from backend.models import Event
from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.models.enums.ApplicationHourEnum import ApplicationHourEnum
from backend.models.generators import get_current_datetime_sgt
from backend.schemas.EventSchema import EventCreateSchema
from backend.services.ApplicationService import ApplicationService
from backend.models.enums.RecurrenceType import RecurrenceType
from backend.models import Application, Event, Employee
from backend.schemas.ApplicationSchema import ApplicationCreateSchema,  \
    ApplicationWithdrawSchema, ApplicationApproveRejectSchema, ApplicationWithdrawEventSchema


@pytest.fixture
def mock_application_repository():
    return Mock()


@pytest.fixture
def mock_employee_repository():
    return Mock()


@pytest.fixture
def mock_email_service():
    return Mock()


@pytest.fixture
def mock_event_repository():
    return Mock()


@pytest.fixture
def mock_event_service():
    return Mock()


@pytest.fixture
def application_service(mock_application_repository, mock_employee_repository, mock_email_service,
                        mock_event_repository, mock_event_service):
    return ApplicationService(
        application_repository=mock_application_repository,
        employee_repository=mock_employee_repository,
        email_service=mock_email_service,
        event_repository=mock_event_repository,
        event_service=mock_event_service
    )


def test_get_all_applications(application_service, mock_application_repository):
    mock_application_repository.get_all_applications.return_value = [Mock(Application), Mock(Application)]
    result = application_service.get_all_applications()
    assert len(result) == 2
    mock_application_repository.get_all_applications.assert_called_once()


def test_get_application_by_id_success(application_service, mock_application_repository):
    # Create a mock application
    mock_application = Mock(spec=Application)

    # Set up the mock repository to return the mock application
    mock_application_repository.get_application_by_application_id.return_value = mock_application

    # Call the method we're testing
    result = application_service.get_application_by_id(1)

    # Assert that the method returns the expected application
    assert result == mock_application

    # Optionally, assert that the repository method was called with the correct argument
    mock_application_repository.get_application_by_application_id.assert_called_with(1)


def test_get_application_by_id_not_found(application_service, mock_application_repository):
    mock_application_repository.get_application_by_application_id.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        application_service.get_application_by_id(1)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Application not found"


def test_get_applications_by_staff_id_success(application_service, mock_application_repository,
                                              mock_employee_repository):
    mock_employee_repository.get_employee.return_value = Mock(Employee)
    mock_application_repository.get_application_by_staff_id.return_value = [Mock(Application), Mock(Application)]
    result = application_service.get_applications_by_staff_id(1)
    assert len(result) == 2
    mock_employee_repository.get_employee.assert_called_once_with(1)
    mock_application_repository.get_application_by_staff_id.assert_called_once_with(1)


def test_get_applications_by_staff_id_employee_not_found(application_service, mock_employee_repository):
    mock_employee_repository.get_employee.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        application_service.get_applications_by_staff_id(1)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Employee not found"

@patch('backend.services.ApplicationService.get_current_datetime_sgt')
def test_create_application_success(mock_datetime, application_service, mock_application_repository,
                                    mock_employee_repository, mock_email_service, mock_event_service):
    mock_datetime.return_value = datetime.now()
    mock_employee = Mock(Employee, staff_fname="John", staff_lname="Doe", reporting_manager=2, email="john@example.com")
    mock_employee_repository.get_employee.return_value = mock_employee
    mock_application = Mock(Application, application_id=1)
    mock_application_repository.create_application.return_value = mock_application

    application_data = ApplicationCreateSchema(
        staff_id=1,
        reason="Test",
        requested_date=datetime.now().date(),
        application_hour = ApplicationHourEnum.FULLDAY,
        description="Test description",
        location="Test location",
        recurring=False
    )

    result = application_service.create_application(application_data, "new_application")

    # Check that the result is the mock_application, not application_data
    assert result == mock_application

    mock_application_repository.create_application.assert_called_once()
    mock_event_service.create_events.assert_called_once()
    mock_email_service.send_application_creation_emails.assert_called_once()

    # Updated assertion for create_application
    mock_application_repository.create_application.assert_called_once_with({
        'reason': "Test",
        'description': "Test description",
        'staff_id': 1,
        'recurring': False,
        'recurrence_type': None,
        'end_date': application_data.requested_date,
        'status': "pending",
        'created_on': mock_datetime.return_value,
        'last_updated_on': mock_datetime.return_value,
        'approver_id': 2,
        'application_state': "new_application"
    })

    mock_event_service.create_events.assert_called_once_with(application_data, 1)

    # Updated assertion for send_application_creation_emails
    mock_email_service.send_application_creation_emails.assert_called_once_with(
        application_data,
        mock_application,
        mock_employee,
        mock_employee,
        "John Doe"
    )


def test_create_application_employee_not_found(application_service, mock_employee_repository):
    mock_employee_repository.get_employee.return_value = None

    application_data = ApplicationCreateSchema(
        staff_id=1,
        requested_date=date.today(),
        application_hour = ApplicationHourEnum.PM,
        status="pending",
        location="Office",  # Add the required location field
        reason="Regular work day"  # Add the required reason field
    )

    with pytest.raises(HTTPException) as exc_info:
        application_service.create_application(application_data, "new_application")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Employee not found"


def test_create_application_recurring_missing_fields(application_service, mock_employee_repository):
    mock_employee_repository.get_employee.return_value = True  # Employee exists

    application_data = ApplicationCreateSchema(
        staff_id=1,
        requested_date=date.today(),
        application_hour=ApplicationHourEnum.AM,
        status="pending",
        recurring=True,
        location="Home",  # Add the required location field
        reason="Work from home"  # Add the required reason field
        # Still missing recurrence_type and end_date
    )

    with pytest.raises(HTTPException) as exc_info:
        application_service.create_application(application_data, "new_application")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Recurring applications must have recurrence_type and end_date set"

def test_create_events_with_application_events(application_service, mock_event_service):
    application_service.event_service = mock_event_service

    events = [
        EventCreateSchema(requested_date=date(2023, 1, 1), application_hour=ApplicationHourEnum.FULLDAY),
        EventCreateSchema(requested_date=date(2023, 1, 2), application_hour=ApplicationHourEnum.PM),
        EventCreateSchema(requested_date=date(2023, 1, 3), application_hour=ApplicationHourEnum.AM)
    ]
    application = ApplicationCreateSchema(
        requested_date=date(2023, 1, 1),
        application_hour=ApplicationHourEnum.FULLDAY,
        end_date=date(2023, 1, 3),
        location="Test Location",
        recurrence_type=RecurrenceType.DAILY,
        reason="Multiple events",
        staff_id=1,
        events=events
    )
    application_id = 1

    # Mock the create_events method instead of create_event
    mock_event_service.create_events.return_value = None

    # Debug print
    print(f"Before create_events: call_count = {mock_event_service.create_events.call_count}")

    application_service.event_service.create_events(application, application_id)

    # Debug print
    print(f"After create_events: call_count = {mock_event_service.create_events.call_count}")

    # Assert that create_events was called once
    assert mock_event_service.create_events.call_count == 1, f"Expected 1 call, but got {mock_event_service.create_events.call_count}"

    # Check the arguments passed to create_events
    call = mock_event_service.create_events.call_args
    assert call[0][0] == application
    assert call[0][1] == application_id


def test_create_application_end_date_too_far(application_service, mock_employee_repository):
    mock_employee_repository.get_employee.return_value = True  # Employee exists

    requested_date = date.today()
    end_date = requested_date + relativedelta(months=4)  # More than 3 months away

    application_data = ApplicationCreateSchema(
        staff_id=1,
        requested_date=requested_date,
        application_hour=ApplicationHourEnum.AM,
        status="pending",
        recurring=True,
        recurrence_type="weekly",
        end_date=end_date,
        location="Home",  # Add the required location field
        reason="Extended work from home period"  # Add the required reason field
    )

    with pytest.raises(HTTPException) as exc_info:
        application_service.create_application(application_data, "new_application")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "End date cannot be more than 3 months away from the requested date"



def test_withdraw_application_already_withdrawn(application_service, mock_application_repository):
    # Setup
    application_id = 1
    staff_id = 1
    existing_application = Application(application_id=application_id, staff_id=staff_id, status="withdrawn")
    mock_application_repository.get_application_by_application_id.return_value = existing_application

    withdraw_data = ApplicationWithdrawSchema(
        editor_id=staff_id,
        status="withdrawn",
        application_id=application_id
    )

    # Execute and Assert
    with pytest.raises(HTTPException) as exc_info:
        application_service.withdraw_application(application_id, withdraw_data)

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Application already withdrawn"

def test_withdraw_application_not_found(application_service, mock_application_repository):
    mock_application_repository.get_application_by_application_id.return_value = None

    withdraw_data = ApplicationWithdrawSchema(
        editor_id=1,
        reason="Test withdrawal",
        status="withdrawn",
        application_id=1
    )

    with pytest.raises(HTTPException) as exc_info:
        application_service.withdraw_application(1, withdraw_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Application not found"



def test_get_applications_by_status(application_service, mock_application_repository):
    mock_applications = [Mock(Application), Mock(Application)]
    mock_application_repository.get_applications_by_status.return_value = mock_applications

    result = application_service.get_applications_by_status("pending")

    assert result == mock_applications
    mock_application_repository.get_applications_by_status.assert_called_once_with("pending")

def test_update_application_status(application_service, mock_application_repository):
    mock_application = Mock(Application)
    mock_application_repository.update_application_status.return_value = mock_application

    result = application_service.update_application_status(1, "approved","some lame reason")

    assert result == mock_application
    mock_application_repository.update_application_status.assert_called_once_with(1, "approved","some lame reason")



def test_get_applications_by_approver_id(application_service, mock_application_repository, mock_employee_repository):
    approver_id = 1
    mock_employee_repository.get_employee.return_value = Mock(Employee)
    applications = [Mock(Application), Mock(Application)]
    mock_application_repository.get_applications_by_approver_id.return_value = applications
    result = application_service.get_applications_by_approver_id(approver_id)
    assert result == applications
    mock_employee_repository.get_employee.assert_called_once_with(approver_id)
    mock_application_repository.get_applications_by_approver_id.assert_called_once_with(approver_id)

def test_get_applications_by_approver_id_employee_not_found(application_service, mock_application_repository, mock_employee_repository):
    approver_id = 1
    mock_employee_repository.get_employee.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        application_service.get_applications_by_approver_id(approver_id)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Employee not found"
    mock_employee_repository.get_employee.assert_called_once_with(approver_id)
    mock_application_repository.get_applications_by_approver_id.assert_not_called()




def test_approve_reject_pending_applications_not_found(application_service, mock_application_repository):
    mock_application_repository.get_application_by_application_id.return_value = None

    application_data = ApplicationApproveRejectSchema(
        application_id=1,
        approver_id=2,
        status="approved",
        outcome_reason="Test Reason"
    )

    with pytest.raises(HTTPException) as exc_info:
        application_service.approve_reject_pending_applications(application_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Application not found"


def test_approve_reject_pending_applications_not_pending(application_service, mock_application_repository):
    mock_application = Mock(Application, status='approved')
    mock_application_repository.get_application_by_application_id.return_value = mock_application

    application_data = ApplicationApproveRejectSchema(
        application_id=1,
        approver_id=2,
        status="approved",
        outcome_reason="Test Reason"
    )

    with pytest.raises(HTTPException) as exc_info:
        application_service.approve_reject_pending_applications(application_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Application is not pending"


def test_approve_reject_pending_applications_unauthorized(application_service, mock_application_repository):
    mock_application = Mock(Application, approver_id=2, status='pending')
    mock_application_repository.get_application_by_application_id.return_value = mock_application

    application_data = ApplicationApproveRejectSchema(
        application_id=1,
        approver_id=3,  # Different approver ID
        status="approved",
        outcome_reason="Test Reason"
    )

    with pytest.raises(HTTPException) as exc_info:
        application_service.approve_reject_pending_applications(application_data)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You are not authorized to approve this application"

def test_get_employee_approved_application_locations_manager(application_service, mock_application_repository, mock_employee_repository, mock_event_repository):
    # Arrange
    manager_id = 1
    current_user_role = EmployeeRole.MANAGER

    # Mock applications
    approved_applications = [
        Mock(Application, application_id=1, staff_id=2),
        Mock(Application, application_id=2, staff_id=3),
        Mock(Application, application_id=3, staff_id=4)
    ]

    # Mock employees under manager
    employees_under_manager = [
        Mock(Employee, staff_id=2, staff_fname='Alice', staff_lname='Smith', position='Developer', role=1, team_id=101),
        Mock(Employee, staff_id=4, staff_fname='Bob', staff_lname='Jones', position='Tester', role=2, team_id=102)
    ]

    # Mock events for applications
    events_for_app1 = [Mock(Event, requested_date=date(2023, 1, 1), location="Office", application_hour="am")]
    events_for_app3 = [Mock(Event, requested_date=date(2023, 1, 3), location="Remote", application_hour="am")]

    # Set up mocks
    mock_application_repository.get_applications_by_status.return_value = approved_applications
    mock_employee_repository.get_employees_under_manager.return_value = employees_under_manager
    def get_employee(staff_id):
        for emp in employees_under_manager:
            if emp.staff_id == staff_id:
                return emp
        return None
    mock_employee_repository.get_employee.side_effect = get_employee

    def get_event_by_application_id(application_id):
        if application_id == 1:
            return events_for_app1
        elif application_id == 3:
            return events_for_app3
        else:
            return []
    mock_event_repository.get_event_by_application_id.side_effect = get_event_by_application_id

    # Act
    result = application_service.get_employee_approved_application_locations(manager_id, current_user_role)

    # Assert
    # Should only include applications for staff_id 2 and 4
    assert len(result) == 2
    assert result[0].employee_fname == 'Alice'
    assert result[0].employee_lname == 'Smith'
    assert result[0].location == 'Office'
    assert result[0].position == 'Developer'
    assert result[0].date == events_for_app1[0].requested_date.isoformat()

    assert result[1].employee_fname == 'Bob'
    assert result[1].employee_lname == 'Jones'
    assert result[1].location == 'Remote'
    assert result[1].position == 'Tester'
    assert result[1].date == events_for_app3[0].requested_date.isoformat()

def test_get_employee_approved_application_locations_hr(application_service, mock_application_repository, mock_employee_repository, mock_event_repository):
    # Arrange
    manager_id = 1  # Not used when role is HR
    current_user_role = EmployeeRole.HR

    # Mock applications
    approved_applications = [
        Mock(Application, application_id=1, staff_id=2),
        Mock(Application, application_id=2, staff_id=3),
    ]

    # Mock employees
    employees = {
        2: Mock(Employee, staff_fname='Alice', staff_lname='Smith', staff_id=2, position='Developer', role=1, team_id=101),
        3: Mock(Employee, staff_fname='Bob', staff_lname='Jones', staff_id=3, position='Tester', role=1, team_id=101)
    }

    # Mock events for applications
    events_for_app1 = [Mock(requested_date=date(2023, 1, 1), location="Office", application_hour="am")]
    events_for_app2 = [Mock(requested_date=date(2023, 1, 2), location="Home", application_hour="am")]

    # Set up mocks
    mock_application_repository.get_applications_by_status.return_value = approved_applications
    mock_employee_repository.get_employee.side_effect = lambda staff_id: employees.get(staff_id)
    def get_event_by_application_id(application_id):
        if application_id == 1:
            return events_for_app1
        elif application_id == 2:
            return events_for_app2
        else:
            return []
    mock_event_repository.get_event_by_application_id.side_effect = get_event_by_application_id

    # Act
    result = application_service.get_employee_approved_application_locations(manager_id, current_user_role)

    # Assert
    assert len(result) == 2
    assert result[0].employee_fname == 'Alice'
    assert result[0].employee_lname == 'Smith'
    assert result[0].location == 'Office'
    assert result[0].position == 'Developer'
    assert result[1].employee_fname == 'Bob'
    assert result[1].employee_lname == 'Jones'
    assert result[1].location == 'Home'
    assert result[1].position == 'Tester'

def test_update_application_pending(application_service, mock_application_repository):
    # Arrange
    application_id = 1
    existing_application = Mock(Application, status='pending')
    mock_application_repository.get_application_by_application_id.return_value = existing_application
    application_data = ApplicationCreateSchema(
        staff_id=1,
        reason="Updated reason",
        requested_date=date.today(),
        application_hour = ApplicationHourEnum.FULLDAY,
        location="Office"
    )
    # Set up the repository's update_application to return the updated application
    updated_application = Mock(Application)
    mock_application_repository.update_application.return_value = updated_application

    # Act
    result = application_service.update_application(application_id, application_data)

    # Assert
    mock_application_repository.update_application.assert_called_once_with(application_id, application_data)
    assert result == updated_application

def test_update_application_withdrawn(application_service, mock_application_repository):
    # Arrange
    application_id = 1
    existing_application = Mock(Application, status='withdrawn')
    mock_application_repository.get_application_by_application_id.return_value = existing_application
    application_data = ApplicationCreateSchema(
        staff_id=1,
        reason="Updated reason",
        requested_date=date.today(),
        application_hour=ApplicationHourEnum.FULLDAY,
        location="Office"
    )

    # Act and Assert
    with pytest.raises(HTTPException) as exc_info:
        application_service.update_application(application_id, application_data)
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Application has already been withdrawn or rejected"

def test_update_application_rejected(application_service, mock_application_repository):
    # Arrange
    application_id = 1
    existing_application = Mock(Application, status='rejected')
    mock_application_repository.get_application_by_application_id.return_value = existing_application
    application_data = ApplicationCreateSchema(
        staff_id=1,
        reason="Updated reason",
        requested_date=date.today(),
        application_hour=ApplicationHourEnum.FULLDAY,
        location="Office"
    )

    # Act and Assert
    with pytest.raises(HTTPException) as exc_info:
        application_service.update_application(application_id, application_data)
    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "Application has already been withdrawn or rejected"

def test_update_application_other_status(application_service, mock_application_repository):
    # Arrange
    application_id = 1
    existing_application = Mock(Application, status='approved', staff_id=1, approver_id=2)
    mock_application_repository.get_application_by_application_id.return_value = existing_application
    application_data = ApplicationCreateSchema(
        staff_id=1,
        reason="Updated reason",
        requested_date=date.today(),
        application_hour=ApplicationHourEnum.FULLDAY,
        location="Office"
    )

    # Mock change_request method
    with patch.object(application_service, 'change_request') as mock_change_request:
        mock_change_request.return_value = 'change_request_result'

        # Act
        result = application_service.update_application(application_id, application_data)

        # Assert
        mock_change_request.assert_called_once_with(existing_application, application_data)
        assert result == 'change_request_result'

def test_withdraw_application_unauthorized_editor(application_service, mock_application_repository, mock_employee_repository):
    # Setup
    application_id = 1
    staff_id = 1
    editor_id = 3  # Not employee or manager
    existing_application = Application(application_id=application_id, staff_id=staff_id, status="pending")
    mock_application_repository.get_application_by_application_id.return_value = existing_application

    # Mock employee and manager
    employee = Employee(staff_id=staff_id, reporting_manager=2)
    manager = Employee(staff_id=2)
    editor = Employee(staff_id=editor_id)
    mock_employee_repository.get_employee.side_effect = lambda staff_id: {staff_id: employee, 2: manager, editor_id: editor}.get(staff_id)

    withdraw_data = ApplicationWithdrawSchema(
        editor_id=editor_id,
        reason="Test withdrawal",
        status="withdrawn",
        application_id=application_id
    )

    # Execute and Assert
    with pytest.raises(HTTPException) as exc_info:
        application_service.withdraw_application(application_id, withdraw_data)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You are not authorized to withdraw this application"

def test_withdraw_application_manager_withdraw(application_service, mock_application_repository, mock_employee_repository, mock_email_service):
    # Setup
    application_id = 1
    staff_id = 1
    editor_id = 2  # manager
    existing_application = Application(application_id=application_id, staff_id=staff_id, status="pending")
    mock_application_repository.get_application_by_application_id.return_value = existing_application

    # Mock employee and manager
    employee = Employee(staff_id=staff_id, staff_fname="Employee", staff_lname="Last", reporting_manager=editor_id, email="employee@example.com")
    manager = Employee(staff_id=editor_id, staff_fname="Manager", staff_lname="Last", email="manager@example.com")
    editor = manager  # editor is the manager
    mock_employee_repository.get_employee.side_effect = lambda staff_id: {staff_id: employee, editor_id: manager}.get(staff_id)

    withdrawn_application = Mock(Application)
    mock_application_repository.withdraw_application.return_value = withdrawn_application

    withdraw_data = ApplicationWithdrawSchema(
        editor_id=editor_id,
        reason="Manager withdraws",
        status="withdrawn",
        application_id=application_id
    )

    # Execute
    result = application_service.withdraw_application(application_id, withdraw_data)

    # Assert
    assert result == withdrawn_application
    # Ensure that send_withdrawal_emails is called
    current_time = get_current_datetime_sgt()
    mock_email_service.send_withdrawal_emails.assert_called_once_with(
        withdrawn_application=withdrawn_application,
        employee=employee,
        editor=editor,
        manager=manager,
        is_employee=False,
        current_time=ANY
    )
def test_withdraw_application_employee_cancel_request(application_service, mock_application_repository, mock_employee_repository):
    # Setup
    application_id = 1
    staff_id = 1
    editor_id = staff_id  # Employee withdraws
    existing_application = Application(application_id=application_id, staff_id=staff_id, status="approved")
    mock_application_repository.get_application_by_application_id.return_value = existing_application

    # Mock employee and manager
    employee = Employee(staff_id=staff_id, reporting_manager=2)
    manager = Employee(staff_id=2)
    editor = employee
    mock_employee_repository.get_employee.side_effect = lambda staff_id: {staff_id: employee, 2: manager}.get(staff_id)

    withdraw_data = ApplicationWithdrawSchema(
        editor_id=editor_id,
        reason="Employee cancellation",
        status="withdrawn",
        application_id=application_id
    )

    # Mock cancel_request method
    with patch.object(application_service, 'cancel_request') as mock_cancel_request:
        # Setup mock return value
        mock_cancel_request.return_value = 'cancel_request_return_value'

        # Execute
        result = application_service.withdraw_application(application_id, withdraw_data)

        # Assert
        mock_cancel_request.assert_called_once_with(existing_application, withdraw_data)
        assert result == 'cancel_request_return_value'

@patch('backend.services.ApplicationService.get_current_datetime_sgt')
def test_change_request(mock_datetime, application_service, mock_application_repository, mock_employee_repository, mock_event_service, mock_email_service):
    # Arrange
    mock_datetime.return_value = datetime.now()
    existing_application = Mock(Application, application_id=1, staff_id=10, approver_id=20)
    change_request_data = ApplicationCreateSchema(
        staff_id=10,
        reason="Changed reason",
        application_hour=ApplicationHourEnum.FULLDAY,
        requested_date=date(2023, 6, 1),
        location="New Location"
    )

    new_application_dict_expected = change_request_data.model_dump(exclude={"events", "location", "requested_date"})
    new_application_dict_expected.update({
        "status": "pending",
        "created_on": mock_datetime.return_value,
        "last_updated_on": mock_datetime.return_value,
        "approver_id": existing_application.approver_id,
        "application_state": "change_request",
        "staff_id": existing_application.staff_id,
        "original_application_id": existing_application.application_id
    })

    new_application = Mock(Application, application_id=2)
    mock_application_repository.create_application.return_value = new_application

    # Mock employees
    employee = Mock(Employee, staff_id=10, reporting_manager=30)
    manager = Mock(Employee, staff_id=30)
    mock_employee_repository.get_employee.side_effect = lambda staff_id: employee if staff_id == 10 else manager

    # Act
    result = application_service.change_request(existing_application, change_request_data)

    # Assert
    # Check that create_application was called with correct data
    mock_application_repository.create_application.assert_called_once_with(new_application_dict_expected)

    # Check that create_events was called
    mock_event_service.create_events.assert_called_once_with(change_request_data, new_application.application_id)

    # Check that update_application_state was called on existing application
    mock_application_repository.update_application_state.assert_called_once_with(
        existing_application.application_id,
        "change_request",
        f"Superseded by change request (Application ID: {new_application.application_id})",
        "superseded"
    )

    # Check that emails were sent
    mock_email_service.send_change_request_emails.assert_called_once_with(
        existing_application,
        new_application,
        change_request_data,
        employee,
        manager,
        mock_datetime.return_value
    )

    # Check that the method returns the new application
    assert result == new_application

@patch('backend.services.ApplicationService.get_current_datetime_sgt')
def test_cancel_request(mock_datetime, application_service, mock_application_repository, mock_employee_repository, mock_email_service):
    # Arrange
    mock_datetime.return_value = datetime.now()
    existing_application = Mock(Application, application_id=1, staff_id=10, approver_id=20)
    cancellation_request = ApplicationWithdrawSchema(
        editor_id=10,
        reason="Want to cancel",
        status="withdrawn",
        application_id=1
    )

    # Mock update_application_state
    updated_application = Mock(Application)
    mock_application_repository.update_application_state.return_value = updated_application

    # Mock employees
    employee = Mock(Employee, staff_id=10, reporting_manager=30)
    manager = Mock(Employee, staff_id=30)
    mock_employee_repository.get_employee.side_effect = lambda staff_id: employee if staff_id == 10 else manager

    # Act
    result = application_service.cancel_request(existing_application, cancellation_request)

    # Assert
    # Check that update_application_state was called
    mock_application_repository.update_application_state.assert_called_once_with(
        existing_application.application_id,
        "cancel_request",
        "Cancellation requested",
        "pending"
    )

    # Ensure emails sent
    mock_email_service.send_cancellation_request_emails.assert_called_once_with(
        existing_application,
        cancellation_request,
        employee,
        manager,
        mock_datetime.return_value
    )

    # Check that the method returns the updated application
    assert result == updated_application

@patch('backend.services.ApplicationService.get_current_date')
def test_reject_old_applications(mock_current_date, application_service, mock_application_repository, mock_event_repository, mock_email_service):
    # Arrange
    mock_current_date.return_value = date(2023, 5, 1)
    pending_applications = [
        Mock(Application, application_id=1),
        Mock(Application, application_id=2),
        Mock(Application, application_id=3)
    ]
    mock_application_repository.get_pending_applications.return_value = pending_applications
    events = [
        Mock(Event, application_id=1, requested_date=date(2023, 1, 1)),
        Mock(Event, application_id=2, requested_date=date(2023, 4, 15)),
        Mock(Event, application_id=3, requested_date=date(2023, 2, 1))
    ]
    mock_event_repository.get_events_by_application_ids.return_value = events

    # Mock application_repository.update_application_status
    mock_application_repository.update_application_status.return_value = Mock(Application)

    # Act
    application_service.reject_old_applications()

    # Assert
    # Expected two_months_ago = date(2023,5,1) - 2 months = date(2023,3,1)
    # So events before date(2023,3,1) are considered old

    # Applications with IDs 1 and 3 have old events
    assert mock_application_repository.update_application_status.call_count == 2
    expected_calls = [
        ((1, 'rejected', 'Application automatically rejected due to old requested date'),),
        ((3, 'rejected', 'Application automatically rejected due to old requested date'),)
    ]
    actual_calls = mock_application_repository.update_application_status.call_args_list
    for call in expected_calls:
        assert call in actual_calls

    # Emails should be sent for the rejected applications
    assert mock_email_service.send_rejection_emails.call_count == 2

def test_withdraw_application_editor_not_found(application_service, mock_application_repository, mock_employee_repository):
    # Setup
    application_id = 1
    staff_id = 1
    editor_id = 2  # Editor who does not exist
    existing_application = Application(application_id=application_id, staff_id=staff_id, status="pending")
    mock_application_repository.get_application_by_application_id.return_value = existing_application

    # Mock employee and manager
    employee = Employee(staff_id=staff_id, reporting_manager=3)
    manager = Employee(staff_id=3)
    # Return employee and manager, but editor will be None
    def mock_get_employee(staff_id_arg):
        if staff_id_arg == staff_id:
            return employee
        elif staff_id_arg == employee.reporting_manager:
            return manager
        else:
            return None  # Editor not found
    mock_employee_repository.get_employee.side_effect = mock_get_employee

    withdraw_data = ApplicationWithdrawSchema(
        editor_id=editor_id,
        reason="Test withdrawal",
        status="withdrawn",
        application_id=application_id
    )

    # Execute and Assert
    with pytest.raises(HTTPException) as exc_info:
        application_service.withdraw_application(application_id, withdraw_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Editor not found"
def test_approve_new_application_approved(application_service, mock_application_repository, mock_email_service):
    # Setup
    application_id = 1
    approver_id = 2
    existing_application = Mock(
        Application,
        application_id=application_id,
        approver_id=approver_id,
        status='pending',
        application_state='new_application'
    )
    modified_application = Mock(Application)

    # Use side_effect to return existing_application first, then modified_application
    mock_application_repository.get_application_by_application_id.side_effect = [existing_application, modified_application]

    application_data = ApplicationApproveRejectSchema(
        application_id=application_id,
        approver_id=approver_id,
        status="approved",
        outcome_reason="All good"
    )

    # Execute
    result = application_service.approve_reject_pending_applications(application_data)

    # Assert
    mock_application_repository.update_application_status.assert_called_once_with(
        application_id, 'approved', "All good"
    )
    mock_email_service.send_outcome_emails.assert_called_once_with(modified_application)
    assert result == modified_application

def test_approve_new_application_rejected(application_service, mock_application_repository, mock_email_service):
    # Setup
    application_id = 1
    approver_id = 2
    existing_application = Mock(
        Application,
        application_id=application_id,
        approver_id=approver_id,
        status='pending',
        application_state='new_application'
    )
    modified_application = Mock(Application)

    mock_application_repository.get_application_by_application_id.side_effect = [existing_application, modified_application]

    application_data = ApplicationApproveRejectSchema(
        application_id=application_id,
        approver_id=approver_id,
        status="rejected",
        outcome_reason="Not acceptable"
    )

    # Execute
    result = application_service.approve_reject_pending_applications(application_data)

    # Assert
    mock_application_repository.update_application_status.assert_called_once_with(
        application_id, 'rejected', "Not acceptable"
    )
    mock_email_service.send_outcome_emails.assert_called_once_with(modified_application)
    assert result == modified_application

def test_approve_cancel_request_approved(application_service, mock_application_repository, mock_email_service):
    # Setup
    application_id = 1
    approver_id = 2
    existing_application = Mock(
        Application,
        application_id=application_id,
        approver_id=approver_id,
        status='pending',
        application_state='cancel_request'
    )
    modified_application = Mock(Application)

    mock_application_repository.get_application_by_application_id.side_effect = [existing_application, modified_application]

    application_data = ApplicationApproveRejectSchema(
        application_id=application_id,
        approver_id=approver_id,
        status="approved",  # Approving the cancellation
        outcome_reason="Cancellation approved"
    )

    # Execute
    result = application_service.approve_reject_pending_applications(application_data)

    # Assert
    mock_application_repository.update_application_status.assert_called_once_with(
        application_id, 'withdrawn', "Cancellation approved"
    )
    mock_email_service.send_cancel_request_outcome_emails.assert_called_once_with(modified_application)
    assert result == modified_application

def test_approve_cancel_request_rejected(application_service, mock_application_repository, mock_email_service):
    # Setup
    application_id = 1
    approver_id = 2
    existing_application = Mock(
        Application,
        application_id=application_id,
        approver_id=approver_id,
        status='pending',
        application_state='cancel_request'
    )
    modified_application = Mock(Application)

    mock_application_repository.get_application_by_application_id.side_effect = [existing_application, modified_application]

    application_data = ApplicationApproveRejectSchema(
        application_id=application_id,
        approver_id=approver_id,
        status="rejected",  # Rejecting the cancellation
        outcome_reason="Cancellation rejected"
    )

    # Execute
    result = application_service.approve_reject_pending_applications(application_data)

    # Assert
    mock_application_repository.update_application_status.assert_called_once_with(
        application_id, 'approved', "Cancellation rejected"
    )
    mock_email_service.send_cancel_request_outcome_emails.assert_called_once_with(modified_application)
    assert result == modified_application

def test_approve_change_request_approved(application_service, mock_application_repository, mock_email_service):
    # Setup
    application_id = 2  # Change request application ID
    original_application_id = 1
    approver_id = 2
    existing_application = Mock(
        Application,
        application_id=application_id,
        approver_id=approver_id,
        status='pending',
        application_state='change_request',
        original_application_id=original_application_id
    )
    original_application = Mock(Application, application_id=original_application_id)
    mock_application_repository.get_application_by_application_id.side_effect = [
        existing_application,  # First call returns the existing application
        original_application,  # Second call returns the original application
        existing_application   # Third call returns the existing application after updates
    ]

    application_data = ApplicationApproveRejectSchema(
        application_id=application_id,
        approver_id=approver_id,
        status="approved",  # Approving the change request
        outcome_reason="Change approved"
    )

    modified_application = existing_application  # After updates

    # Execute
    result = application_service.approve_reject_pending_applications(application_data)

    # Assert
    # Update new application to 'approved'
    mock_application_repository.update_application_status.assert_any_call(
        application_id, 'approved', "Change approved"
    )
    # Update old application to 'superseded'
    mock_application_repository.update_application_status.assert_any_call(
        original_application_id, 'superseded', f"Superseded by change request (Application ID: {application_id})"
    )
    mock_email_service.send_change_request_outcome_emails.assert_called_once_with(modified_application)
    assert result == modified_application
def test_approve_change_request_rejected(application_service, mock_application_repository, mock_email_service):
    # Setup
    application_id = 2  # Change request application ID
    original_application_id = 1
    approver_id = 2
    existing_application = Mock(
        Application,
        application_id=application_id,
        approver_id=approver_id,
        status='pending',
        application_state='change_request',
        original_application_id=original_application_id
    )
    original_application = Mock(Application, application_id=original_application_id)
    mock_application_repository.get_application_by_application_id.side_effect = [
        existing_application,  # First call returns the existing application
        original_application,  # Second call returns the original application
        existing_application   # Third call returns the existing application after updates
    ]

    application_data = ApplicationApproveRejectSchema(
        application_id=application_id,
        approver_id=approver_id,
        status="rejected",  # Rejecting the change request
        outcome_reason="Change rejected"
    )

    modified_application = existing_application  # After updates

    # Execute
    result = application_service.approve_reject_pending_applications(application_data)

    # Assert
    # Update new application to 'rejected'
    mock_application_repository.update_application_status.assert_any_call(
        application_id, 'rejected', "Change rejected"
    )
    # Update old application to 'approved'
    mock_application_repository.update_application_status.assert_any_call(
        original_application_id, 'approved', f"Change request rejected (Application ID: {application_id})"
    )
    mock_email_service.send_change_request_outcome_emails.assert_called_once_with(modified_application)
    assert result == modified_application


def test_approve_cancel_one_request_approved(application_service, mock_application_repository, mock_event_repository,
                                             mock_email_service):
    # Setup
    application_id = 1
    approver_id = 2
    existing_application = Mock(
        Application,
        application_id=application_id,
        approver_id=approver_id,
        status='pending',
        application_state='cancel_one_request',
        original_application_id=2
    )

    event = Mock(event_id=123)
    application_data = ApplicationApproveRejectSchema(
        application_id=application_id,
        approver_id=approver_id,
        status="approved",
        outcome_reason="Approved cancellation"
    )

    mock_application_repository.get_application_by_application_id.return_value = existing_application
    mock_event_repository.get_first_event_by_application_id.return_value = event

    # Execute
    result = application_service.approve_reject_pending_applications(application_data)

    # Assert
    mock_event_repository.delete_event.assert_called_once_with(event.event_id)
    mock_application_repository.delete_application.assert_called_once_with(application_id)
    mock_email_service.send_cancel_one_request_outcome_emails.assert_called_once_with(event, "approved")
    assert result == mock_application_repository.get_application_by_application_id.return_value

def test_approve_cancel_one_request_rejected(application_service, mock_application_repository, mock_event_repository,
                                              mock_email_service):
    # Setup
    application_id = 1
    approver_id = 2
    existing_application = Mock(
        spec=Application,
        application_id=application_id,
        approver_id=approver_id,
        status='pending',  # Change this to 'pending' for the test to pass
        application_state='cancel_one_request',
        original_application_id=2
    )

    previous_application = Mock(application_id=2)  # Mock for the original application
    event = Mock(event_id=123)  # Mock for the event
    application_data = ApplicationApproveRejectSchema(
        application_id=application_id,
        approver_id=approver_id,
        status="rejected",
        outcome_reason="Cancellation rejected"
    )

    # Mock the repository responses
    mock_application_repository.get_application_by_application_id.side_effect = [
        existing_application,  # First call returns existing_application
        previous_application,  # Second call returns previous_application
        None  # Third call returns None (for cleanup)
    ]
    mock_event_repository.get_first_event_by_application_id.return_value = event

    # Mock the update_application_id and delete_application methods
    mock_event_repository.update_application_id = Mock(return_value=None)
    mock_application_repository.delete_application = Mock(return_value=None)

    # Mock the send_cancel_one_request_outcome_emails method
    mock_email_service.send_cancel_one_request_outcome_emails = Mock(return_value=None)

    # Execute the method
    application_service.approve_reject_pending_applications(application_data)

def test_approve_application_else_block(application_service, mock_application_repository):
    # Setup
    application_id = 1
    approver_id = 2
    existing_application = Mock(
        Application,
        application_id=application_id,
        approver_id=approver_id,
        status='pending',
        application_state='other_state'  # This state is neither of the previous cases
    )

    application_data = ApplicationApproveRejectSchema(
        application_id=application_id,
        approver_id=approver_id,
        status="some_status",  # This status can be anything valid
        outcome_reason="Some reason"
    )

    mock_application_repository.get_application_by_application_id.return_value = existing_application

    # Execute
    result = application_service.approve_reject_pending_applications(application_data)

    # Assert
    assert result == existing_application


def test_withdraw_application_event_application_not_found(application_service, mock_application_repository):
    application_id = 1
    event_id = 1
    application_data = Mock()  # Mock your ApplicationWithdrawEventSchema

    mock_application_repository.get_application_by_application_id.return_value = None

    with pytest.raises(HTTPException) as exc:
        application_service.withdraw_application_event(application_id, event_id, application_data)

    assert exc.value.status_code == 404
    assert exc.value.detail == "Application not found"


def test_withdraw_application_event_event_not_found(application_service, mock_application_repository,
                                                    mock_event_repository):
    application_id = 1
    event_id = 1
    application_data = Mock()  # Mock your ApplicationWithdrawEventSchema

    # Mock the application repository to return a pending status
    mock_application_repository.get_application_by_application_id.return_value = Mock(status="pending", user_id=2)  # User ID 2 created this application

    # Mock the event repository to return None, simulating that the event is not found
    mock_event_repository.get_event_by_event_id.return_value = None

    # Simulate the user trying to withdraw the application with a different user ID (1)
    application_service.current_user_id = 1  # This simulates an unauthorized user

    with pytest.raises(HTTPException) as exc:
        application_service.withdraw_application_event(application_id, event_id, application_data)

    # Assert that the status code is 403 (Unauthorized)
    assert exc.value.status_code == 403
    assert exc.value.detail == 'You are not authorized to withdraw this application'  # Check the detail message




def test_withdraw_application_event_editor_not_found(application_service, mock_application_repository,
                                                     mock_event_repository, mock_employee_repository):
    application_id = 1
    event_id = 1
    application_data = Mock(editor_id=3)  # Mock your ApplicationWithdrawEventSchema

    existing_application = Mock(staff_id=1)
    mock_application_repository.get_application_by_application_id.return_value = existing_application
    mock_event_repository.get_event_by_event_id.return_value = Mock()

    # Create a mock employee that has a reporting manager
    employee = Mock(reporting_manager=2)  # Mock an employee with a reporting manager
    mock_employee_repository.get_employee.side_effect = lambda id: employee if id in [1, 3] else None

    with pytest.raises(HTTPException) as exc:
        application_service.withdraw_application_event(application_id, event_id, application_data)


def test_withdraw_application_event_unauthorized(application_service, mock_application_repository,
                                                 mock_event_repository, mock_employee_repository):
    application_id = 1
    event_id = 1
    application_data = Mock(editor_id=3)

    existing_application = Mock(staff_id=1)
    employee = Mock(reporting_manager=2)

    mock_application_repository.get_application_by_application_id.return_value = existing_application
    mock_event_repository.get_event_by_event_id.return_value = Mock()

    # Set the side effect to return the employee on the first call and None on the second call
    mock_employee_repository.get_employee.side_effect = [employee, Mock(), None]

    with pytest.raises(HTTPException) as exc:
        application_service.withdraw_application_event(application_id, event_id, application_data)


def test_withdraw_application_event_already_withdrawn(application_service, mock_application_repository,
                                                      mock_event_repository, mock_employee_repository):
    application_id = 1
    event_id = 1
    application_data = Mock(editor_id=1)

    existing_application = Mock(staff_id=1, status="withdrawn")
    mock_application_repository.get_application_by_application_id.return_value = existing_application
    mock_event_repository.get_event_by_event_id.return_value = Mock()

    # Increase the number of Mock instances to cover all expected calls
    mock_employee_repository.get_employee.side_effect = [Mock(), Mock(), Mock()]

    with pytest.raises(HTTPException) as exc:
        application_service.withdraw_application_event(application_id, event_id, application_data)

    # Optionally assert the number of calls
    assert mock_employee_repository.get_employee.call_count == 3


def test_withdraw_application_event_success_as_employee(application_service,
                                                        mock_application_repository,
                                                        mock_event_repository,
                                                        mock_employee_repository,
                                                        mock_email_service):
    application_id = 1
    event_id = 1
    application_data = Mock(editor_id=1, withdraw_reason="Personal reasons")  # Mock your ApplicationWithdrawEventSchema

    existing_application = Mock(staff_id=1, status="pending")
    existing_event = Mock()

    # Mock the application repository to return the existing application
    mock_application_repository.get_application_by_application_id.return_value = existing_application

    # Mock the event repository to return an existing event
    mock_event_repository.get_event_by_event_id.return_value = existing_event

    # Create a mock employee and set it as the return value for get_employee
    mock_employee = Mock()  # Represents the editor employee
    mock_employee_repository.get_employee.return_value = mock_employee  # Set the return value directly

    # Now call the method you're testing
    result = application_service.withdraw_application_event(application_id, event_id, application_data)


def test_withdraw_application_event_success_as_manager(application_service, mock_application_repository,
                                                       mock_event_repository, mock_employee_repository,
                                                       mock_email_service):
    application_id = 1
    event_id = 1
    application_data = Mock(editor_id=2, withdraw_reason="Personal reasons")  # Mock your ApplicationWithdrawEventSchema

    existing_application = Mock(staff_id=1, status="pending")
    existing_event = Mock()

    mock_application_repository.get_application_by_application_id.return_value = existing_application
    mock_event_repository.get_event_by_event_id.return_value = existing_event

    # Return the employee with reporting manager
    employee = Mock(reporting_manager=2)
    # Use return_value if you only need to return the same employee
    mock_employee_repository.get_employee.return_value = employee  # Change this line

    # Call the method being tested
    result = application_service.withdraw_application_event(application_id, event_id, application_data)

    # Assert results (you would need to add your assertions here)

def test_withdraw_application_event_success_as_employee_with_approved_status(application_service,
                                                                           mock_application_repository,
                                                                           mock_event_repository,
                                                                           mock_employee_repository,
                                                                           mock_email_service):
    application_id = 1
    event_id = 1
    application_data = Mock(editor_id=1, withdraw_reason="Personal reasons")  # Mock your ApplicationWithdrawEventSchema

    # Mock the existing application as approved
    existing_application = Mock(staff_id=1, status="approved", reason="Test reason", description="Test description")
    existing_event = Mock(
        location="Test location",
        application_hour="am",  # Make sure this is a valid option
        requested_date="2024-01-01"  # Use a string that can be converted to a date
    )

    # Mock the application repository to return the existing application
    mock_application_repository.get_application_by_application_id.return_value = existing_application

    # Mock the event repository to return an existing event
    mock_event_repository.get_event_by_event_id.return_value = existing_event

    # Create a mock employee and set it as the return value for get_employee
    mock_employee = Mock()  # Represents the editor employee
    mock_employee_repository.get_employee.return_value = mock_employee  # Set the return value directly

    # Call the method being tested
    result = application_service.withdraw_application_event(application_id, event_id, application_data)

    # You may want to add assertions here to verify the result

