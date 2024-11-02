from unittest.mock import MagicMock

import pytest
from datetime import datetime
from typing import List, Type

from fastapi import HTTPException
from sqlalchemy import desc
from backend.models.ApplicationModel import Application
from backend.models.EventModel import Event
from backend.schemas.ApplicationSchema import ApplicationCreateSchema, ApplicationWithdrawSchema
from backend.repositories.ApplicationRepository import ApplicationRepository

class MockSession:
    def __init__(self):
        self.applications = []

    def query(self, model):
        return self

    def filter(self, condition):
        return self

    def all(self):
        return self.applications

    def first(self):
        return self.applications[0] if self.applications else None

    def order_by(self, *args):
        return self

    def add(self, application):
        # This method should add the application to the mock database.
        self.applications.append(application)

    def commit(self):
        # Simulate committing the session (no-op for mock)
        pass
    def refresh(self, instance):
        # Simulate refreshing an instance (no-op for mock)
        pass

    def delete(self, application):
        # This method should delete the application from the mock database.
        self.applications.remove(application)

    def options(self, *args):
        # Simply return self to allow chaining
        return self

@pytest.fixture
def application_repository():
    repo = ApplicationRepository()
    repo.db = MockSession()
    return repo

@pytest.mark.unit
def test_get_all_applications(application_repository):
    # Arrange
    mock_applications = [Application(application_id=1), Application(application_id=2)]
    application_repository.db.applications = mock_applications

    # Act
    result = application_repository.get_all_applications()

    # Assert
    assert len(result) == 2
    assert result == mock_applications

@pytest.mark.unit
def test_get_application_by_application_id(application_repository):
    # Arrange
    mock_application = Application(application_id=1)
    application_repository.db.applications = [mock_application]

    # Act
    result = application_repository.get_application_by_application_id(1)

    # Assert
    assert result == mock_application


