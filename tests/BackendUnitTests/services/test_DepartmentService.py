import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException

from backend.services.DepartmentService import DepartmentService
from backend.schemas.DepartmentSchema import DepartmentSchema, TeamSchema
from backend.schemas.BaseSchema import BaseEmployeeInfo, BaseTeamInfo, BaseDepartmentInfo


@pytest.fixture
def mock_repositories():
    return {
        'team_repository': Mock(),
        'department_repository': Mock(),
        'employee_repository': Mock()
    }


@pytest.fixture
def department_service(mock_repositories):
    return DepartmentService(
        team_repository=mock_repositories['team_repository'],
        department_repository=mock_repositories['department_repository'],
        employee_repository=mock_repositories['employee_repository']
    )


class TestDepartmentService:

    @pytest.mark.unit
    def test_get_department_by_department_id_success(self, department_service, mock_repositories):
        # Arrange
        mock_department = Mock()
        mock_department.department_id = 1
        mock_department.name = "Engineering"
        mock_department.description = "Engineering Department"
        mock_department.director_id = 100

        mock_director = Mock()
        mock_director.staff_id = 100
        mock_director.staff_fname = "John"
        mock_director.staff_lname = "Doe"
        mock_director.position = "Software Engineer"
        mock_director.role = 1
        mock_director.team_id = 1
        mock_director.country = "USA"
        mock_director.email = "john.doe@example.com"

        mock_team = Mock()
        mock_team.team_id = 1
        mock_team.name = "Frontend Team"
        mock_team.description = "Frontend Development"
        mock_team.manager_id = 200
        mock_team.parent_team_id = None

        # Create a department mock for the team's department attribute
        mock_team_department = Mock()
        mock_team_department.department_id = 1
        mock_team_department.name = "Engineering"
        mock_team.department = mock_team_department

        mock_repositories['department_repository'].get_department_by_id.return_value = mock_department
        mock_repositories['employee_repository'].get_employee.return_value = mock_director
        mock_repositories['team_repository'].get_teams_by_department_id.return_value = [mock_team]
        mock_repositories['employee_repository'].get_employees_by_team_id.return_value = []
        mock_repositories['team_repository'].get_child_teams.return_value = []

        # Act
        result = department_service.get_department_by_department_id(1)

        # Assert
        assert isinstance(result, DepartmentSchema)
        assert result.department_id == 1
        assert result.name == "Engineering"
        assert result.director.staff_id == 100
        assert len(result.teams) == 1
        assert result.teams[0].name == "Frontend Team"

    @pytest.mark.unit
    def test_get_department_by_department_id_not_found(self, department_service, mock_repositories):
        # Arrange
        mock_repositories['department_repository'].get_department_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            department_service.get_department_by_department_id(999)
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Department not found"

    @pytest.mark.unit
    def test_department_to_schema_without_director(self, department_service, mock_repositories):
        # Arrange
        mock_department = Mock()
        mock_department.department_id = 1
        mock_department.name = "Engineering"
        mock_department.description = "Engineering Department"
        mock_department.director_id = None

        mock_repositories['team_repository'].get_teams_by_department_id.return_value = []

        # Act
        result = department_service.department_to_schema(mock_department)

        # Assert
        assert isinstance(result, DepartmentSchema)
        assert result.department_id == 1
        assert result.director is None
        assert result.teams is None

    @pytest.mark.unit
    def test_team_to_schema_full_hierarchy(self, department_service, mock_repositories):
        # Arrange
        mock_department = Mock()
        mock_department.department_id = 1
        mock_department.name = "Engineering"

        mock_team = Mock()
        mock_team.team_id = 1
        mock_team.name = "Frontend Team"
        mock_team.description = "Frontend Development"
        mock_team.department = mock_department
        mock_team.manager_id = 200
        mock_team.parent_team_id = 2

        mock_parent_team = Mock()
        mock_parent_team.team_id = 2
        mock_parent_team.name = "Development Team"
        mock_parent_team.description = "Development Department"

        mock_manager = Mock()
        mock_manager.staff_id = 200
        mock_manager.staff_fname = "Jane"
        mock_manager.staff_lname = "Smith"
        mock_manager.position = "Team Lead"
        mock_manager.role = 1
        mock_manager.team_id = 1
        mock_manager.country = "USA"
        mock_manager.email = "jane.smith@example.com"


        mock_member = Mock()
        mock_member.staff_id = 300
        mock_member.staff_fname = "Bob"
        mock_member.staff_lname = "Johnson"
        mock_member.position = "Software Engineer"
        mock_member.role = 1
        mock_member.team_id = 1
        mock_member.country = "USA"
        mock_member.email = "bob.johnson@example.com"

        mock_repositories['employee_repository'].get_employee.return_value = mock_manager
        mock_repositories['team_repository'].get_team.return_value = mock_parent_team
        mock_repositories['employee_repository'].get_employees_by_team_id.return_value = [mock_member]
        mock_repositories['team_repository'].get_child_teams.return_value = []

        # Act
        result = department_service.team_to_schema(mock_team)

        # Assert
        assert isinstance(result, TeamSchema)
        assert result.team_id == 1
        assert result.name == "Frontend Team"
        assert result.manager.staff_id == 200
        assert result.parent_team.team_id == 2
        assert len(result.members) == 1
        assert result.members[0].staff_id == 300
        assert result.child_teams is None

    @pytest.mark.unit
    def test_base_schema_conversions(self, department_service):
        # Arrange
        mock_team = Mock()
        mock_team.team_id = 1
        mock_team.name = "Frontend Team"
        mock_team.description = "Frontend Development"

        # Arrange
        mock_employee = Mock()
        mock_employee.staff_id = 100
        mock_employee.staff_fname = "John"
        mock_employee.staff_lname = "Doe"
        mock_employee.position = "Software Engineer"
        mock_employee.role = 1
        mock_employee.team_id = 1
        mock_employee.country = "USA"
        mock_employee.email = "john.doe@example.com"

        mock_department = Mock()
        mock_department.department_id = 1
        mock_department.name = "Engineering"

        # Act
        team_result = department_service.team_to_base_schema(mock_team)
        employee_result = department_service.employee_to_schema(mock_employee)
        department_result = department_service.department_to_base_schema(mock_department)

        # Assert
        assert isinstance(team_result, BaseTeamInfo)
        assert team_result.team_id == 1
        assert team_result.name == "Frontend Team"

        assert isinstance(employee_result, BaseEmployeeInfo)
        assert employee_result.staff_id == 100
        assert employee_result.staff_fname == "John"

        assert isinstance(department_result, BaseDepartmentInfo)
        assert department_result.department_id == 1
        assert department_result.name == "Engineering"

    @pytest.mark.unit
    def test_get_all_departments(self, department_service, mock_repositories):
        # Arrange
        mock_departments = [
            Mock(department_id=1, name="Engineering", description="Engineering Department", director_id=None),
            Mock(department_id=2, name="Sales", description="Sales Department", director_id=None),
            Mock(department_id=3, name="HR", description="Human Resources Department", director_id=None)
        ]

        # Mock the `get_all_departments` return value
        mock_repositories['department_repository'].get_all_departments.return_value = mock_departments

        # Mock the `department_to_schema` method for converting mock departments to schema
        department_service.department_to_schema = Mock(side_effect=[
            DepartmentSchema(department_id=1, name="Engineering", description="Engineering Department",
                             director_id=None),
            DepartmentSchema(department_id=2, name="Sales", description="Sales Department", director_id=None),
            DepartmentSchema(department_id=3, name="HR", description="Human Resources Department", director_id=None)
        ])

        # Act
        result = department_service.get_all_departments()

        # Assert
        assert len(result) == 3
        assert isinstance(result[0], DepartmentSchema)
        assert result[0].department_id == 1
        assert result[0].name == "Engineering"
        assert result[1].department_id == 2
        assert result[1].name == "Sales"
        assert result[2].department_id == 3
        assert result[2].name == "HR"

        # Verify `department_to_schema` was called on each department
        department_service.department_to_schema.assert_any_call(mock_departments[0])
        department_service.department_to_schema.assert_any_call(mock_departments[1])
        department_service.department_to_schema.assert_any_call(mock_departments[2])
        assert department_service.department_to_schema.call_count == 3