import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

# Helper function to get the token
def get_bearer_token():
    form_data = {
        "username": "colinmok1000@gmail.com",
        "password": "password123"
    }
    response = client.post("http://localhost:8080/api/authenticate", data=form_data)
    assert response.status_code == 200
    return f"Bearer {response.json()['access_token']}"

# Expected team data in the database
expected_teams = {
    1: {"name": "Executives", "description": "Team for the executive leadership including the CEO.", "manager": {"staff_id": 130002}},
    2: {"name": "Consultants - Ernst Sim's Team", "description": "Team that advises clients on business strategies.", "manager": {"staff_id": 180001}},
    3: {"name": "Engineers - Philip Lee's Team", "description": "Team responsible for product development and software engineering.", "manager": {"staff_id": 151408}},
    4: {"name": "Finance Managers - David Yap's Team", "description": "Team that oversees financial planning and accounting.", "manager": {"staff_id": 170166}},
    # Add additional teams as necessary
}

# Test to get a team by team_id
@pytest.mark.integration
@pytest.mark.parametrize("team_id, expected_data", expected_teams.items())
def test_get_team_by_team_id(team_id, expected_data):
    token = get_bearer_token()
    headers = {"Authorization": token}

    response = client.get(f"/api/team/{team_id}", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()

    # Validate fields in response match expected data for the team
    assert data["team_id"] == team_id, f"Expected team_id {team_id}, got {data['team_id']}"
    assert data["name"] == expected_data["name"], f"Expected name '{expected_data['name']}', got {data['name']}"
    assert data["description"] == expected_data["description"], f"Expected description '{expected_data['description']}', got {data['description']}"

    # Check if manager details are included and correct
    if "manager" in expected_data and expected_data["manager"]:
        assert "manager" in data, "Expected 'manager' field in response"
        assert data["manager"]["staff_id"] == expected_data["manager"]["staff_id"], f"Expected manager staff_id {expected_data['manager']['staff_id']}, got {data['manager']['staff_id']}"

# Test to get a team by manager_id
@pytest.mark.integration
@pytest.mark.parametrize("team_id, expected_data", expected_teams.items())
def test_get_team_by_manager_id(team_id, expected_data):
    token = get_bearer_token()
    headers = {"Authorization": token}

    manager_id = expected_data["manager"]["staff_id"]
    response = client.get(f"/api/team/manager/{manager_id}", headers=headers)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    data = response.json()

    # Validate fields in response match expected data for the team managed by this manager
    assert data["team_id"] == team_id, f"Expected team_id {team_id}, got {data['team_id']}"
    assert data["name"] == expected_data["name"], f"Expected name '{expected_data['name']}', got {data['name']}"
    assert data["description"] == expected_data["description"], f"Expected description '{expected_data['description']}', got {data['description']}"

    # Check if manager details are included and correct
    if "manager" in expected_data and expected_data["manager"]:
        assert "manager" in data, "Expected 'manager' field in response"
        assert data["manager"]["staff_id"] == expected_data["manager"]["staff_id"], f"Expected manager staff_id {expected_data['manager']['staff_id']}, got {data['manager']['staff_id']}"
