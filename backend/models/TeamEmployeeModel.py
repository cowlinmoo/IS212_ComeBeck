from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from backend.models.BaseModel import EntityMeta

class TeamEmployee(EntityMeta):
    __tablename__ = 'team_employee'

    team_id = Column(ForeignKey('team.team_id'), primary_key=True)
    staff_id = Column(ForeignKey('employees.staff_id'), primary_key=True)

    team = relationship("Team", back_populates="members")
    employee = relationship("Employee", back_populates="team_memberships")