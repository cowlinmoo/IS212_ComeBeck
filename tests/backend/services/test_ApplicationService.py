import pytest
from datetime import datetime, timedelta, date
from unittest.mock import Mock, patch, create_autospec
from fastapi import HTTPException
from dateutil.relativedelta import relativedelta

from backend.schemas.EventSchema import EventCreateSchema
from backend.services.ApplicationService import ApplicationService
from backend.models.enums.RecurrenceType import RecurrenceType
from backend.models import Application, Event, Employee
from backend.schemas.ApplicationSchema import ApplicationCreateSchema, ApplicationUpdateSchema, \
    ApplicationWithdrawSchema


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
    mock_employee_repository.get_employee.return_value = Mock(Employee, staff_fname="John", staff_lname="Doe",
                                                              reporting_manager=2, email="john@example.com")
    mock_application_repository.create_application.return_value = Mock(Application, application_id=1)

    application_data = ApplicationCreateSchema(
        staff_id=1,
        reason="Test",
        requested_date=datetime.now().date(),
        description="Test description",
        location="Test location",
        recurring=False
    )

    result = application_service.create_application(application_data)

    assert result == application_data
    mock_application_repository.create_application.assert_called_once()
    mock_event_service.create_event.assert_called_once()
    mock_email_service.send_email.assert_called()


