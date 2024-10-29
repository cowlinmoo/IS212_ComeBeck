import pytest
from unittest.mock import Mock, patch
from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.routers.EmployeeRouter import (
    get_all_employees,
    get_employee,
    create_employee,
    update_employee,
    delete_employee
)

# Mock response data
MOCK_EMPLOYEE = {
    "id": 1,
    "staff_id": 1001,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "role": EmployeeRole.STAFF,
    "department_id": 1,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}

MOCK_EMPLOYEES = [
    MOCK_EMPLOYEE,
    {
        "id": 2,
        "staff_id": 1002,
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "jane.smith@example.com",
        "role": EmployeeRole.MANAGER,
        "department_id": 1,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
]


@pytest.fixture
def mock_service():
    service = Mock()
    # Set up return values for all service methods
    service.get_all_employees.return_value = MOCK_EMPLOYEES
    service.get_employee_by_staff_id.return_value = MOCK_EMPLOYEE
    service.create_employee.return_value = MOCK_EMPLOYEE
    service.update_employee.return_value = MOCK_EMPLOYEE
    service.delete_employee_by_staff_id.return_value = MOCK_EMPLOYEE
    return service


@pytest.fixture
def mock_current_user():
    return {"role": EmployeeRole.HR}


def test_get_all_employees(mock_service, mock_current_user):
    """
    Test getting all employees
    """
    result = get_all_employees(
        employee_service=mock_service,
        current_user=mock_current_user
    )

    assert result == MOCK_EMPLOYEES
    mock_service.get_all_employees.assert_called_once()


@pytest.mark.parametrize("role", [
    EmployeeRole.HR,
    EmployeeRole.MANAGER,
    EmployeeRole.STAFF
])
def test_get_all_employees_different_roles(mock_service, role):
    """
    Test getting all employees with different user roles
    """
    current_user = {"role": role}

    result = get_all_employees(
        employee_service=mock_service,
        current_user=current_user
    )

    assert result == MOCK_EMPLOYEES
    mock_service.get_all_employees.assert_called_once()


def test_get_employee(mock_service, mock_current_user):
    """
    Test getting a single employee by staff_id
    """
    result = get_employee(
        staff_id=1001,
        employee_service=mock_service,
        current_user=mock_current_user
    )

    assert result == MOCK_EMPLOYEE
    mock_service.get_employee_by_staff_id.assert_called_once_with(1001)


def test_create_employee(mock_service):
    """
    Test creating a new employee
    """
    employee_data = Mock()

    result = create_employee(
        employee=employee_data,
        employee_service=mock_service
    )

    assert result == MOCK_EMPLOYEE
    mock_service.create_employee.assert_called_once_with(employee_data)


def test_update_employee(mock_service, mock_current_user):
    """
    Test updating an existing employee
    """
    employee_data = Mock()

    result = update_employee(
        staff_id=1001,
        employee=employee_data,
        employee_service=mock_service,
        current_user=mock_current_user
    )

    assert result == MOCK_EMPLOYEE
    mock_service.update_employee.assert_called_once_with(1001, employee_data)


@pytest.mark.parametrize("role", [
    EmployeeRole.HR,
    EmployeeRole.MANAGER
])
def test_update_employee_different_roles(mock_service, role):
    """
    Test updating employee with different authorized roles
    """
    current_user = {"role": role}
    employee_data = Mock()

    result = update_employee(
        staff_id=1001,
        employee=employee_data,
        employee_service=mock_service,
        current_user=current_user
    )

    assert result == MOCK_EMPLOYEE
    mock_service.update_employee.assert_called_once_with(1001, employee_data)


def test_delete_employee(mock_service, mock_current_user):
    """
    Test deleting an employee
    """
    result = delete_employee(
        staff_id=1001,
        employee_service=mock_service,
        current_user=mock_current_user
    )

    assert result == MOCK_EMPLOYEE
    mock_service.delete_employee_by_staff_id.assert_called_once_with(1001)


@pytest.mark.parametrize("role", [
    EmployeeRole.HR,
    EmployeeRole.MANAGER
])
def test_delete_employee_different_roles(mock_service, role):
    """
    Test deleting employee with different authorized roles
    """
    current_user = {"role": role}

    result = delete_employee(
        staff_id=1001,
        employee_service=mock_service,
        current_user=current_user
    )

    assert result == MOCK_EMPLOYEE
    mock_service.delete_employee_by_staff_id.assert_called_once_with(1001)


# Test error cases
def test_get_employee_not_found(mock_service, mock_current_user):
    """
    Test getting a non-existent employee
    """
    mock_service.get_employee_by_staff_id.return_value = None

    result = get_employee(
        staff_id=9999,
        employee_service=mock_service,
        current_user=mock_current_user
    )

    assert result is None
    mock_service.get_employee_by_staff_id.assert_called_once_with(9999)