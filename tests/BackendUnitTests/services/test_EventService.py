import pytest
from unittest.mock import MagicMock
from datetime import datetime, date, timedelta
from backend.models import Event
from backend.models.enums.ApplicationHourEnum import ApplicationHourEnum
from backend.models.enums.RecurrenceType import RecurrenceType
from backend.schemas.ApplicationSchema import ApplicationCreateSchema
from backend.services.EventService import EventService


@pytest.fixture
def event_repository_mock():
    return MagicMock()


@pytest.fixture
def event_service(event_repository_mock):
    return EventService(eventRepository=event_repository_mock)


@pytest.mark.unit
def test_get_all_events(event_service, event_repository_mock):
    # Arrange
    mock_events = [Event(event_id=1), Event(event_id=2)]
    event_repository_mock.get_all_events.return_value = mock_events

    # Act
    events = event_service.get_all_events()

    # Assert
    assert events == mock_events
    event_repository_mock.get_all_events.assert_called_once()


@pytest.mark.unit
def test_create_event(event_service, event_repository_mock):
    # Arrange
    new_event = Event(requested_date=datetime.now(), location="Location A", application_hour="am")
    event_repository_mock.create_event.return_value = new_event

    # Act
    created_event = event_service.create_event(new_event)

    # Assert
    assert created_event == new_event
    event_repository_mock.create_event.assert_called_once_with(new_event)


@pytest.mark.unit
def test_create_multiple_events(event_service, event_repository_mock):
    # Arrange
    application = ApplicationCreateSchema(
        location="Location A",
        reason="Team meeting",
        requested_date=date.today(),
        application_hour=ApplicationHourEnum.AM,
        description="Team meeting scheduled",
        staff_id=1,
        recurring=False,
        events=[
            Event(requested_date=date.today(), application_hour=ApplicationHourEnum.AM),
            # Use date.today() instead of datetime.now()
            Event(requested_date=date.today(), application_hour=ApplicationHourEnum.PM)
            # Use date.today() instead of datetime.now()
        ]
    )

    application_id = 1

    # Act
    event_service.create_events(application, application_id)

    # Assert
    assert event_repository_mock.create_event.call_count == 2  # Ensure create_event was called twice
    calls = event_repository_mock.create_event.call_args_list
    assert calls[0][0][0].location == application.location  # First event's location
    assert calls[0][0][0].application_id == application_id  # First event's application_id
    assert calls[1][0][0].location == application.location  # Second event's location
    assert calls[1][0][0].application_id == application_id  # Second event's application_id

@pytest.mark.unit
def test_create_multiple_events_loop():
    # Arrange
    event_service = EventService()  # Assume EventService is your service class
    event_service.eventRepository = MagicMock()  # Mock the event repository

    events_to_create = [
        Event(requested_date=date.today(), location="Location A", application_hour=ApplicationHourEnum.AM),
        Event(requested_date=date.today(), location="Location B", application_hour=ApplicationHourEnum.PM)
    ]

    # Mock the return value of create_event for each event
    event_service.eventRepository.create_event.side_effect = events_to_create

    # Act
    created_events = event_service.create_multiple_events(events_to_create)

    # Assert
    assert len(created_events) == len(events_to_create)  # Ensure the same number of events were created
    assert event_service.eventRepository.create_event.call_count == len(events_to_create)  # Ensure create_event was called the correct number of times

    # Verify that the created events match the expected events
    for i, event in enumerate(events_to_create):
        assert created_events[i].requested_date == event.requested_date
        assert created_events[i].location == event.location
        assert created_events[i].application_hour == event.application_hour

@pytest.mark.unit
def test_create_single_event(event_service, event_repository_mock):
    # Arrange
    application = ApplicationCreateSchema(
        location="Location A",
        reason="Going on a family vacation",
        requested_date=date.today(),
        application_hour=ApplicationHourEnum.AM,  # Ensure this is an enum
        description="Family vacation planned",
        staff_id=1,
        recurring=False,
        events=[]  # Ensure that events is included
    )

    application_id = 1
    expected_event = Event(
        requested_date=application.requested_date,
        location=application.location,
        application_id=application_id,
        application_hour=application.application_hour
    )
    event_repository_mock.create_event.return_value = expected_event

    # Act
    event_service.create_events(application, application_id)

    # Assert
    # Check if create_event was called with the right attributes
    event_repository_mock.create_event.assert_called_once()
    actual_event = event_repository_mock.create_event.call_args[0][0]  # Get the actual event object
    assert expected_event.requested_date == actual_event.requested_date
    assert expected_event.location == actual_event.location
    assert expected_event.application_id == actual_event.application_id
    assert expected_event.application_hour == actual_event.application_hour


