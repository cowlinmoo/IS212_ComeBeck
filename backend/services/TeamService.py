from fastapi import Depends

from backend.repositories.TeamRepository import TeamRepository


class TeamService:
    teamRepository = TeamRepository

    def __init__(
            self, teamRepository: TeamRepository = Depends()
    ) -> None:
        self.teamRepository = teamRepository


    # def get_team_employees_by_team_id(self, team_id: int):
    #     return self.teamRepository.get_team_employees_by_team_id(team_id)