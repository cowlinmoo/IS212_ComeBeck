import pytest
from unittest.mock import Mock
from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.routers.TeamRouter import get_team_by_team_id, get_team_by_manager_id

# Mock response data for team by team_id
MOCK_TEAM = {
    "id": 1,
    "name": "Engineering Team",
    "department_id": 1,
    "employees": [
        {
            "id": 1,
            "staff_id": 1001,
            "first_name": "John",
            "last_name": "Doe",
            "role": EmployeeRole.STAFF
        },
        {
            "id": 2,
            "staff_id": 1002,
            "first_name": "Jane",
            "last_name": "Smith",
            "role": EmployeeRole.MANAGER
        }
    ],
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}

# Mock response data for team by manager_id
MOCK_TEAM_BY_MANAGER = {
    "id": 1,
    "name": "Engineering Team",
    "department_id": 1,
    "employees": [
        {
            "id": 1,
            "staff_id": 1001,
            "first_name": "John",
            "last_name": "Doe",
            "role": EmployeeRole.STAFF
        },
        {
            "id": 2,
            "staff_id": 1002,
            "first_name": "Jane",
            "last_name": "Smith",
            "role": EmployeeRole.MANAGER
        }
    ],
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}

@pytest.fixture
def mock_service():
    service = Mock()
    # Set up return values for service methods
    service.get_team_employees_by_team_id.return_value = MOCK_TEAM
    service.get_team_employees_by_manager_id.return_value = MOCK_TEAM_BY_MANAGER
    return service

@pytest.fixture
def mock_current_user():
    return {"role": EmployeeRole.HR}

# Tests for get_team_by_team_id
@pytest.mark.unit
def test_get_team_by_team_id(mock_service, mock_current_user):
    """
    Test getting team by team_id
    """
    result = get_team_by_team_id(
        team_id=1,
        service=mock_service,
        current_user=mock_current_user
    )

    assert result == MOCK_TEAM
    mock_service.get_team_employees_by_team_id.assert_called_once_with(1)

@pytest.mark.parametrize("role", [
    EmployeeRole.HR,
    EmployeeRole.MANAGER,
    EmployeeRole.STAFF
])
@pytest.mark.unit
def test_get_team_by_team_id_different_roles(mock_service, role):
    """
    Test getting team by ID with different user roles
    """
    current_user = {"role": role}

    result = get_team_by_team_id(
        team_id=1,
        service=mock_service,
        current_user=current_user
    )

    assert result == MOCK_TEAM
    mock_service.get_team_employees_by_team_id.assert_called_once_with(1)

@pytest.mark.unit
def test_get_team_by_team_id_not_found(mock_service, mock_current_user):
    """
    Test getting a non-existent team by team_id
    """
    mock_service.get_team_employees_by_team_id.return_value = None

    result = get_team_by_team_id(
        team_id=999,
        service=mock_service,
        current_user=mock_current_user
    )

    assert result is None
    mock_service.get_team_employees_by_team_id.assert_called_once_with(999)

# Tests for get_team_by_manager_id
@pytest.mark.unit
def test_get_team_by_manager_id(mock_service, mock_current_user):
    """
    Test getting team by manager_id
    """
    # Call the endpoint with mock dependencies
    result = get_team_by_manager_id(
        manager_id=1,
        service=mock_service,
        current_user=mock_current_user
    )

    # Assert the result matches our mock data
    assert result == MOCK_TEAM_BY_MANAGER
    # Verify the service method was called with correct parameters
    mock_service.get_team_employees_by_manager_id.assert_called_once_with(1)

@pytest.mark.parametrize("role", [
    EmployeeRole.HR,
    EmployeeRole.MANAGER
])
@pytest.mark.unit
def test_get_team_by_manager_id_different_roles(mock_service, role):
    """
    Test the get_team_by_manager_id endpoint with different user roles
    """
    current_user = {"role": role}

    result = get_team_by_manager_id(
        manager_id=1,
        service=mock_service,
        current_user=current_user
    )

    assert result == MOCK_TEAM_BY_MANAGER
    mock_service.get_team_employees_by_manager_id.assert_called_once_with(1)

@pytest.mark.unit
def test_get_team_by_manager_id_not_found(mock_service, mock_current_user):
    """
    Test the get_team_by_manager_id endpoint with a non-existent manager
    """
    # Configure mock to return None for non-existent manager
    mock_service.get_team_employees_by_manager_id.return_value = None

    result = get_team_by_manager_id(
        manager_id=999,
        service=mock_service,
        current_user=mock_current_user
    )

    assert result is None
    mock_service.get_team_employees_by_manager_id.assert_called_once_with(999)
