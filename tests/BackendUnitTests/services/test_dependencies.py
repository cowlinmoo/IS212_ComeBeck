import pytest
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from backend.config.Database import get_db_connection
from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.repositories.ApplicationRepository import ApplicationRepository
from backend.repositories.EmployeeRepository import EmployeeRepository
from backend.repositories.EventRepository import EventRepository
from backend.services.ApplicationService import ApplicationService
from backend.services.AuthenticationService import SECRET_KEY, ALGORITHM
from backend.services.EmailService import EmailService
from backend.services.EventService import EventService
from backend.services.SchedulerService import SchedulerService

from backend.services.dependencies import (
    get_current_user,
    role_required,
    get_application_repository,
    get_employee_repository,
    get_email_service,
    get_event_repository,
    get_event_service,
    get_application_service,
    get_scheduler_service,
)


# Mock fixtures
@pytest.fixture
def mock_db():
    return Mock(spec=Session)


@pytest.fixture
def mock_get_db_connection(mock_db):
    return lambda: mock_db


@pytest.fixture
def mock_application_repository():
    return Mock(spec=ApplicationRepository)


@pytest.fixture
def mock_employee_repository():
    return Mock(spec=EmployeeRepository)


@pytest.fixture
def mock_email_service():
    return Mock(spec=EmailService)


@pytest.fixture
def mock_event_repository():
    return Mock(spec=EventRepository)


@pytest.fixture
def mock_event_service():
    return Mock(spec=EventService)


# Tests for get_current_user
@patch('backend.services.dependencies.jwt.decode')
@pytest.mark.unit
def test_get_current_user_valid_token(mock_jwt_decode):
    mock_jwt_decode.return_value = {"sub": "test@example.com", "role": 1}
    token = "valid_token"
    result = get_current_user(token)
    assert result == {"email": "test@example.com", "role": EmployeeRole(1)}


@patch('backend.services.dependencies.jwt.decode')
@pytest.mark.unit
def test_get_current_user_invalid_token(mock_jwt_decode):
    mock_jwt_decode.side_effect = JWTError()
    token = "invalid_token"
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"


@patch('backend.services.dependencies.jwt.decode')
@pytest.mark.unit
def test_get_current_user_missing_fields(mock_jwt_decode):
    mock_jwt_decode.return_value = {"sub": "test@example.com"}
    token = "incomplete_token"
    with pytest.raises(HTTPException) as exc_info:
        get_current_user(token)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Could not validate credentials"


# Tests for role_required
@pytest.mark.unit
def test_role_required_allowed_role():
    allowed_roles = [EmployeeRole.HR, EmployeeRole.MANAGER]
    decorator = role_required(*allowed_roles)
    current_user = {"email": "admin@example.com", "role": EmployeeRole.HR}
    result = decorator(current_user)
    assert result == current_user


@pytest.mark.unit
def test_role_required_forbidden_role():
    allowed_roles = [EmployeeRole.HR, EmployeeRole.MANAGER]
    decorator = role_required(*allowed_roles)
    current_user = {"email": "employee@example.com", "role": EmployeeRole.STAFF}
    with pytest.raises(HTTPException) as exc_info:
        decorator(current_user)
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Sorry you don't have enough permissions to perform this action"


# Tests for repository and service getters
@pytest.mark.unit
def test_get_application_repository(mock_db):
    result = get_application_repository(mock_db)
    assert isinstance(result, ApplicationRepository)
    assert result.db == mock_db


@pytest.mark.unit
def test_get_employee_repository(mock_db):
    result = get_employee_repository(mock_db)
    assert isinstance(result, EmployeeRepository)
    assert result.db == mock_db


@pytest.mark.unit
def test_get_email_service():
    result = get_email_service()
    assert isinstance(result, EmailService)


@pytest.mark.unit
def test_get_event_repository(mock_db):
    result = get_event_repository(mock_db)
    assert isinstance(result, EventRepository)
    assert result.db == mock_db


@patch('backend.services.dependencies.EventService')
@pytest.mark.unit
def test_get_event_service(mock_event_service_class, mock_event_repository):
    result = get_event_service(mock_event_repository)
    mock_event_service_class.assert_called_once_with(mock_event_repository)
    assert result == mock_event_service_class.return_value


# Test for get_application_service
@pytest.mark.unit
def test_get_application_service(
        mock_application_repository,
        mock_employee_repository,
        mock_email_service,
        mock_event_repository,
        mock_event_service
):
    result = get_application_service(
        mock_application_repository,
        mock_employee_repository,
        mock_email_service,
        mock_event_repository,
        mock_event_service
    )
    assert isinstance(result, ApplicationService)
    assert result.application_repository == mock_application_repository
    assert result.employee_repository == mock_employee_repository
    assert result.email_service == mock_email_service
    assert result.event_repository == mock_event_repository
    assert result.event_service == mock_event_service


# Test for get_scheduler_service
@patch('backend.services.dependencies.get_db_connection')
@patch('backend.services.dependencies.ApplicationRepository')
@patch('backend.services.dependencies.EmployeeRepository')
@patch('backend.services.dependencies.EmailService')
@patch('backend.services.dependencies.EventRepository')
@patch('backend.services.dependencies.EventService')
@patch('backend.services.dependencies.ApplicationService')
@patch('backend.services.dependencies.SchedulerService')
@pytest.mark.unit
def test_get_scheduler_service(
        mock_scheduler_service,
        mock_application_service,
        mock_event_service,
        mock_event_repository,
        mock_email_service,
        mock_employee_repository,
        mock_application_repository,
        mock_get_db_connection
):
    mock_db = Mock()
    mock_get_db_connection.return_value = iter([mock_db])

    result = get_scheduler_service()

    mock_application_repository.assert_called_once_with(mock_db)
    mock_employee_repository.assert_called_once_with(mock_db)
    mock_email_service.assert_called_once()
    mock_event_repository.assert_called_once_with(mock_db)
    mock_event_service.assert_called_once_with(mock_event_repository.return_value)
    mock_application_service.assert_called_once_with(
        mock_application_repository.return_value,
        mock_employee_repository.return_value,
        mock_email_service.return_value,
        mock_event_repository.return_value,
        mock_event_service.return_value
    )
    mock_scheduler_service.assert_called_once_with(mock_application_service.return_value)
    assert result == mock_scheduler_service.return_value