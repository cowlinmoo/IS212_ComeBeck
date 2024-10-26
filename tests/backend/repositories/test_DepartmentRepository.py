from unittest import mock

import pytest
from fastapi import HTTPException

from backend.models import Employee
from backend.models.Department import Department
from backend.repositories.DepartmentRepository import DepartmentRepository

class MockSession:
    def __init__(self):
        self.departments = []

    def query(self, model):
        return self

    def filter(self, condition):
        return self

    def all(self):
        return self.departments

    def first(self):
        return self.departments[0] if self.departments else None

@pytest.fixture
def department_repository():
    repo = DepartmentRepository()
    repo.db = MockSession()
    return repo

def test_get_all_department_ids(department_repository):
    # Arrange
    mock_departments = [
        Department(department_id=1),
        Department(department_id=2),
        Department(department_id=3)
    ]
    department_repository.db.departments = mock_departments

    # Act
    result = department_repository.get_all_department_ids()

    # Assert
    assert len(result) == 3
    assert result == [1, 2, 3]

def test_get_all_department(department_repository):
    # Arrange
    mock_departments = [
        Department(department_id=1),
        Department(department_id=2),
        Department(department_id=3)
    ]
    department_repository.db.departments = mock_departments

    # Act
    result = department_repository.get_all_departments()

    # Assert
    assert len(result) == 3
    assert result == mock_departments

def test_get_department_by_id(department_repository):
    # Arrange
    mock_department = Department(department_id=1)
    department_repository.db.departments = [mock_department]

    # Act
    result = department_repository.get_department_by_id(1)

    # Assert
    assert result == mock_department
    assert result.department_id == 1

def test_get_department_by_id_not_found(department_repository):
    # Arrange
    department_repository.db.departments = []

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        department_repository.get_department_by_id(1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Department not found"

def test_get_department_by_director_id(department_repository):
    # Arrange
    mock_department = Department(department_id=1, director_id=100)
    department_repository.db.departments = [mock_department]

    # Act
    result = department_repository.get_department_by_director_id(100)

    # Assert
    assert result == mock_department  # Change 'mock' to 'mock_department'
    assert result.department_id == 1

def test_get_department_by_director_id_not_found(department_repository):
    # Arrange
    department_repository.db.departments = []

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        department_repository.get_department_by_director_id(999)  # Using a non-existent ID

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Department not found"


def test_get_employees_by_department_id(department_repository):
    # Arrange
    employee1 = Employee(staff_id=1, staff_fname="Alice", staff_lname="Smith",
                         position="Developer", department_id=1, team_id=1,
                         country="USA", email="alice@example.com",
                         reporting_manager=None, role=2, password="hashed_password")

    employee2 = Employee(staff_id=2, staff_fname="Bob", staff_lname="Johnson",
                         position="Designer", department_id=1, team_id=1,
                         country="USA", email="bob@example.com",
                         reporting_manager=None, role=2, password="hashed_password")

    mock_department = Department(department_id=1, employees=[employee1, employee2])
    department_repository.db.departments = [mock_department]

    # Act
    result = department_repository.get_employees_by_department_id(1)

    # Assert
    assert result == [employee1, employee2]  # Ensure the result is correct
    assert len(result) == 2  # Check the count of employees


def test_get_employees_by_department_id_not_found(department_repository):
    # Arrange
    department_repository.db.departments = []  # No departments available

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        department_repository.get_employees_by_department_id(1)  # Using a non-existent ID

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Department not found"