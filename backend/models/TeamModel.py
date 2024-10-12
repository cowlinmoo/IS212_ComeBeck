from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.models import Employee
from backend.models.generators import get_current_datetime_sgt
from backend.models.BaseModel import EntityMeta


class Team(EntityMeta):
    __tablename__ = 'teams'

    team_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    manager_id = Column(Integer, ForeignKey('employees.staff_id'), nullable=True)
    department_id = Column(Integer, ForeignKey('departments.department_id'), nullable=False)
    parent_team_id = Column(Integer, ForeignKey('teams.team_id'), nullable=True)

    department = relationship("Department", back_populates="teams")
    manager = relationship("Employee", foreign_keys=[manager_id], back_populates="managed_team")
    members = relationship("Employee", back_populates="team", foreign_keys="Employee.team_id")
    parent_team = relationship("Team", remote_side=[team_id], back_populates="child_teams")
    child_teams = relationship("Team", back_populates="parent_team")