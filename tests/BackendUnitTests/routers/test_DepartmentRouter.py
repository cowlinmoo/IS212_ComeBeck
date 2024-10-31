import pytest
from unittest.mock import Mock
from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.routers.DepartmentRouter import get_department_by_department_id, get_all_departments

# Mock response data for single department
MOCK_DEPARTMENT = {
    "id": 1,
    "name": "Engineering",
    "description": "Engineering Department",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}

# Mock response data for multiple departments
MOCK_DEPARTMENTS = [
    {
        "id": 1,
        "name": "Engineering",
        "description": "Engineering Department",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 2,
        "name": "Sales",
        "description": "Sales Department",
        "created_at": "2024-01-02T00:00:00",
        "updated_at": "2024-01-02T00:00:00"
    }
]

@pytest.fixture
def mock_service():
    service = Mock()
    # Set up the return values for the service methods
    service.get_department_by_department_id.return_value = MOCK_DEPARTMENT
    service.get_all_departments.return_value = MOCK_DEPARTMENTS
    return service

@pytest.fixture
def mock_current_user():
    return {"role": EmployeeRole.HR}

pytest.mark.unit
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
@pytest.mark.unit
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
@pytest.mark.unit
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

@pytest.mark.unit
def test_get_all_departments(mock_service, mock_current_user):
    """
    Test the get_all_departments endpoint
    """
    # Call the endpoint with mock dependencies
    result = get_all_departments(
        service=mock_service,
        current_user=mock_current_user
    )

    # Assert the result matches our mock data
    assert result == MOCK_DEPARTMENTS

    # Verify the service method was called correctly
    mock_service.get_all_departments.assert_called_once_with()

# Additional test cases to ensure different roles can access the endpoint
@pytest.mark.parametrize("role", [
    EmployeeRole.HR,
    EmployeeRole.MANAGER,
    EmployeeRole.STAFF
])
@pytest.mark.unit
def test_get_all_departments_different_roles(mock_service, role):
    """
    Test the get_all_departments endpoint with different user roles
    """
    current_user = {"role": role}

    result = get_all_departments(
        service=mock_service,
        current_user=current_user
    )

    assert result == MOCK_DEPARTMENTS
    mock_service.get_all_departments.assert_called_once_with()

# Test with no departments available
@pytest.mark.unit
def test_get_all_departments_no_departments(mock_service, mock_current_user):
    """
    Test the get_all_departments endpoint when no departments are available
    """
    # Configure mock to return an empty list
    mock_service.get_all_departments.return_value = []

    result = get_all_departments(
        service=mock_service,
        current_user=mock_current_user
    )

    assert result == []
    mock_service.get_all_departments.assert_called_once_with()
