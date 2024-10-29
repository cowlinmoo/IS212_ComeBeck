import pytest
from fastapi import Depends
from datetime import timedelta, datetime, timezone
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from jose import jwt

from backend.services.AuthenticationService import AuthenticationService, SECRET_KEY, ALGORITHM
from backend.models.EmployeeModel import Employee
from backend.models.enums.EmployeeRoleEnum import EmployeeRole


@pytest.fixture
def mock_db():
    return Mock(spec=Session)


@pytest.fixture
def auth_service(mock_db):
    return AuthenticationService(mock_db)


def test_create_access_token_with_expiry():
    service = AuthenticationService()
    data = {"sub": "test@example.com"}
    expires_delta = timedelta(minutes=30)

    token = service.create_access_token(data, expires_delta)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "test@example.com"
    assert "exp" in decoded


def test_create_access_token_without_expiry():
    service = AuthenticationService()
    data = {"sub": "test@example.com"}

    token = service.create_access_token(data)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "test@example.com"
    assert "exp" in decoded


@patch('BackendUnitTests.services.AuthenticationService.bcrypt_context')
def test_authenticate_employee_success(mock_bcrypt, auth_service, mock_db):
    mock_employee = Mock(spec=Employee)
    mock_employee.email = "test@example.com"
    mock_employee.password = "hashed_password"
    mock_employee.role = 2

    mock_db.query.return_value.filter.return_value.first.return_value = mock_employee
    mock_bcrypt.verify.return_value = True

    employee, role = auth_service.authenticate_employee("test@example.com", "password")

    assert employee == mock_employee
    assert role == EmployeeRole.STAFF
    mock_bcrypt.verify.assert_called_once_with("password", "hashed_password")

@patch('BackendUnitTests.services.AuthenticationService.bcrypt_context')
def test_authenticate_manager_success(mock_bcrypt, auth_service, mock_db):
    mock_employee = Mock(spec=Employee)
    mock_employee.email = "test@example.com"
    mock_employee.password = "hashed_password"
    mock_employee.role = 3

    mock_db.query.return_value.filter.return_value.first.return_value = mock_employee
    mock_bcrypt.verify.return_value = True

    employee, role = auth_service.authenticate_employee("test@example.com", "password")

    assert employee == mock_employee
    assert role == EmployeeRole.MANAGER
    mock_bcrypt.verify.assert_called_once_with("password", "hashed_password")

@patch('BackendUnitTests.services.AuthenticationService.bcrypt_context')
def test_authenticate_hr_success(mock_bcrypt, auth_service, mock_db):
    mock_employee = Mock(spec=Employee)
    mock_employee.email = "test@example.com"
    mock_employee.password = "hashed_password"
    mock_employee.role = 1

    mock_db.query.return_value.filter.return_value.first.return_value = mock_employee
    mock_bcrypt.verify.return_value = True

    employee, role = auth_service.authenticate_employee("test@example.com", "password")

    assert employee == mock_employee
    assert role == EmployeeRole.HR
    mock_bcrypt.verify.assert_called_once_with("password", "hashed_password")

@patch('BackendUnitTests.services.AuthenticationService.bcrypt_context')
def test_authenticate_employee_wrong_password(mock_bcrypt, auth_service, mock_db):
    mock_employee = Mock(spec=Employee)
    mock_employee.email = "test@example.com"
    mock_employee.password = "hashed_password"

    mock_db.query.return_value.filter.return_value.first.return_value = mock_employee
    mock_bcrypt.verify.return_value = False

    employee, role = auth_service.authenticate_employee("test@example.com", "wrong_password")

    assert employee is None
    assert role is None


def test_authenticate_employee_not_found(auth_service, mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None

    employee, role = auth_service.authenticate_employee("nonexistent@example.com", "password")

    assert employee is None
    assert role is None


@patch('BackendUnitTests.services.AuthenticationService.bcrypt_context')
def test_authenticate_employee_exception(mock_bcrypt, auth_service, mock_db):
    mock_db.query.side_effect = Exception("Database error")

    employee, role = auth_service.authenticate_employee("test@example.com", "password")

    assert employee is None
    assert role is None


def test_db_dependency_injection():
    mock_db = Mock(spec=Session)
    service = AuthenticationService(mock_db)
    assert service.db == mock_db