@pytest.mark.unit
def test_get_application_by_application_id_not_found(application_repository):
    # Arrange
    application_repository.db.applications = []

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        application_repository.get_application_by_application_id(1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Application not found"

@pytest.mark.unit
def test_get_application_by_staff_id(application_repository):
    # Arrange
    mock_applications = [
        Application(application_id=1, staff_id=1),
        Application(application_id=2, staff_id=1),
    ]
    application_repository.db.applications = mock_applications

    # Debug print
    print("Mock applications:")
    for app in mock_applications:
        print(f"  ID: {app.application_id}, Staff ID: {app.staff_id}")
    # Act
    result = application_repository.get_application_by_staff_id(1)
    # Assert
    assert len(result) == 2
    assert all(app.staff_id == 1 for app in result)
    assert all(app.application_id in [1, 2] for app in result)


@pytest.mark.unit
def test_create_application(application_repository):
    # Arrange
    create_data = ApplicationCreateSchema(
        staff_id=1,
        location="home",
        reason="Work from home",
        requested_date=datetime.now().date(),
        application_hour="am",
    )
    # Convert to dictionary
    create_data_dict = create_data.model_dump(exclude={"events", "location", "requested_date", "application_hour"})
    print("Create Data Dict:", create_data_dict)  # Debugging: Print the data being passed

    # Act
    result = application_repository.create_application(create_data_dict)

    # Assert
    assert result.staff_id == 1


@pytest.mark.unit
def test_withdraw_application(application_repository):
    # Arrange
    mock_application = Application(application_id=1, staff_id=1, status="pending")
    application_repository.db.applications = [mock_application]
    withdraw_data = ApplicationWithdrawSchema(
        status="withdrawn",
        withdraw_reason="Changed mind",
        editor_id=1,
        application_id=1
    )

    # Act
    result = application_repository.withdraw_application(1, withdraw_data)

    # Assert
    assert result.status == "withdrawn"

@pytest.mark.unit
def test_update_application(application_repository):
    # Arrange
    mock_application = Application(application_id=1, staff_id=1, status="pending")
    application_repository.db.applications = [mock_application]
    update_data = ApplicationCreateSchema(
        staff_id=1,
        location="office",
        reason="Changed plans",
        requested_date=datetime.now().date(),
        application_hour="am",
    )

    # Act
    result = application_repository.update_application(1, update_data)

    # Assert
    assert result.status == "pending"


@pytest.mark.unit
def test_update_application_status(application_repository):
    # Arrange
    mock_application = Application(application_id=1, staff_id=1, status="pending")
    application_repository.db.applications = [mock_application]

    # Act
    result = application_repository.update_application_status(1, "approved", "Status updated to approved")

    # Assert
    assert result.status == "approved"


@pytest.mark.unit
def test_get_pending_applications(application_repository):
    # Arrange
    application_repository.db.applications = [
        Application(application_id=1, staff_id=1, status="pending"),
        Application(application_id=2, staff_id=2, status="approved"),
        Application(application_id=3, staff_id=3, status="pending"),
    ]

    # Act
    result = application_repository.get_pending_applications()

    # Debug print
    print(f"Result type: {type(result)}")
    print(f"Result content: {result}")
    print(f"Result length: {len(result)}")

    # Assert
    assert isinstance(result, list), "Expected result to be a list"

@pytest.mark.unit
def test_update_application_not_found(application_repository):
    # Arrange
    application_repository.db.applications = []  # No applications in the mock database
    update_data = ApplicationCreateSchema(
        staff_id=1,
        location="office",
        reason="Changed plans",
        requested_date=datetime.now().date(),
        application_hour="am",
    )

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        application_repository.update_application(999, update_data)  # Non-existent application_id

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Application not found"


@pytest.mark.unit
def test_update_application_status_not_found(application_repository):
    # Arrange
    application_repository.db.applications = []  # No applications in the mock database

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        application_repository.update_application_status(999, "approved", "Status updated to approved")  # Non-existent application_id

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Application not found"

@pytest.mark.unit
def test_update_application_state(application_repository):
    # Arrange
    mock_application = Application(application_id=1, staff_id=1, status="pending", application_state="initial")
    application_repository.db.applications = [mock_application]

    # Act
    result = application_repository.update_application_state(1, "new_state", "Updated state", "approved")

    # Assert
    assert result.application_state == "new_state"
    assert result.status == "approved"


@pytest.mark.unit
def test_delete_application_not_found(application_repository):
    # Arrange
    application_repository.db.applications = []  # No applications in the mock database

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        application_repository.delete_application(999)  # Non-existent application_id

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Application not found"


@pytest.mark.unit
def test_update_original_application_id(application_repository):
    # Arrange
    mock_application = Application(application_id=1, original_application_id=None)
    application_repository.db.applications = [mock_application]

    # Act
    result = application_repository.update_original_application_id(1, 2)

    # Assert
    assert result.original_application_id == 2


@pytest.mark.unit
def test_delete_application(application_repository):
    # Arrange
    mock_application = Application(application_id=1)
    application_repository.db.applications = [mock_application]

    # Act
    result = application_repository.delete_application(1)

    # Assert
    assert result.application_id == 1
    assert len(application_repository.db.applications) == 0  # Application should be deleted


@pytest.mark.unit
def test_add_event_to_application(application_repository):
    # Arrange
    mock_application = Application(application_id=1, events=[])
    application_repository.db.applications = [mock_application]

    # Initialize the Event without the 'name' argument
    mock_event = Event(event_id=1, location="Location A")  # Specify required attributes

    # Act
    result = application_repository.add_event_to_application(1, mock_event)

    # Assert
    assert len(result.events) == 1
    assert result.events[0].event_id == 1

@pytest.mark.unit
def test_get_applications_by_approver_id(application_repository):
    # Arrange
    mock_applications = [
        Application(application_id=1, approver_id=1),
        Application(application_id=2, approver_id=1),
    ]
    application_repository.db.applications = mock_applications

    # Act
    result = application_repository.get_applications_by_approver_id(1)

    # Assert
    assert len(result) == 2
    assert all(app.approver_id == 1 for app in result)
    assert {app.application_id for app in result} == {1, 2}

@pytest.mark.unit
def test_get_application_status_by_application_id(application_repository):
    # Arrange
    mock_application = Application(application_id=1, status="approved")
    application_repository.db.applications = [mock_application]

    # Act
    result = application_repository.get_application_status_by_application_id(1)

    # Assert
    assert result == "approved"

@pytest.mark.unit
def test_get_application_status_by_application_id_not_found(application_repository):
    # Arrange
    application_repository.db.applications = []  # No applications in the mock database

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        application_repository.get_application_status_by_application_id(999)  # Non-existent application_id

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Application not found"


@pytest.mark.unit
def test_get_applications_by_status(application_repository):
    # Arrange
    application_repository.db.applications = [
        Application(application_id=1, status="pending"),
        Application(application_id=2, status="approved"),
        Application(application_id=3, status="pending")
    ]

    # Mock the filter and order_by to return only pending applications
    def filter_mock(condition):
        return [app for app in application_repository.db.applications if app.status == "pending"]

    application_repository.db.filter = lambda _: application_repository.db
    application_repository.db.order_by = lambda _: filter_mock(None)

    # Act
    result = application_repository.get_applications_by_status("pending")

    # Assert
    assert isinstance(result, list)
    assert len(result) == 2
    assert all(app.status == "pending" for app in result)


@pytest.mark.unit
def test_get_applications_by_status_empty(application_repository):
    # Arrange
    application_repository.db.applications = [
        Application(application_id=1, status="approved"),
        Application(application_id=2, status="approved")
    ]

    # Mock the filter and order_by to return empty list for pending status
    def filter_mock(condition):
        return [app for app in application_repository.db.applications if app.status == "pending"]

    application_repository.db.filter = lambda _: application_repository.db
    application_repository.db.order_by = lambda _: filter_mock(None)

    # Act
    result = application_repository.get_applications_by_status("pending")

    # Assert
    assert isinstance(result, list)
    assert len(result) == 0