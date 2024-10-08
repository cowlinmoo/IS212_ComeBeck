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
    class Config:
        from_attributes = True
class EventResponse(BaseModel):
    event_id: int = Field(examples=[301, 302, 303])
    requested_date: date = Field(examples=[date.today()])
    location: str = Field(examples=["Office A", "Office B", "Home"])
    class Config:
        from_attributes = True