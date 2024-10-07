from typing import List, Type

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.config.Database import get_db_connection
from backend.models import TeamEmployee


class TeamEmployeeRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)):
        self.db = db
    def get_team_employees_by_team_id(self, team_id: int) -> List[Type[TeamEmployee]]:
        return self.db.query(TeamEmployee).filter(TeamEmployee.team_id == team_id).all()
