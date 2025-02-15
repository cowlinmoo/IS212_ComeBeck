import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from backend.models import Team, Department, Employee
from backend.repositories.DepartmentRepository import DepartmentRepository
from backend.repositories.EmployeeRepository import EmployeeRepository
from backend.repositories.TeamRepository import TeamRepository
from backend.schemas.TeamSchema import TeamSchema
from backend.schemas.BaseSchema import BaseEmployeeInfo, BaseDepartmentInfo, BaseTeamInfo
from backend.services.TeamService import TeamService


@pytest.fixture
def team_service():
    team_repo = MagicMock(TeamRepository)
    department_repo = MagicMock(DepartmentRepository)
    employee_repo = MagicMock(EmployeeRepository)
    return TeamService(teamRepository=team_repo, departmentRepository=department_repo, employeeRepository=employee_repo)


@pytest.mark.unit
def test_get_team_employees_by_team_id_found(team_service):
    # Arrange
    team_id = 1
    mock_team = Team(
        team_id=team_id,
        name="Development",
        description="Development Team",
        department_id=1,
        manager_id=2,
        parent_team_id=None,  # Assuming no parent team for this test
    )

    # Create mock department with required fields
    mock_department = MagicMock()
    mock_department.department_id = 1
    mock_department.name = "IT Department"

    # Create mock manager with required fields
    mock_manager = MagicMock()
    mock_manager.staff_id = 2  # Required field
    mock_manager.staff_fname = "Alice"  # Required field
    mock_manager.staff_lname = "Smith"  # Required field
    mock_manager.position = "Manager"  # Required field
    mock_manager.role = 1  # Required field
    mock_manager.team_id = 1  # Required field
    mock_manager.country = "USA"  # Required field
    mock_manager.email = "alice.smith@example.com"  # Required field

    # Create mock members with required fields
    mock_members = [
        MagicMock(staff_id=3, staff_fname="Bob", staff_lname="Brown", team_id=1, role=2, country="USA", email="bob.brown@example.com", position="Developer"),
        MagicMock(staff_id=4, staff_fname="Charlie", staff_lname="White", team_id=1, role=2, country="USA", email="charlie.white@example.com", position="Developer"),
    ]

    # Setup mocks
    team_service.teamRepository.get_team_by_id.return_value = mock_team
    team_service.departmentRepository.get_department_by_id.return_value = mock_department
    team_service.employeeRepository.get_employee.return_value = mock_manager
    team_service.employeeRepository.get_employees_by_team_id.return_value = mock_members

    # Define orm_to_dict for testing
    def orm_to_dict(obj):
        if obj is None:
            return {}
        return {
            "department_id": getattr(obj, "department_id", None),
            "name": getattr(obj, "name", None),
            "staff_id": getattr(obj, "staff_id", None),
            "staff_fname": getattr(obj, "staff_fname", None),
            "staff_lname": getattr(obj, "staff_lname", None),
            "position": getattr(obj, "position", None),
            "role": getattr(obj, "role", None),
            "team_id": getattr(obj, "team_id", None),
            "country": getattr(obj, "country", None),
            "email": getattr(obj, "email", None)
        }

    # Patch the function in TeamService for testing
    team_service.team_to_schema = lambda team: {
        "team_id": team.team_id,
        "name": team.name,
        "description": team.description,
        "department": BaseDepartmentInfo.model_validate(orm_to_dict(mock_department)),
        "manager": BaseEmployeeInfo.model_validate(orm_to_dict(mock_manager)),
        "parent_team": None,  # Assuming parent_team is None for this test
        "child_teams": None,  # Assuming no child teams for this test
        "members": [
            BaseEmployeeInfo.model_validate(orm_to_dict(member)) for member in mock_members
        ],
    }

    # Act
    result = team_service.get_team_employees_by_team_id(team_id)

    # Assert
    assert result["team_id"] == team_id
    assert result["name"] == "Development"
    assert result["description"] == "Development Team"

    # Access department attributes directly
    department = result["department"]
    assert department.department_id == 1
    assert department.name == "IT Department"

    # Access manager attributes directly
    manager = result["manager"]
    assert manager.staff_id == 2
    assert manager.staff_fname == "Alice"
    assert manager.staff_lname == "Smith"

    # Validate team members
    assert len(result["members"]) == 2
    assert result["members"][0].staff_id == 3
    assert result["members"][0].staff_fname == "Bob"
    assert result["members"][0].staff_lname == "Brown"
    assert result["members"][1].staff_id == 4
    assert result["members"][1].staff_fname == "Charlie"
    assert result["members"][1].staff_lname == "White"


