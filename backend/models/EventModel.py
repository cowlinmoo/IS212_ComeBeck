from sqlalchemy import (Column, BigInteger, String, ForeignKey, Date, Enum as
                        SQLAlchemyEnum)
from sqlalchemy.orm import relationship

from backend.models.BaseModel import EntityMeta
from backend.models.enums.ApplicationHourEnum import ApplicationHourEnum
from backend.models.generators import get_current_datetime_sgt


class Event(EntityMeta):
    __tablename__ = 'event'

    event_id = Column(BigInteger, primary_key=True)
    requested_date = Column(Date, nullable=False, default=get_current_datetime_sgt)
    application_hour = Column(SQLAlchemyEnum(ApplicationHourEnum), nullable=False,
                              default = ApplicationHourEnum.FULLDAY)
    location = Column(String(10), nullable=False)
    application_id = Column(BigInteger, ForeignKey('application.application_id'),
                            nullable=False)
    original_event_id = Column(BigInteger, nullable=True)

    application = relationship("Application", back_populates="events")
