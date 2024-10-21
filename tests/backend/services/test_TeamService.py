import pytest
from fastapi import HTTPException
from unittest.mock import MagicMock
from backend.models import Team
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

    # Create mock members with required fields
    mock_members = [
        MagicMock(staff_id=3, staff_fname="Bob", staff_lname="Brown"),
        MagicMock(staff_id=4, staff_fname="Charlie", staff_lname="White"),
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


def test_get_team_employees_by_team_id_not_found(team_service):
    # Arrange
    team_id = 999  # Non-existing team ID
    team_service.teamRepository.get_team_by_id.return_value = None

    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        team_service.get_team_employees_by_team_id(team_id)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Team not found"

