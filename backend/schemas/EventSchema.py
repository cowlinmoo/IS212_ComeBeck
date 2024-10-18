from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from backend.models.enums.ApplicationHourEnum import ApplicationHourEnum


class EventSchema(BaseModel):
    event_id: int
    requested_date: date
    location: str
    application_id: int
    application_hour: ApplicationHourEnum = Field(
        examples=[ApplicationHourEnum.FULLDAY, ApplicationHourEnum.AM, ApplicationHourEnum.PM])

    class Config:
        from_attributes = True

class EventCreateSchema(BaseModel):
    requested_date: date = Field(examples=[date.today()])
    application_hour: ApplicationHourEnum = Field(
        examples=[ApplicationHourEnum.FULLDAY, ApplicationHourEnum.AM, ApplicationHourEnum.PM])
    class Config:
        from_attributes = True
class EventResponse(BaseModel):
    event_id: int = Field(examples=[301, 302, 303])
    requested_date: date = Field(examples=[date.today()])
    location: str = Field(examples=["Office A", "Office B", "Home"])
    application_hour: ApplicationHourEnum = Field(
        examples=[ApplicationHourEnum.FULLDAY, ApplicationHourEnum.AM, ApplicationHourEnum.PM])
    class Config:
        from_attributes = True