def test_create_application_employee_not_found(application_service, mock_employee_repository):
    mock_employee_repository.get_employee.return_value = None

    application_data = ApplicationCreateSchema(
        staff_id=1,
        requested_date=date.today(),
        status="pending",
        location="Office",  # Add the required location field
        reason="Regular work day"  # Add the required reason field
    )

    with pytest.raises(HTTPException) as exc_info:
        application_service.create_application(application_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Employee not found"


def test_create_application_recurring_missing_fields(application_service, mock_employee_repository):
    mock_employee_repository.get_employee.return_value = True  # Employee exists

    application_data = ApplicationCreateSchema(
        staff_id=1,
        requested_date=date.today(),
        status="pending",
        recurring=True,
        location="Home",  # Add the required location field
        reason="Work from home"  # Add the required reason field
        # Still missing recurrence_type and end_date
    )

    with pytest.raises(HTTPException) as exc_info:
        application_service.create_application(application_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Recurring applications must have recurrence_type and end_date set"
from backend.models.EventModel import Event as EventModel  # Adjust import path as needed

def test_create_events_with_application_events(application_service, mock_event_service):
    events = [
        EventCreateSchema(requested_date=date(2023, 1, 1)),
        EventCreateSchema(requested_date=date(2023, 1, 2)),
        EventCreateSchema(requested_date=date(2023, 1, 3))
    ]
    application = ApplicationCreateSchema(
        requested_date=date(2023, 1, 1),
        end_date=date(2023, 1, 3),
        location="Test Location",
        recurrence_type=RecurrenceType.DAILY,
        reason="Multiple events",
        staff_id=1,
        events=events
    )
    application_id = 1

    mock_event_service.create_event.return_value = None

    application_service._create_events(application, application_id)

    assert mock_event_service.create_event.call_count == 3

    calls = mock_event_service.create_event.call_args_list
    for i, call in enumerate(calls):
        assert call[0][0].requested_date == events[i].requested_date
        assert call[0][0].location == "Test Location"
        assert call[0][0].application_id == application_id

def test_create_events_recurring(application_service, mock_event_service):
    # Setup
    application = ApplicationCreateSchema(
        requested_date=date(2023, 1, 1),
        end_date=date(2023, 3, 1),
        location="Test Location",
        recurrence_type=RecurrenceType.WEEKLY,
        reason="Test Reason",
        staff_id=1,
        recurring=True,
        events=[]  # Use an empty list instead of None
    )
    application_id = 1

    # Mock the event_service.create_event method
    mock_event_service.create_event.return_value = None

    # Execute
    application_service._create_events(application, application_id)

    # Assert
    expected_calls = 9  # 9 weeks between Jan 1 and Mar 1
    assert mock_event_service.create_event.call_count == expected_calls

    # Check the arguments of each call
    for i, call in enumerate(mock_event_service.create_event.call_args_list):
        args, _ = call
        event = args[0]
        assert isinstance(event, Event)
        assert event.requested_date == application.requested_date + timedelta(weeks=i)
        assert event.location == application.location
        assert event.application_id == application_id

def test_create_recurring_events_monthly(application_service, mock_event_service):
    # Setup
    application = ApplicationCreateSchema(
        requested_date=date(2023, 1, 1),  # Changed to date object
        end_date=date(2023, 5, 1),  # Changed to date object
        location="Test Location",
        recurrence_type=RecurrenceType.MONTHLY,
        reason="Monthly meeting",
        staff_id=1
    )
    application_id = 1

    # Mock the event_service.create_event method
    mock_event_service.create_event.return_value = None

    # Execute
    application_service._create_recurring_events(application, application_id)

    # Assert
    expected_calls = 5  # Jan 1, Feb 1, Mar 1, Apr 1, May 1
    assert mock_event_service.create_event.call_count == expected_calls

    # Check the arguments of each call
    expected_dates = [
        date(2023, 1, 1),
        date(2023, 2, 1),
        date(2023, 3, 1),
        date(2023, 4, 1),
        date(2023, 5, 1)
    ]
    for i, call in enumerate(mock_event_service.create_event.call_args_list):
        args, _ = call
        event = args[0]
        assert isinstance(event, Event)
        assert event.requested_date == expected_dates[i]
        assert event.location == application.location
        assert event.application_id == application_id

from datetime import date  # Add this import if not already present

def test_create_recurring_events_no_end_date(application_service, mock_event_service):
    # Setup
    application = ApplicationCreateSchema(
        requested_date=date(2023, 1, 1),  # Changed to date object
        end_date=None,
        location="Test Location",
        recurrence_type=RecurrenceType.DAILY,
        reason="Daily event",
        staff_id=1
    )
    application_id = 1

    # Mock the event_service.create_event method
    mock_event_service.create_event.return_value = None

    # Execute
    application_service._create_recurring_events(application, application_id)

    # Assert
    expected_calls = 1  # Only one event is created
    assert mock_event_service.create_event.call_count == expected_calls

    # Check the arguments of the call
    call = mock_event_service.create_event.call_args_list[0]
    event = call[0][0]

    assert event.requested_date == date(2023, 1, 1)  # Changed to date object
    assert event.location == "Test Location"
    assert event.application_id == application_id

def test_create_application_end_date_too_far(application_service, mock_employee_repository):
    mock_employee_repository.get_employee.return_value = True  # Employee exists

    requested_date = date.today()
    end_date = requested_date + relativedelta(months=4)  # More than 3 months away

    application_data = ApplicationCreateSchema(
        staff_id=1,
        requested_date=requested_date,
        status="pending",
        recurring=True,
        recurrence_type="weekly",
        end_date=end_date,
        location="Home",  # Add the required location field
        reason="Extended work from home period"  # Add the required reason field
    )

    with pytest.raises(HTTPException) as exc_info:
        application_service.create_application(application_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "End date cannot be more than 3 months away from the requested date"

def test_create_recurring_events_monthly_across_years(application_service, mock_event_service):
    application = ApplicationCreateSchema(
        requested_date=date(2023, 12, 15),
        end_date=date(2024, 2, 15),
        location="Test Location",
        recurrence_type=RecurrenceType.MONTHLY,
        reason="Monthly event across years",
        staff_id=1
    )
    application_id = 1

    mock_event_service.create_event.return_value = None

    application_service._create_recurring_events(application, application_id)

    assert mock_event_service.create_event.call_count == 3

    calls = mock_event_service.create_event.call_args_list
    assert calls[0][0][0].requested_date == date(2023, 12, 15)
    assert calls[1][0][0].requested_date == date(2024, 1, 15)
    assert calls[2][0][0].requested_date == date(2024, 2, 15)
def test_update_application(application_service, mock_application_repository):
    mock_application = Mock(Application)
    mock_application_repository.update_application.return_value = mock_application

    update_data = ApplicationUpdateSchema(
        status="approved",
        requested_date=date.today()
    )
    result = application_service.update_application(1, update_data)

    assert result == mock_application
    mock_application_repository.update_application.assert_called_once_with(1, update_data)


def test_withdraw_application_success(application_service, mock_application_repository, mock_employee_repository,
                                      mock_email_service):
    mock_application = Mock(Application, staff_id=1, status="pending")
    mock_application_repository.get_application_by_application_id.return_value = mock_application
    mock_employee_repository.get_employee.return_value = Mock(Employee, staff_fname="John", staff_lname="Doe",
                                                              reporting_manager=2, email="john@example.com")
    mock_application_repository.withdraw_application.return_value = mock_application

    withdraw_data = ApplicationWithdrawSchema(
        staff_id=1,
        reason="Test withdrawal",
        status="withdrawn",  # Add the required status field
        application_id=1  # Add the required application_id field
    )
    result = application_service.withdraw_application(1, withdraw_data)

    assert result == mock_application
    mock_application_repository.withdraw_application.assert_called_once_with(1, withdraw_data)
    mock_email_service.send_email.assert_called()


def test_withdraw_application_already_withdrawn(application_service, mock_application_repository):
    # Setup
    application_id = 1
    staff_id = 1
    existing_application = Application(application_id=application_id, staff_id=staff_id, status="withdrawn")
    mock_application_repository.get_application_by_application_id.return_value = existing_application

    withdraw_data = ApplicationWithdrawSchema(
        staff_id=staff_id,
        status="withdrawn",
        application_id=application_id
    )

    # Execute and Assert
    with pytest.raises(HTTPException) as exc_info:
        application_service.withdraw_application(application_id, withdraw_data)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Application already withdrawn"

def test_withdraw_application_not_found(application_service, mock_application_repository):
    mock_application_repository.get_application_by_application_id.return_value = None

    withdraw_data = ApplicationWithdrawSchema(
        staff_id=1,
        reason="Test withdrawal",
        status="withdrawn",
        application_id=1
    )

    with pytest.raises(HTTPException) as exc_info:
        application_service.withdraw_application(1, withdraw_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Application not found"


def test_withdraw_application_wrong_staff(application_service, mock_application_repository, mock_employee_repository):
    # Setup
    application_id = 1
    staff_id = 1
    wrong_staff_id = 2
    existing_application = Application(application_id=application_id, staff_id=staff_id, status="pending")
    mock_application_repository.get_application_by_application_id.return_value = existing_application
    mock_employee_repository.get_employee.return_value = {"id": wrong_staff_id, "name": "Wrong Employee"}

    withdraw_data = ApplicationWithdrawSchema(
        staff_id=wrong_staff_id,
        status="withdrawn",
        application_id=application_id
    )

    # Execute and Assert
    with pytest.raises(HTTPException) as exc_info:
        application_service.withdraw_application(application_id, withdraw_data)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "You can only withdraw your own application"

def test_get_applications_by_status(application_service, mock_application_repository):
    mock_applications = [Mock(Application), Mock(Application)]
    mock_application_repository.get_applications_by_status.return_value = mock_applications

    result = application_service.get_applications_by_status("pending")

    assert result == mock_applications
    mock_application_repository.get_applications_by_status.assert_called_once_with("pending")

def test_withdraw_application_employee_not_found(application_service, mock_application_repository, mock_employee_repository):
    # Setup
    application_id = 1
    staff_id = 1
    wrong_staff_id = 2
    existing_application = Application(application_id=application_id, staff_id=staff_id, status="pending")
    mock_application_repository.get_application_by_application_id.return_value = existing_application
    mock_employee_repository.get_employee.return_value = None

    withdraw_data = ApplicationWithdrawSchema(
        staff_id=wrong_staff_id,
        status="withdrawn",
        application_id=application_id
    )

    # Execute and Assert
    with pytest.raises(HTTPException) as exc_info:
        application_service.withdraw_application(application_id, withdraw_data)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Employee not found"

def test_update_application_status(application_service, mock_application_repository):
    mock_application = Mock(Application)
    mock_application_repository.update_application_status.return_value = mock_application

    result = application_service.update_application_status(1, "approved")

    assert result == mock_application
    mock_application_repository.update_application_status.assert_called_once_with(1, "approved")


@patch('backend.services.ApplicationService.get_current_date')
def test_reject_old_applications(mock_current_date, application_service, mock_application_repository,
                                 mock_event_repository, mock_employee_repository, mock_email_service):
    mock_current_date.return_value = datetime(2023, 6, 1).date()

    mock_application_repository.get_pending_applications.return_value = [
        Mock(Application, application_id=1),
        Mock(Application, application_id=2)
    ]

    mock_event_repository.get_events_by_application_ids.return_value = [
        Mock(Event, application_id=1, requested_date=datetime(2023, 3, 1).date()),
        Mock(Event, application_id=2, requested_date=datetime(2023, 5, 1).date())
    ]

    mock_employee_repository.get_employee.return_value = Mock(Employee, staff_fname="John", staff_lname="Doe",
                                                              email="john@example.com")

    application_service.reject_old_applications()

    mock_application_repository.update_application_status.assert_called_once_with(1, 'rejected')
    mock_email_service.send_email.assert_called_once()