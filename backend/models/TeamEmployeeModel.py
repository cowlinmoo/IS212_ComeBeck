from sqlalchemy import Column, ForeignKey
from models import EntityMeta

class TeamEmployee(EntityMeta):
    __tablename__ = 'team_employee'

    team_id = Column(ForeignKey('team.team_id'), primary_key=True)
    staff_id = Column(ForeignKey('employees.staff_id'), primary_key=True)

    class Config:
        orm_mode = True
