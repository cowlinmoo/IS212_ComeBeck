from typing import List, Type, Optional

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend.config.Database import get_db_connection
from backend.models import Team


class TeamRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)):
        self.db = db

    def get_all_team_ids(self) -> List[int]:
        return [team.team_id for team in self.db.query(Team).all()]

    def get_team_by_id(self, team_id: int) -> Team:
        team = self.db.query(Team).filter(Team.team_id == team_id).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        return team

    def get_team_by_manager_id(self, manager_id: int) -> Team:
        team = self.db.query(Team).filter(Team.manager_id == manager_id).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        return team

    def get_employees_by_team_id(self, team_id: int) -> List[Type[Team]]:
        team = self.get_team_by_id(team_id)
        return team.members

    def get_teams_by_department_id(self, department_id):
        return self.db.query(Team).filter(Team.department_id == department_id).all()

    def get_child_teams(self, parent_team_id: int) -> List[Team]:
        return self.db.query(Team).filter(Team.parent_team_id == parent_team_id).all()

    def get_team(self, team_id: int) -> Optional[Team]:
        return self.db.query(Team).filter(Team.team_id == team_id).first()

    def get_parent_team(self, team_id: int) -> Optional[Team]:
        team = self.get_team_by_id(team_id)
        if team.parent_team_id:
            return self.get_team(team.parent_team_id)
        return None