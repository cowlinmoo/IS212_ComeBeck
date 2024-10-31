import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from backend.routers.AuthenticationRouter import login_for_access_token
from backend.models.enums.EmployeeRoleEnum import EmployeeRole


class MockEmployee:
    def __init__(self, email="test@example.com", role=EmployeeRole.STAFF, staff_id=1):
        self.email = email
        self.role = role
        self.staff_id = staff_id


@pytest.fixture
def mock_form_data():
    form_data = Mock(spec=OAuth2PasswordRequestForm)
    form_data.username = "test@example.com"
    form_data.password = "password123"
    return form_data


@pytest.fixture
def mock_auth_service():
    service = Mock()

    # Default successful authentication setup
    employee = MockEmployee()
    service.authenticate_employee.return_value = (employee, EmployeeRole.STAFF)
    service.create_access_token.return_value = "mocked_access_token"

    return service


@pytest.mark.unit
def test_successful_login(mock_form_data, mock_auth_service):
    # Test successful login
    result = login_for_access_token(
        form_data=mock_form_data,
        auth_service=mock_auth_service
    )

    # Verify the authentication was called with correct credentials
    mock_auth_service.authenticate_employee.assert_called_once_with(
        mock_form_data.username,
        mock_form_data.password
    )

    # Verify token creation was called with correct data
    mock_auth_service.create_access_token.assert_called_once_with(
        data={"sub": "test@example.com", "role": EmployeeRole.STAFF, "id": 1}
    )

    # Verify the response structure
    assert result.email == "test@example.com"
    assert result.role == "STAFF"
    assert result.access_token == "mocked_access_token"
    assert result.token_type == "bearer"
    assert result.staff_id == 1


@pytest.mark.unit
def test_failed_authentication(mock_form_data, mock_auth_service):
    # Mock failed authentication
    mock_auth_service.authenticate_employee.return_value = (None, None)

    # Test failed login
    with pytest.raises(HTTPException) as exc_info:
        login_for_access_token(
            form_data=mock_form_data,
            auth_service=mock_auth_service
        )

    # Verify the exception details
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Incorrect email or password"
    assert exc_info.value.headers == {"WWW-Authenticate": "Bearer"}

    # Verify the authentication was called
    mock_auth_service.authenticate_employee.assert_called_once_with(
        mock_form_data.username,
        mock_form_data.password
    )

    # Verify token creation was not called
    mock_auth_service.create_access_token.assert_not_called()


@pytest.mark.unit
def test_different_role_login(mock_form_data, mock_auth_service):
    # Mock HR employee authentication
    hr_employee = MockEmployee(
        email="hr@example.com",
        role=EmployeeRole.HR,
        staff_id=2
    )
    mock_auth_service.authenticate_employee.return_value = (hr_employee, EmployeeRole.HR)
    mock_auth_service.create_access_token.return_value = "hr_access_token"

    # Test HR login
    result = login_for_access_token(
        form_data=mock_form_data,
        auth_service=mock_auth_service
    )

    # Verify the response for HR role
    assert result.email == "hr@example.com"
    assert result.role == "HR"
    assert result.access_token == "hr_access_token"
    assert result.token_type == "bearer"
    assert result.staff_id == 2


@pytest.mark.unit
def test_manager_role_login(mock_form_data, mock_auth_service):
    # Mock Manager employee authentication
    manager_employee = MockEmployee(
        email="manager@example.com",
        role=EmployeeRole.MANAGER,
        staff_id=3
    )
    mock_auth_service.authenticate_employee.return_value = (manager_employee, EmployeeRole.MANAGER)
    mock_auth_service.create_access_token.return_value = "manager_access_token"

    # Test Manager login
    result = login_for_access_token(
        form_data=mock_form_data,
        auth_service=mock_auth_service
    )

    # Verify the response for Manager role
    assert result.email == "manager@example.com"
    assert result.role == "MANAGER"
    assert result.access_token == "manager_access_token"
    assert result.token_type == "bearer"
    assert result.staff_id == 3