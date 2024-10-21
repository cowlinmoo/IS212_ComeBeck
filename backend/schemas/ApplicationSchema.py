from pydantic import BaseModel, Field, validator, field_validator, model_validator
from datetime import datetime, date, timedelta
from typing import Optional, List

from backend.models.enums import EventLocationEnum
from backend.models.enums.ApplicationHourEnum import ApplicationHourEnum
from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.models.enums.RecurrenceType import RecurrenceType

import logging

from backend.schemas.BaseSchema import BaseEmployeeInfo
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
    staff: BaseEmployeeInfo = Field(default_factory=BaseEmployeeInfo)
    application_id: int = Field(examples=[201, 202, 203])
    application_state: Optional[str] = Field(default=None, examples=["new_application", "cancel_one_request", "cancel_request", "change_request"])
    reason: str = Field(
        examples=["Vacation request", "Sick leave", "Personal day"])
    description: Optional[str] = Field(
        default=None, examples=["Going on a family vacation", "Doctor's appointment"])
    created_on: datetime = Field(examples=[datetime.now()])
    last_updated_on: Optional[datetime] = Field(
        default=None, examples=[datetime.now()])
    staff_id: int = Field(examples=[101, 102, 103])
    status: str = Field(examples=["pending", "approved", "rejected", "withdrawn"])
    approver_id: Optional[int] = Field(default=None, examples=[101, 102, 103])
    recurring: bool = Field(examples=[True, False])
    events: List[EventResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True

class ApplicationCreateSchema(BaseModel):
    location: str = Field(examples=["Home", "Office", "Remote"])
    reason: str = Field(
        examples=["Vacation request", "Sick leave", "Personal day"])
    requested_date: date = Field(examples=[date.today()])
    application_hour: ApplicationHourEnum = Field(
        examples=[ApplicationHourEnum.FULLDAY, ApplicationHourEnum.AM, ApplicationHourEnum.PM])
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
            {"requested_date": date.today(), "application_hour": ApplicationHourEnum.FULLDAY},
            {"requested_date": date.today() + timedelta(days=3), "application_hour": ApplicationHourEnum.FULLDAY}
        ]
    ])

    @model_validator(mode='after')
    def set_end_date(self):
        if self.end_date is None:
            self.end_date = self.requested_date
        return self

    class Config:
        validate_assignment = True
        from_attributes = True

class ApplicationWithdrawSchema(BaseModel):
    status: str = Field(examples=["withdrawn"])
    editor_id: int = Field(examples=[101, 102, 103])
    application_id: int = Field(examples=[201, 202, 203])
    withdraw_reason: Optional[str] = Field(default=None, examples=["Personal reasons", "Change of plans"])
    class Config:
        from_attributes = True

class ApplicationWithdrawEventSchema(BaseModel):
    status: str = Field(examples=["withdrawn"])
    editor_id: int = Field(examples=[101, 102, 103])
    withdraw_reason: Optional[str] = Field(default=None, examples=["Personal reasons", "Change of plans"])
    class Config:
        from_attributes = True

class ApplicationApproveRejectSchema(BaseModel):
    status: str = Field(examples=["approved", "rejected"])
    approver_id: int = Field(examples=[100, 102, 103])
    application_id: int = Field(examples=[201, 202, 203])
    outcome_reason: Optional[str] = Field(default=None, examples=["Some reason for decision"])
    class Config:
        from_attributes = True


class ApprovedApplicationLocationSchema(BaseModel):
    employee_id:int
    employee_fname: str = Field(examples=["John", "Jane"])
    employee_lname: str = Field(examples=["Doe", "Smith"])
    location: str = Field(examples=["New York", "London"])
    position: str = Field(examples=["Manager", "Developer"])
    date: str = Field(examples=["2023-10-01", "2023-10-02"])
    application_hour:str = Field(examples=["FULLDAY","AM","PM"])
    role:int
    team_id:int

    class Config:
        from_attributes = True
