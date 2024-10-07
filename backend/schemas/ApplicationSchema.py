from pydantic import BaseModel, Field, validator, field_validator, model_validator
from datetime import datetime, date, timedelta
from typing import Optional, List

from backend.models.enums import EventLocationEnum
from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.models.enums.RecurrenceType import RecurrenceType

import logging

from backend.schemas.EventSchema import EventCreateSchema, EventResponse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ApplicationSchema(BaseModel):
    application_id: int = Field(examples=[201, 202, 203])
    reason: str = Field(
        examples=["Vacation request", "Sick leave", "Personal day"])
    requested_date: date = Field(examples=[date.today()])
    description: Optional[str] = Field(
        default=None, examples=["Going on a family vacation", "Doctor's appointment"])
    created_on: datetime = Field(examples=[datetime.now()])
    last_updated_on: Optional[datetime] = Field(
        default=None, examples=[datetime.now()])
    status: str = Field(
        examples=["pending", "approved", "rejected", "withdrawn"])
    staff_id: int = Field(examples=[101, 102, 103])
    approver_id: Optional[int] = Field(default=None, examples=[101, 102, 103])
    recurring: bool = Field(examples=[True, False])

    class Config:
        from_attributes = True


class ApplicationResponse(BaseModel):
    application_id: int = Field(examples=[201, 202, 203])
    reason: str = Field(
        examples=["Vacation request", "Sick leave", "Personal day"])
    description: Optional[str] = Field(
        default=None, examples=["Going on a family vacation", "Doctor's appointment"])
    created_on: datetime = Field(examples=[datetime.now()])
    last_updated_on: Optional[datetime] = Field(
        default=None, examples=[datetime.now()])
    status: str = Field(
        examples=["pending", "approved", "rejected", "withdrawn"])
    staff_id: int = Field(examples=[101, 102, 103])
    approver_id: Optional[int] = Field(default=None, examples=[101, 102, 103])
    recurring: bool = Field(examples=[True, False])
    events: List[EventResponse] = Field(default_factory=list)


class ApplicationCreateSchema(BaseModel):
    location: str = Field(examples=["Home", "Office", "Remote"])
    reason: str = Field(
        examples=["Vacation request", "Sick leave", "Personal day"])
    requested_date: date = Field(examples=[date.today()])
    description: Optional[str] = Field(
        default=None, examples=["Going on a family vacation", "Doctor's appointment"])
    staff_id: int = Field(examples=[101, 102, 103])
    recurring: bool = Field(default=False, examples=[True, False])
    recurrence_type: Optional[RecurrenceType] = Field(default=None, examples=[
                                                      RecurrenceType.DAILY, RecurrenceType.WEEKLY, RecurrenceType.MONTHLY])
    end_date: Optional[date] = Field(
        default=None, examples=[date.today() + timedelta(days=7)])
    events: List[EventCreateSchema] = Field(default=[],
                                            examples=[
        [
            {"requested_date": date.today()},
            {"requested_date": date.today() + timedelta(days=3)}
        ]
    ])

    @model_validator(mode='after')
    def set_end_date(self):
        if self.end_date is None:
            self.end_date = self.requested_date
        return self

    class Config:
        validate_assignment = True


class ApplicationUpdateSchema(BaseModel):
    reason: Optional[str] = Field(default=None, examples=[
                                  "Vacation request", "Sick leave", "Personal day"])
    requested_date: date = Field(examples=[date.today()])
    description: Optional[str] = Field(
        default=None, examples=["Going on a family vacation", "Doctor's appointment"])
    status: Optional[str] = Field(default=None, examples=[
                                  "pending", "approved", "rejected", "withdrawn"])
    approver_id: Optional[int] = Field(default=None, examples=[101, 102, 103])


class ApplicationWithdrawSchema(BaseModel):
    status: str = Field(examples=["withdrawn"])
    staff_id: int = Field(examples=[101, 102, 103])
    application_id: int = Field(examples=[201, 202, 203])
    withdraw_reason: Optional[str] = Field(
        default=None, examples=["Personal reasons", "Change of plans"])


class ApprovedApplicationLocationSchema(BaseModel):
    employee_fname: str
    employee_lname: str
    location: str
    position: str
    date:str