@pytest.mark.unit
def test_get_team_employees_by_team_id_not_found(team_service):
    # Arrange
    team_id = 999  # Non-existing team ID
    team_service.teamRepository.get_team_by_id.return_value = None

    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        team_service.get_team_employees_by_team_id(team_id)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Team not found"


@pytest.mark.unit
def test_team_to_schema(team_service):
    # Arrange
    team_id = 1
    mock_team = Team(
        team_id=team_id,
        name="Development",
        description="Development Team",
        department_id=1,
        manager_id=2,
    )

    # Use actual ORM model classes for mock department and manager
    mock_department = Department(department_id=1, name="IT Department")
    mock_manager = Employee(staff_id=2, staff_fname="Alice", staff_lname="Smith", position="Manager", role=1, team_id=1, country="USA", email="alice.smith@example.com",department_id=1)

    # Create mock members using the actual ORM model if applicable
    mock_members = [
        Employee(staff_id=3, staff_fname="Bob", staff_lname="Brown", team_id=1, role=2, country="USA", email="bob.brown@example.com", position="Developer", department_id=1),
        Employee(staff_id=4, staff_fname="Charlie", staff_lname="White", team_id=1, role=2, country="USA", email="charlie.white@example.com", position="Developer", department_id=1),
    ]

    # Setup mocks for the repositories
    team_service.departmentRepository.get_department_by_id.return_value = mock_department
    team_service.employeeRepository.get_employee.return_value = mock_manager
    team_service.employeeRepository.get_employees_by_team_id.return_value = mock_members

    # Act
    result = team_service.team_to_schema(mock_team)

    # Assert
    assert result.team_id == mock_team.team_id
    assert result.name == mock_team.name
    assert result.description == mock_team.description

    # Validate the members
    assert len(result.members) == 2
    assert result.members[0].staff_id == 3
    assert result.members[0].staff_fname == "Bob"
    assert result.members[1].staff_id == 4
    assert result.members[1].staff_fname == "Charlie"

@pytest.mark.unit
def test_get_team_employees_by_manager_id_found(team_service):
    # Arrange
    manager_id = 2
    mock_manager = MagicMock()
    mock_manager.staff_id = manager_id
    mock_team = Team(
        team_id=1,
        name="Development",
        description="Development Team",
        department_id=1,
        manager_id=manager_id
    )

    # Set up the return values for the mocks
    team_service.employeeRepository.get_employee.return_value = mock_manager
    team_service.teamRepository.get_team_by_manager_id.return_value = mock_team

    # Patch the `team_to_schema` method to simplify the test
    team_service.team_to_schema = MagicMock(return_value={"team_id": mock_team.team_id, "name": mock_team.name})

    # Act
    result = team_service.get_team_employees_by_manager_id(manager_id)

    # Assert
    assert result["team_id"] == mock_team.team_id
    assert result["name"] == mock_team.name
    team_service.team_to_schema.assert_called_once_with(mock_team)

@pytest.mark.unit
def test_get_team_employees_by_manager_id_manager_not_found(team_service):
    # Arrange
    manager_id = 999  # Non-existing manager ID
    team_service.employeeRepository.get_employee.return_value = None

    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        team_service.get_team_employees_by_manager_id(manager_id)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Manager not found"

@pytest.mark.unit
def test_get_team_employees_by_manager_id_team_not_found(team_service):
    # Arrange
    manager_id = 2
    mock_manager = MagicMock()
    mock_manager.staff_id = manager_id

    # Mock employee retrieval for manager
    team_service.employeeRepository.get_employee.return_value = mock_manager
    team_service.teamRepository.get_team_by_manager_id.return_value = None

    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        team_service.get_team_employees_by_manager_id(manager_id)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Team not found"
