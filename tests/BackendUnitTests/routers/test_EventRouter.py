import pytest
from unittest.mock import Mock, patch
from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.routers.EventRouter import (
    get_all_events,
    get_event_by_event_id
)

# Mock response data
MOCK_EVENT = {
    "id": 1,
    "type": "APPLICATION_CREATED",
    "description": "New application created",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}

MOCK_EVENTS = [
    MOCK_EVENT,
    {
        "id": 2,
        "type": "APPLICATION_APPROVED",
        "description": "Application approved",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
]


@pytest.fixture
def mock_service():
    service = Mock()
    # Set up return values for all service methods
    service.get_all_events.return_value = MOCK_EVENTS
    service.get_event_by_event_id.return_value = MOCK_EVENT
    return service


@pytest.fixture
def mock_current_user():
    return {"role": EmployeeRole.HR}


def test_get_all_events(mock_service, mock_current_user):
    """
    Test getting all events
    """
    result = get_all_events(
        event_service=mock_service,
        current_user=mock_current_user
    )

    assert result == MOCK_EVENTS
    mock_service.get_all_events.assert_called_once()


@pytest.mark.parametrize("role", [
    EmployeeRole.HR,
    EmployeeRole.MANAGER,
    EmployeeRole.STAFF
])
def test_get_all_events_different_roles(mock_service, role):
    """
    Test getting all events with different user roles
    """
    current_user = {"role": role}

    result = get_all_events(
        event_service=mock_service,
        current_user=current_user
    )

    assert result == MOCK_EVENTS
    mock_service.get_all_events.assert_called_once()


def test_get_event_by_event_id(mock_service, mock_current_user):
    """
    Test getting a single event by event_id
    """
    result = get_event_by_event_id(
        event_id=1,
        event_service=mock_service,
        current_user=mock_current_user
    )

    assert result == MOCK_EVENT
    mock_service.get_event_by_event_id.assert_called_once_with(1)


@pytest.mark.parametrize("role", [
    EmployeeRole.HR,
    EmployeeRole.MANAGER,
    EmployeeRole.STAFF
])
def test_get_event_by_event_id_different_roles(mock_service, role):
    """
    Test getting event by ID with different user roles
    """
    current_user = {"role": role}

    result = get_event_by_event_id(
        event_id=1,
        event_service=mock_service,
        current_user=current_user
    )

    assert result == MOCK_EVENT
    mock_service.get_event_by_event_id.assert_called_once_with(1)


def test_get_event_by_event_id_not_found(mock_service, mock_current_user):
    """
    Test getting a non-existent event
    """
    mock_service.get_event_by_event_id.return_value = None

    result = get_event_by_event_id(
        event_id=999,
        event_service=mock_service,
        current_user=mock_current_user
    )

    assert result is None
    mock_service.get_event_by_event_id.assert_called_once_with(999)