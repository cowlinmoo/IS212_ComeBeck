import pytest
from unittest.mock import Mock, patch
from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.routers.DepartmentRouter import get_department_by_department_id

# Mock response data
MOCK_DEPARTMENT = {
    "id": 1,
    "name": "Engineering",
    "description": "Engineering Department",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}


@pytest.fixture
def mock_service():
    service = Mock()
    # Set up the return value for the get_department_by_department_id method
    service.get_department_by_department_id.return_value = MOCK_DEPARTMENT
    return service


@pytest.fixture
def mock_current_user():
    return {"role": EmployeeRole.HR}


def test_get_department_by_department_id(mock_service, mock_current_user):
    """
    Test the get_department_by_department_id endpoint
    """
    # Call the endpoint with mock dependencies
    result = get_department_by_department_id(
        department_id=1,
        service=mock_service,
        current_user=mock_current_user
    )

    # Assert the result matches our mock data
    assert result == MOCK_DEPARTMENT

    # Verify the service method was called with correct parameters
    mock_service.get_department_by_department_id.assert_called_once_with(1)


# Additional test cases to ensure different roles can access the endpoint
@pytest.mark.parametrize("role", [
    EmployeeRole.HR,
    EmployeeRole.MANAGER,
    EmployeeRole.STAFF
])
def test_get_department_by_department_id_different_roles(mock_service, role):
    """
    Test the get_department_by_department_id endpoint with different user roles
    """
    current_user = {"role": role}

    result = get_department_by_department_id(
        department_id=1,
        service=mock_service,
        current_user=current_user
    )

    assert result == MOCK_DEPARTMENT
    mock_service.get_department_by_department_id.assert_called_once_with(1)


# Test with invalid department ID
def test_get_department_by_department_id_invalid_id(mock_service, mock_current_user):
    """
    Test the get_department_by_department_id endpoint with an invalid department ID
    """
    # Configure mock to return None for invalid ID
    mock_service.get_department_by_department_id.return_value = None

    result = get_department_by_department_id(
        department_id=999,
        service=mock_service,
        current_user=mock_current_user
    )

    assert result is None
    mock_service.get_department_by_department_id.assert_called_once_with(999)