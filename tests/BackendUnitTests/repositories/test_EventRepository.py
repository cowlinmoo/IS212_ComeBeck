import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from backend.models import Event
from backend.repositories.EventRepository import EventRepository


@pytest.fixture
def mock_db_session():
    """Fixture for creating a mock database session."""
    return MagicMock()


@pytest.fixture
def event_repository(mock_db_session):
    """Fixture for creating an EventRepository instance with a mock db session."""
    return EventRepository(db=mock_db_session)


@pytest.mark.unit
def test_get_all_events(event_repository, mock_db_session):
    # Arrange
    mock_events = [Event(event_id=1), Event(event_id=2)]
    mock_db_session.query.return_value.all.return_value = mock_events

    # Act
    result = event_repository.get_all_events()

    # Assert
    assert result == mock_events
    mock_db_session.query.assert_called_once_with(Event)


@pytest.mark.unit
def test_get_event_by_event_id(event_repository, mock_db_session):
    # Arrange
    mock_event = Event(event_id=1)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_event

    # Act
    result = event_repository.get_event_by_event_id(1)

    # Assert
    assert result == mock_event
    mock_db_session.query.assert_called_once_with(Event)


@pytest.mark.unit
def test_get_event_by_event_id_not_found(event_repository, mock_db_session):
    # Arrange
    mock_db_session.query.return_value.filter.return_value.first.return_value = None

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        event_repository.get_event_by_event_id(1)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Event not found"


@pytest.mark.unit
def test_get_event_by_application_id(event_repository, mock_db_session):
    # Arrange
    mock_events = [Event(event_id=1, application_id=1), Event(event_id=2, application_id=1)]
    mock_db_session.query.return_value.filter.return_value.all.return_value = mock_events

    # Act
    result = event_repository.get_event_by_application_id(1)

    # Assert
    assert result == mock_events
    mock_db_session.query.assert_called_once_with(Event)


@pytest.mark.unit
def test_create_event(event_repository, mock_db_session):
    # Arrange
    mock_event = Event(event_id=1)
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    # Act
    result = event_repository.create_event(mock_event)

    # Assert
    assert result == mock_event
    mock_db_session.add.assert_called_once_with(mock_event)
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(mock_event)


@pytest.mark.unit
def test_update_event(event_repository, mock_db_session):
    # Arrange
    mock_event = Event(event_id=1)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_event
    updated_event = {'name': 'Updated Event Name'}

    # Act
    result = event_repository.update_event(1, updated_event)

    # Assert
    assert result == mock_event
    assert mock_event.name == 'Updated Event Name'  # Assuming 'name' is an attribute of Event
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(mock_event)


@pytest.mark.unit
def test_delete_event(event_repository, mock_db_session):
    # Arrange
    mock_event = Event(event_id=1)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_event
    mock_db_session.delete = MagicMock()

    # Act
    result = event_repository.delete_event(1)

    # Assert
    assert result == mock_event
    mock_db_session.delete.assert_called_once_with(mock_event)
    mock_db_session.commit.assert_called_once()


@pytest.mark.unit
def test_update_application_id(event_repository, mock_db_session):
    # Arrange
    mock_event = Event(event_id=1, application_id=1)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_event

    # Act
    result = event_repository.update_application_id(1, 2)

    # Assert
    assert result.application_id == 2
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(mock_event)


@pytest.mark.unit
def test_update_original_event_id(event_repository, mock_db_session):
    # Arrange
    mock_event = Event(event_id=1, original_event_id=1)
    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_event

    # Act
    result = event_repository.update_original_event_id(1, 2)

    # Assert
    assert result.original_event_id == 2
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once_with(mock_event)


@pytest.mark.unit
def test_get_first_event_by_application_id(event_repository, mock_db_session):
    # Mocking the return value of the query
    mock_event = Event(event_id=1, application_id=1)
    mock_db_session.query().filter().first.return_value = mock_event

    event = event_repository.get_first_event_by_application_id(1)
    assert event == mock_event


@pytest.mark.unit
def test_get_first_event_by_application_id_not_found(event_repository, mock_db_session):
    # Simulating no event found
    mock_db_session.query().filter().first.return_value = None

    event = event_repository.get_first_event_by_application_id(999)
    assert event is None  # Since it should return None when no event is found


@pytest.mark.unit
def test_get_events_by_application_ids(event_repository, mock_db_session):
    # Mocking multiple return values for the query
    mock_events = [
        Event(event_id=1, application_id=1),
        Event(event_id=2, application_id=2),
    ]
    mock_db_session.query().filter().all.return_value = mock_events

    events = event_repository.get_events_by_application_ids([1, 2])
    assert len(events) == 2
    assert events[0].event_id == 1
    assert events[1].event_id == 2


@pytest.mark.unit
def test_get_events_by_application_ids_empty(event_repository, mock_db_session):
    # Simulating an empty return
    mock_db_session.query().filter().all.return_value = []

    events = event_repository.get_events_by_application_ids([999])  # Non-existing IDs
    assert events == []  # Should return an empty list