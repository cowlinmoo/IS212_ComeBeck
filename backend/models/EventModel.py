from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime
from backend.models.BaseModel import EntityMeta
from backend.models.generators import get_current_datetime_sgt


class Event(EntityMeta):
    __tablename__ = 'event'

    event_id = Column(BigInteger, primary_key=True)
    datetime = Column(DateTime, nullable=False,
                      default=get_current_datetime_sgt)
    location = Column(String(10), nullable=False)
    arrangement_id = Column(BigInteger, ForeignKey(
        'arrangement.arrangement_id'), nullable=False)

    class Config:
        orm_mode = True
