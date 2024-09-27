from datetime import date

from pydantic import BaseModel, Field

class EventSchema(BaseModel):
    event_id: int
    requested_date: date
    location: str
    application_id: int

    class Config:
        from_attributes = True

class EventCreateSchema(BaseModel):
    requested_date: date = Field(examples=[date.today()])