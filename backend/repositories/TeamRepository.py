from typing import List, Type

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
