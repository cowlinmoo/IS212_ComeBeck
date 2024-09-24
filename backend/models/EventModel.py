from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, Date
from backend.models.BaseModel import EntityMeta
from backend.models.generators import get_current_datetime_sgt

class Event(EntityMeta):
    __tablename__ = 'event'

    event_id = Column(BigInteger, primary_key=True)
    requested_date = Column(Date, nullable=False, default=get_current_datetime_sgt)
    location = Column(String(10), nullable=False)
    application_id = Column(BigInteger, ForeignKey('application.application_id'), nullable=False)