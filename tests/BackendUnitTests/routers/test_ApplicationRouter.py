import pytest
from unittest.mock import Mock, patch
from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.routers.ApplicationRouter import (
    get_all_applications, get_application_by_id, get_applications_by_staff_id,
    get_applications_by_approver_id, create_application, update_application,
    withdraw_application, withdraw_application_event, get_applications_by_status,
    get_all_employee_locations_by_manager_id, process_application
)

# Mock response data
MOCK_APPLICATION = {
    "id": 1,
    "status": "PENDING",
    "staff_id": 1,
    "approver_id": 2,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
}

MOCK_EVENT = {
    "id": 1,
    "type": "WITHDRAWAL",
    "created_at": "2024-01-01T00:00:00"
}

@pytest.fixture
def mock_service():
    service = Mock()
    service.get_all_applications.return_value = [MOCK_APPLICATION]
    service.get_application_by_id.return_value = MOCK_APPLICATION
    service.get_applications_by_staff_id.return_value = [MOCK_APPLICATION]
    service.get_applications_by_approver_id.return_value = [MOCK_APPLICATION]
    service.create_application.return_value = MOCK_APPLICATION
    service.update_application.return_value = MOCK_APPLICATION
    service.withdraw_application.return_value = MOCK_APPLICATION
    service.withdraw_application_event.return_value = MOCK_EVENT
    service.get_applications_by_status.return_value = [MOCK_APPLICATION]
    service.get_employee_approved_application_locations.return_value = [{"location": "Office A", "staff_id": 1}]
    service.approve_reject_pending_applications.return_value = MOCK_APPLICATION
    return service

@pytest.fixture
def mock_current_user():
    return {"role": EmployeeRole.HR}

def test_get_all_applications(mock_service, mock_current_user):
    result = get_all_applications(service=mock_service, current_user=mock_current_user)
    assert result == [MOCK_APPLICATION]
    mock_service.get_all_applications.assert_called_once()

def test_get_application_by_id(mock_service, mock_current_user):
    result = get_application_by_id(1, service=mock_service, current_user=mock_current_user)
    assert result == MOCK_APPLICATION
    mock_service.get_application_by_id.assert_called_once_with(1)

def test_get_applications_by_staff_id(mock_service, mock_current_user):
    result = get_applications_by_staff_id(1, service=mock_service, current_user=mock_current_user)
    assert result == [MOCK_APPLICATION]
    mock_service.get_applications_by_staff_id.assert_called_once_with(1)

def test_get_applications_by_approver_id(mock_service, mock_current_user):
    result = get_applications_by_approver_id(1, service=mock_service, current_user=mock_current_user)
    assert result == [MOCK_APPLICATION]
    mock_service.get_applications_by_approver_id.assert_called_once_with(1)

def test_create_application(mock_service, mock_current_user):
    application_data = Mock()
    result = create_application(application=application_data, service=mock_service, current_user=mock_current_user)
    assert result == MOCK_APPLICATION
    mock_service.create_application.assert_called_once_with(application_data, "new_application")

def test_update_application(mock_service, mock_current_user):
    application_data = Mock()
    result = update_application(1, application=application_data, service=mock_service, current_user=mock_current_user)
    assert result == MOCK_APPLICATION
    mock_service.update_application.assert_called_once_with(1, application_data)

def test_withdraw_application(mock_service, mock_current_user):
    withdraw_data = Mock()
    result = withdraw_application(1, application=withdraw_data, service=mock_service, current_user=mock_current_user)
    assert result == MOCK_APPLICATION
    mock_service.withdraw_application.assert_called_once_with(1, withdraw_data)

def test_withdraw_application_event(mock_service, mock_current_user):
    withdraw_data = Mock()
    result = withdraw_application_event(1, 1, application=withdraw_data, service=mock_service, current_user=mock_current_user)
    assert result == MOCK_EVENT
    mock_service.withdraw_application_event.assert_called_once_with(1, 1, withdraw_data)

def test_get_applications_by_status(mock_service, mock_current_user):
    result = get_applications_by_status("PENDING", service=mock_service, current_user=mock_current_user)
    assert result == [MOCK_APPLICATION]
    mock_service.get_applications_by_status.assert_called_once_with("PENDING")

def test_get_employee_locations_by_manager(mock_service, mock_current_user):
    result = get_all_employee_locations_by_manager_id(1, service=mock_service, current_user=mock_current_user)
    assert result == [{"location": "Office A", "staff_id": 1}]
    mock_service.get_employee_approved_application_locations.assert_called_once_with(manager_id=1, current_user_role=mock_current_user["role"])

def test_process_application(mock_service, mock_current_user):
    application_data = Mock()
    result = process_application(application=application_data, service=mock_service, current_user=mock_current_user)
    assert result == MOCK_APPLICATION
    mock_service.approve_reject_pending_applications.assert_called_once_with(application_data)