@pytest.mark.unit
def test_create_recurring_events(event_service, event_repository_mock):
    # Arrange
    application = ApplicationCreateSchema(
        location="Location A",
        reason="Weekly team meeting",
        requested_date=date.today(),
        application_hour=ApplicationHourEnum.AM,
        description="Weekly team meeting scheduled",
        staff_id=1,
        recurring=True,  # Set to True for recurring events
        events=[]  # Empty events since we're testing recurring
    )

    application_id = 1

    # Mock the create_recurring_events method
    event_service.create_recurring_events = MagicMock()

    # Act
    event_service.create_events(application, application_id)

    # Assert
    event_service.create_recurring_events.assert_called_once_with(application, application_id)


@pytest.mark.unit
def test_delete_event(event_service, event_repository_mock):
    # Arrange
    event_id = 1

    # Act
    event_service.delete_event(event_id)

    # Assert
    event_repository_mock.delete_event.assert_called_once_with(event_id)
@pytest.mark.unit
def test_get_event_by_event_id(event_service, event_repository_mock):
    # Arrange
    event_id = 1
    mock_event = Event(event_id=event_id, location="Location A", application_hour="am")
    event_repository_mock.get_event_by_event_id.return_value = mock_event

    # Act
    event = event_service.get_event_by_event_id(event_id)

    # Assert
    assert event == mock_event
    event_repository_mock.get_event_by_event_id.assert_called_once_with(event_id)


@pytest.mark.unit
def test_get_event_by_application_id(event_service, event_repository_mock):
    # Arrange
    application_id = 1
    mock_event = Event(event_id=2, location="Location B", application_hour="pm")
    event_repository_mock.get_event_by_application_id.return_value = mock_event

    # Act
    event = event_service.get_event_by_application_id(application_id)

    # Assert
    assert event == mock_event
    event_repository_mock.get_event_by_application_id.assert_called_once_with(application_id)
@pytest.mark.unit
def test_update_event(event_service, event_repository_mock):
    # Arrange
    event_id = 1
    updated_event = Event(event_id=event_id, location="Updated Location", application_hour="pm")

    # Set the return value for the update_event method in the repository mock
    event_repository_mock.update_event.return_value = updated_event

    # Act
    result = event_service.update_event(event_id, updated_event)

    # Assert
    assert result == updated_event
    event_repository_mock.update_event.assert_called_once_with(event_id, updated_event)
@pytest.mark.unit
def test_create_recurring_events_daily(event_service, event_repository_mock):
    # Arrange
    application = ApplicationCreateSchema(
        location="Location A",
        reason="Team meeting",
        requested_date=date.today(),
        application_hour=ApplicationHourEnum.AM,
        description="Team meeting scheduled",
        staff_id=1,
        recurring=True,
        recurrence_type=RecurrenceType.DAILY,
        end_date=date.today() + timedelta(days=364),  # Set end_date to 3 days from today
        events=[]
    )
    application_id = 1
    # Act
    event_service.create_recurring_events(application, application_id)

    # Assert
    assert event_repository_mock.create_event.call_count == 365  # Expect 365 events created for daily recurrence

@pytest.mark.unit
def test_create_recurring_events_weekly(event_service, event_repository_mock):
    # Arrange
    application = ApplicationCreateSchema(
        location="Location B",
        reason="Weekly Sync",
        requested_date=date.today(),
        application_hour=ApplicationHourEnum.AM,
        description="Weekly sync scheduled",
        staff_id=1,
        recurring=True,
        recurrence_type=RecurrenceType.WEEKLY,
        end_date=date.today() + timedelta(weeks=2),  # End date is two weeks later
        events=[]
    )
    application_id = 1
    # Act
    event_service.create_recurring_events(application, application_id)

    # Assert
    assert event_repository_mock.create_event.call_count == 3  # Expect 3 events created for weekly recurrence

@pytest.mark.unit
def test_create_recurring_events_monthly(event_service, event_repository_mock):
    # Arrange
    application = ApplicationCreateSchema(
        location="Location C",
        reason="Monthly Review",
        requested_date=date.today(),
        application_hour=ApplicationHourEnum.AM,
        description="Monthly review scheduled",
        staff_id=1,
        recurring=True,
        recurrence_type=RecurrenceType.MONTHLY,
        end_date=date.today() + timedelta(days=90),  # End date is three months later
        events=[]
    )
    application_id = 1
    # Act
    event_service.create_recurring_events(application, application_id)

    # Assert
    assert event_repository_mock.create_event.call_count == 3  # Expect 3 events created for monthly recurrence
