import pytest
from unittest.mock import Mock, patch, call
from fastapi import HTTPException

from backend.models import Employee, Team, Department
from backend.services.EmployeeService import EmployeeService
from backend.schemas.EmployeeSchema import EmployeeCreateSchema, EmployeeUpdateSchema
from backend.schemas.BaseSchema import BaseEmployeeSchema, BaseDepartmentInfo, BaseTeamInfo


@pytest.fixture
def mock_employee_repository():
    return Mock()


@pytest.fixture
def mock_team_repository():
    return Mock()


@pytest.fixture
def mock_department_repository():
    return Mock()


@pytest.fixture
def employee_service(mock_employee_repository, mock_team_repository, mock_department_repository):
    return EmployeeService(
        employeeRepository=mock_employee_repository,
        teamRepository=mock_team_repository,
        departmentRepository=mock_department_repository
    )


@pytest.fixture
def sample_employee():
    return Employee(
        staff_id=1,
        staff_fname="John",
        staff_lname="Doe",
        position="Software Engineer",
        department_id=1,
        team_id=1,
        country="US",
        email="john.doe@example.com",
        reporting_manager=2,
        role=1,
        password="hashed_password"
    )


@pytest.fixture
def sample_team():
    return Team(
        team_id=1,
        name="Engineering Team",
        description="Main engineering team",
        manager_id=2,
        department_id=1,
        parent_team_id=None
    )


@pytest.fixture
def sample_department():
    return Department(
        department_id=1,
        name="Engineering",
        description="Engineering department",
        director_id=3
    )


