from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.models.generators import get_current_datetime_sgt
from backend.models.BaseModel import EntityMeta


class Team(EntityMeta):
    __tablename__ = 'team'

    team_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_on = Column(DateTime, default=get_current_datetime_sgt)
    manager_id = Column(Integer, ForeignKey('employees.staff_id'))  # New column

    manager = relationship("Employee", foreign_keys="Team.manager_id", back_populates="managed_teams")
    members = relationship("TeamEmployee", back_populates="team")