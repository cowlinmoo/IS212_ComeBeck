from sqlalchemy import Column, Integer, String, Text, DateTime
from generators import get_current_datetime_sgt
from models import EntityMeta


class Team(EntityMeta):
    __tablename__ = 'team'

    team_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_on = Column(DateTime, default=get_current_datetime_sgt)

    class Config:
        orm_mode = True