class TestEmployeeService:
    def test_get_all_employees(self, employee_service, mock_employee_repository,
                               mock_department_repository, mock_team_repository,
                               sample_employee, sample_department, sample_team):
        # Arrange
        mock_employee_repository.get_all_employees.return_value = [sample_employee]
        mock_employee_repository.get_employees_by_manager_id.return_value = []
        mock_department_repository.get_department_by_id.return_value = sample_department
        mock_team_repository.get_team_by_id.return_value = sample_team
        mock_team_repository.get_team_by_manager_id.side_effect = HTTPException(status_code=404,
                                                                                detail="Team not found")
        mock_department_repository.get_department_by_director_id.side_effect = HTTPException(status_code=404,
                                                                                             detail="Department not found")

        # Act
        result = employee_service.get_all_employees()

        # Assert
        assert len(result) == 1
        assert result[0].staff_id == sample_employee.staff_id
        assert result[0].department.department_id == sample_department.department_id
        assert result[0].team.team_id == sample_team.team_id

    def test_create_employee_success(self, employee_service, mock_employee_repository,
                                     mock_team_repository, mock_department_repository,
                                     sample_team, sample_employee, sample_department):
        # Arrange
        employee_create_data = EmployeeCreateSchema(
            staff_fname="John",
            staff_lname="Doe",
            position="Software Engineer",
            team_id=1,
            country="US",
            email="john.doe@example.com",
            role=1,
            password="password123"
        )

        # Set up all necessary mock returns
        mock_team_repository.get_team_by_id.return_value = sample_team
        mock_employee_repository.create_employee.return_value = sample_employee
        mock_employee_repository.get_employees_by_manager_id.return_value = []
        mock_department_repository.get_department_by_id.return_value = sample_department

        # Mock additional relationships that might be needed
        mock_team_repository.get_team_by_manager_id.side_effect = HTTPException(
            status_code=404, detail="Team not found"
        )
        mock_department_repository.get_department_by_director_id.side_effect = HTTPException(
            status_code=404, detail="Department not found"
        )

        # Act
        result = employee_service.create_employee(employee_create_data)

        # Assert
        assert result.staff_id == sample_employee.staff_id
        # Verify get_team_by_id was called twice with the same argument
        assert mock_team_repository.get_team_by_id.call_count == 2

    def test_create_employee_duplicate_email(self, employee_service, mock_employee_repository,
                                             mock_team_repository, sample_team):
        # Arrange
        employee_create_data = EmployeeCreateSchema(
            staff_fname="John",
            staff_lname="Doe",
            position="Software Engineer",
            team_id=1,
            country="US",
            email="existing@example.com",
            role=1,
            password="password123"
        )
        mock_team_repository.get_team_by_id.return_value = sample_team
        mock_employee_repository.create_employee.side_effect = HTTPException(
            status_code=409, detail="Employee with this email already exists"
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            employee_service.create_employee(employee_create_data)
        assert exc.value.status_code == 409
        assert exc.value.detail == "Employee with this email already exists"

    def test_create_employee_team_not_found(self, employee_service, mock_employee_repository,
                                            mock_team_repository):
        # Arrange
        employee_create_data = EmployeeCreateSchema(
            staff_fname="John",
            staff_lname="Doe",
            position="Software Engineer",
            team_id=1,
            country="US",
            email="john.doe@example.com",
            role=1,
            password="password123"
        )

        # Simulate that the team does not exist
        mock_team_repository.get_team_by_id.return_value = None  # Change here

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            employee_service.create_employee(employee_create_data)

        assert exc.value.status_code == 404
        assert exc.value.detail == "Team ID does not exist"

    def test_create_employee_team_no_manager(self, employee_service, mock_employee_repository,
                                            mock_team_repository, sample_team):
        # Arrange
        employee_create_data = EmployeeCreateSchema(
            staff_fname="John",
            staff_lname="Doe",
            position="Software Engineer",
            team_id=1,
            country="US",
            email="john.doe@example.com",
            role=1,
            password="password123"
        )
        mock_team_repository.get_team_by_id.return_value = sample_team
        sample_team.manager_id = None
        mock_employee_repository.create_employee.side_effect = HTTPException(
            status_code=404, detail="Team has no manager assigned"
        )
        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            employee_service.create_employee(employee_create_data)

    def test_update_employee_success(self, employee_service, mock_employee_repository,
                                     mock_team_repository, mock_department_repository,
                                     sample_team, sample_employee, sample_department):
        # Arrange
        update_data = EmployeeUpdateSchema(
            staff_fname="Jane",
            staff_lname="Doe",
            team_id=1,
            role=1,
            position="Software Engineer",
            country="US",
            email="jane.doe@example.com",
        )
        mock_team_repository.get_team_by_id.return_value = sample_team
        mock_employee_repository.update_employee.return_value = sample_employee
        mock_employee_repository.get_employees_by_manager_id.return_value = []
        mock_department_repository.get_department_by_id.return_value = sample_department
        mock_team_repository.get_team_by_manager_id.side_effect = HTTPException(status_code=404,
                                                                                detail="Team not found")
        mock_department_repository.get_department_by_director_id.side_effect = HTTPException(status_code=404,
                                                                                             detail="Department not found")

        # Act
        result = employee_service.update_employee(1, update_data)

        # Assert
        expected_update_data = {
            'staff_fname': 'Jane',
            'staff_lname': 'Doe',
            'position': 'Software Engineer',
            'role': 1,
            'country': 'US',
            'email': 'jane.doe@example.com',
            'team_id': 1,
            'department_id': sample_team.department_id,
            'reporting_manager': sample_team.manager_id
        }
        mock_employee_repository.update_employee.assert_called_once_with(1, expected_update_data)
        assert result.staff_id == sample_employee.staff_id

    def test_update_employee_team_not_found(self, employee_service, mock_employee_repository,
                                            mock_team_repository, sample_employee):
        # Arrange
        update_data = EmployeeUpdateSchema(
            staff_fname="Jane",
            staff_lname="Doe",
            team_id=1,
            role=1,
            position="Software Engineer",
            country="US",
            email="jane.doe@example.com",
        )
        mock_team_repository.get_team_by_id.return_value = None
        mock_employee_repository.update_employee.side_effect = HTTPException(
            status_code=404, detail="Team ID does not exist")

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            employee_service.update_employee(1, update_data)

    def test_update_employee_team_no_manager(self, employee_service, mock_employee_repository,
                                            mock_team_repository, sample_team):
        # Arrange
        update_data = EmployeeUpdateSchema(
            staff_fname="Jane",
            staff_lname="Doe",
            team_id=1,
            role=1,
            position="Software Engineer",
            country="US",
            email="jane.doe@example.com",
        )
        mock_team_repository.get_team_by_id.return_value = sample_team
        sample_team.manager_id = None
        mock_employee_repository.update_employee.side_effect = HTTPException(
            status_code=404, detail="Team has no manager assigned")
        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            employee_service.update_employee(1, update_data)

    def test_employee_to_schema_with_all_relationships(self, employee_service,
                                                       mock_employee_repository,
                                                       mock_department_repository,
                                                       mock_team_repository,
                                                       sample_employee,
                                                       sample_department,
                                                       sample_team):
        # Arrange
        direct_report = Employee(
            staff_id=4,
            staff_fname="Direct",
            staff_lname="Report",
            position="Junior Engineer",
            department_id=1,
            team_id=1,
            country="US",
            email="direct.report@example.com",
            reporting_manager=1,
            role=1,
            password="hashed_password"
        )

        mock_department_repository.get_department_by_id.return_value = sample_department
        mock_team_repository.get_team_by_id.return_value = sample_team
        mock_team_repository.get_team_by_manager_id.return_value = sample_team
        mock_employee_repository.get_employees_by_manager_id.return_value = [direct_report]
        mock_department_repository.get_department_by_director_id.return_value = sample_department

        # Act
        result = employee_service.employee_to_schema(sample_employee)

        # Assert
        assert result.staff_id == sample_employee.staff_id
        assert result.department.department_id == sample_department.department_id
        assert result.team.team_id == sample_team.team_id
        assert result.managed_team.team_id == sample_team.team_id
        assert result.directed_department.department_id == sample_department.department_id
        assert len(result.direct_reports) == 1
        assert result.direct_reports[0].staff_id == direct_report.staff_id

    def test_delete_employee_success(self, employee_service, mock_employee_repository, sample_employee):
        # Arrange
        mock_employee_repository.get_employee.return_value = sample_employee
        mock_employee_repository.delete_employee.return_value = sample_employee

        # Act
        result = employee_service.delete_employee_by_staff_id(1)

        # Assert
        assert result.staff_id == sample_employee.staff_id
        mock_employee_repository.delete_employee.assert_called_once_with(1)

    def test_delete_employee_not_found(self, employee_service, mock_employee_repository):
        # Arrange
        mock_employee_repository.delete_employee.side_effect = HTTPException(
            status_code=404, detail="Employee not found"
        )

        # Act & Assert
        with pytest.raises(HTTPException) as exc:
            employee_service.delete_employee_by_staff_id(999)
        assert exc.value.status_code == 404
        assert exc.value.detail == "Employee not found"

    def test_get_one_employee(self, employee_service, mock_employee_repository,
                              mock_department_repository, mock_team_repository,
                              sample_employee, sample_department, sample_team):
        # Arrange
        mock_employee_repository.get_employee.return_value = sample_employee
        mock_employee_repository.get_employees_by_manager_id.return_value = []
        mock_department_repository.get_department_by_id.return_value = sample_department
        mock_team_repository.get_team_by_id.return_value = sample_team
        mock_team_repository.get_team_by_manager_id.side_effect = HTTPException(status_code=404,
                                                                                detail="Team not found")
        mock_department_repository.get_department_by_director_id.side_effect = HTTPException(status_code=404,
                                                                                             detail="Department not found")

        # Act
        result = employee_service.get_employee_by_staff_id(1)

        # Assert
        assert result.staff_id == sample_employee.staff_id
        assert result.department.department_id == sample_department.department_id
        assert result.team.team_id == sample_team.team_id