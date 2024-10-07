from fastapi import Depends

from backend.repositories.TeamEmployeeRepository import TeamEmployeeRepository


class TeamService:
    teamEmployeeRepository = TeamEmployeeRepository

    def __init__(
            self, teamEmployeeRepository: TeamEmployeeRepository = Depends()
    ) -> None:
        self.teamEmployeeRepository = teamEmployeeRepository


    def get_team_employees_by_team_id(self, team_id: int):
        return self.teamEmployeeRepository.get_team_employees_by_team_id(team_id)