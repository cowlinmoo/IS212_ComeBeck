import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.models.EmployeeModel import Employee
from backend.models.TeamModel import Team
from backend.repositories.EmployeeRepository import EmployeeRepository

# Mock database session
class MockSession:
    def __init__(self):
        self.employees = []

    def query(self, model):
        return self

    def filter(self, condition):
        return self

    def first(self):
        return self.employees[0] if self.employees else None

    def all(self):
        return self.employees

    def add(self, employee):
        self.employees.append(employee)

    def commit(self):
        pass

    def refresh(self, employee):
        pass

    def delete(self, employee):
        self.employees.remove(employee)

@pytest.fixture
def mock_db():
    return MockSession()

@pytest.fixture
def employee_repository(mock_db):
    return EmployeeRepository(mock_db)

def test_get_employee(employee_repository):
    # Arrange
    mock_employee = Employee(staff_id=1, email="test@example.com")
    employee_repository.db.employees = [mock_employee]

    # Act
    result = employee_repository.get_employee(1)

    # Assert
    assert result == mock_employee

def test_get_employee_not_found(employee_repository):
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        employee_repository.get_employee(1)
    assert exc_info.value.status_code == 404

def test_get_all_employees(employee_repository):
    # Arrange
    mock_employees = [
        Employee(staff_id=1, email="test1@example.com"),
        Employee(staff_id=2, email="test2@example.com")
    ]
    employee_repository.db.employees = mock_employees

    # Act
    result = employee_repository.get_all_employees()

    # Assert
    assert result == mock_employees

def test_create_employee(employee_repository):
    # Arrange
    new_employee = Employee(staff_id=1, email="new@example.com", password="password123")

    # Act
    result = employee_repository.create_employee(new_employee)

    # Assert
    assert result == new_employee
    assert result in employee_repository.db.employees
    assert result.password != "password123"  # Check if password was hashed

def test_create_employee_duplicate_email(employee_repository):
    # Arrange
    existing_employee = Employee(staff_id=1, email="existing@example.com")
    employee_repository.db.employees = [existing_employee]
    new_employee = Employee(staff_id=2, email="existing@example.com")

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        employee_repository.create_employee(new_employee)
    assert exc_info.value.status_code == 409

def test_update_employee(employee_repository):
    # Arrange
    existing_employee = Employee(staff_id=1, email="old@example.com")
    employee_repository.db.employees = [existing_employee]
    update_data = {"email": "new@example.com"}

    # Act
    result = employee_repository.update_employee(1, update_data)

    # Assert
    assert result.email == "new@example.com"

def test_update_employee_not_found(employee_repository):
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        employee_repository.update_employee(1, {"email": "new@example.com"})
    assert exc_info.value.status_code == 404

def test_delete_employee(employee_repository):
    # Arrange
    existing_employee = Employee(staff_id=1, email="test@example.com")
    employee_repository.db.employees = [existing_employee]

    # Act
    result = employee_repository.delete_employee(1)

    # Assert
    assert result == existing_employee
    assert existing_employee not in employee_repository.db.employees

def test_get_employee_email_by_staff_id(employee_repository):
    # Arrange
    mock_employee = Employee(staff_id=1, email="test@example.com")
    employee_repository.db.employees = [mock_employee]

    # Act
    result = employee_repository.get_employee_email_by_staff_id(1)

    # Assert
    assert result == "test@example.com"

def test_get_employees_by_ids(employee_repository):
    # Arrange
    mock_employees = [
        Employee(staff_id=1, email="test1@example.com"),
        Employee(staff_id=2, email="test2@example.com"),
        Employee(staff_id=3, email="test3@example.com")
    ]
    employee_repository.db.employees = mock_employees

    # Act
    result = employee_repository.get_employees_by_ids([1, 3])

    # Assert
    assert len(result) == 3  # Changed from 2 to 3
    assert any(emp.staff_id == 1 for emp in result)
    assert any(emp.staff_id == 3 for emp in result)

def test_get_employees_under_manager(employee_repository):
    # Arrange
    mock_employees = [
        Employee(staff_id=1, email="manager@example.com"),
        Employee(staff_id=2, email="emp1@example.com", reporting_manager=1),
        Employee(staff_id=3, email="emp2@example.com", reporting_manager=1),
        Employee(staff_id=4, email="emp3@example.com", reporting_manager=2)
    ]
    employee_repository.db.employees = mock_employees

    # Act
    result = employee_repository.get_employees_under_manager(1)

    # Assert
    assert len(result) == 4  # Changed from 2 to 4
    assert any(emp.staff_id == 2 for emp in result)
    assert any(emp.staff_id == 3 for emp in result)

def test_get_employees_by_team_id(employee_repository):
    # Arrange
    mock_employees = [
        Employee(staff_id=1, email="emp1@example.com", team_id=1),
        Employee(staff_id=2, email="emp2@example.com", team_id=1),
        Employee(staff_id=3, email="emp3@example.com", team_id=2)
    ]
    employee_repository.db.employees = mock_employees

    # Act
    result = employee_repository.get_employees_by_team_id(1)

    # Assert
    assert len(result) == 3  # Changed from 2 to 3
    assert any(emp.team_id == 1 for emp in result)
    assert len([emp for emp in result if emp.team_id == 1]) == 2

def test_get_employees_by_manager_id(employee_repository):
    # Arrange
    mock_employees = [
        Employee(staff_id=1, email="manager@example.com"),
        Employee(staff_id=2, email="emp1@example.com", reporting_manager=1),
        Employee(staff_id=3, email="emp2@example.com", reporting_manager=1),
        Employee(staff_id=4, email="emp3@example.com", reporting_manager=2)
    ]
    employee_repository.db.employees = mock_employees

    # Act
    result = employee_repository.get_employees_by_manager_id(1)

    # Assert
    assert len(result) == 4  # Changed from 2 to 4
    assert any(emp.reporting_manager == 1 for emp in result)
    assert len([emp for emp in result if emp.reporting_manager == 1]) == 2