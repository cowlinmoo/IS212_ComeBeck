from unittest import mock
import pytest
from fastapi import HTTPException

from backend.models import Team, Employee
from backend.repositories.TeamRepository import TeamRepository

class MockSession:
    def __init__(self):
        self.teams = []

    def query(self, model):
        return self

    def filter(self, condition):
        return self

    def all(self):
        return self.teams

    def first(self):
        return self.teams[0] if self.teams else None

    def get(self, team_id):
        return next((team for team in self.teams if team.team_id == team_id), None)

@pytest.fixture
def team_repository():
    repo = TeamRepository()
    repo.db = MockSession()
    return repo

@pytest.mark.unit
def test_get_all_team_ids(team_repository):
    # Arrange
    mock_teams = [
        Team(team_id=1),
        Team(team_id=2),
        Team(team_id=3)
    ]
    team_repository.db.teams = mock_teams

    # Act
    result = team_repository.get_all_team_ids()

    # Assert
    assert len(result) == 3
    assert result == [1, 2, 3]

@pytest.mark.unit
def test_get_team_by_id(team_repository):
    # Arrange
    mock_team = Team(team_id=1)
    team_repository.db.teams = [mock_team]

    # Act
    result = team_repository.get_team_by_id(1)

    # Assert
    assert result == mock_team
    assert result.team_id == 1

@pytest.mark.unit
def test_get_team_by_id_not_found(team_repository):
    # Arrange
    team_repository.db.teams = []

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        team_repository.get_team_by_id(1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Team not found"

@pytest.mark.unit
def test_get_team_by_manager_id(team_repository):
    # Arrange
    mock_team = Team(team_id=1, manager_id=100)
    team_repository.db.teams = [mock_team]

    # Act
    result = team_repository.get_team_by_manager_id(100)

    # Assert
    assert result == mock_team
    assert result.team_id == 1

@pytest.mark.unit
def test_get_team_by_manager_id_not_found(team_repository):
    # Arrange
    team_repository.db.teams = []

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        team_repository.get_team_by_manager_id(999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Team not found"

@pytest.mark.unit
def test_get_employees_by_team_id(team_repository):
    # Arrange
    member1 = Employee(staff_id=1, staff_fname="Alice", staff_lname="Smith")
    member2 = Employee(staff_id=2, staff_fname="Bob", staff_lname="Johnson")
    mock_team = Team(team_id=1, members=[member1, member2])
    team_repository.db.teams = [mock_team]

    # Act
    result = team_repository.get_employees_by_team_id(1)

    # Assert
    assert result == [member1, member2]
    assert len(result) == 2

@pytest.mark.unit
def test_get_employees_by_team_id_not_found(team_repository):
    # Arrange
    team_repository.db.teams = []

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        team_repository.get_employees_by_team_id(1)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Team not found"

@pytest.mark.unit
def test_get_teams_by_department_id(team_repository):
    # Arrange
    mock_team = Team(team_id=1, department_id=100)
    team_repository.db.teams = [mock_team]

    # Act
    result = team_repository.get_teams_by_department_id(100)

    # Assert
    assert result == [mock_team]
    assert len(result) == 1

@pytest.mark.unit
def test_get_child_teams(team_repository):
    # Arrange
    mock_child_team = Team(team_id=2, parent_team_id=1)
    team_repository.db.teams = [mock_child_team]

    # Act
    result = team_repository.get_child_teams(1)

    # Assert
    assert result == [mock_child_team]
    assert len(result) == 1


@pytest.mark.unit
def test_get_parent_team(team_repository):
    # Arrange
    # Create mock parent and child teams
    mock_parent_team = Team(team_id=1)  # Parent team with ID 1
    mock_child_team = Team(team_id=2, parent_team_id=1)  # Child team with parent ID 1

    # Set up the mock database session with teams
    team_repository.db.teams = [mock_parent_team, mock_child_team]

    # Mocking the get_team_by_id method to return the team based on ID
    def mock_get_team_by_id(team_id):
        return next((team for team in team_repository.db.teams if team.team_id == team_id), None)

    team_repository.get_team_by_id = mock_get_team_by_id  # Mock get_team_by_id

    # Act
    result = team_repository.get_parent_team(2)  # Get parent team for child team with ID 2

    # Assert
    assert result == mock_parent_team  # This should pass if the logic is correct

@pytest.mark.unit
def test_get_parent_team_no_parent(team_repository):
    # Arrange
    mock_team = Team(team_id=1, parent_team_id=None)
    team_repository.db.teams = [mock_team]

    # Act
    result = team_repository.get_parent_team(1)

    # Assert
    assert result is None
