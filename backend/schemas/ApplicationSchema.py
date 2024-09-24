from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

class ApplicationSchema(BaseModel):
    application_id: int = Field(examples=[201, 202, 203])
    reason: str = Field(examples=["Vacation request", "Sick leave", "Personal day"])
    requested_date: date = Field(examples=[date.today()])
    description: Optional[str] = Field(default=None, examples=["Going on a family vacation", "Doctor's appointment"])
    created_on: datetime = Field(examples=[datetime.now()])
    last_updated_on: Optional[datetime] = Field(default=None, examples=[datetime.now()])
    status: str = Field(examples=["pending", "approved", "rejected", "withdrawn"])
    staff_id: int = Field(examples=[101, 102, 103])
    approver_id: Optional[int] = Field(default=None, examples=[101, 102, 103])
    recurring: bool = Field(examples=[True, False])

    class Config:
        from_attributes = True

class ApplicationResponse(BaseModel):
    application_id: int = Field(examples=[201, 202, 203])
    reason: str = Field(examples=["Vacation request", "Sick leave", "Personal day"])
    description: Optional[str] = Field(default=None, examples=["Going on a family vacation", "Doctor's appointment"])
    created_on: datetime = Field(examples=[datetime.now()])
    last_updated_on: Optional[datetime] = Field(default=None, examples=[datetime.now()])
    status: str = Field(examples=["pending", "approved", "rejected", "withdrawn"])
    staff_id: int = Field(examples=[101, 102, 103])
    approver_id: Optional[int] = Field(default=None, examples=[101, 102, 103])
    recurring: bool = Field(examples=[False, True])

class ApplicationCreateSchema(BaseModel):
    location: str = Field(examples=["Home", "Office", "Remote"])
    reason: str = Field(examples=["Vacation request", "Sick leave", "Personal day"])
    requested_date: date = Field(examples=[date.today()])
    description: Optional[str] = Field(default=None, examples=["Going on a family vacation", "Doctor's appointment"])
    staff_id: int = Field(examples=[101, 102, 103])
    recurring: bool = Field(examples=[False, True])

class ApplicationUpdateSchema(BaseModel):
    reason: Optional[str] = Field(default=None, examples=["Vacation request", "Sick leave", "Personal day"])
    requested_date: date = Field(examples=[date.today()])
    description: Optional[str] = Field(default=None, examples=["Going on a family vacation", "Doctor's appointment"])
    status: Optional[str] = Field(default=None, examples=["pending", "approved", "rejected", "withdrawn"])
    approver_id: Optional[int] = Field(default=None, examples=[101, 102, 103])

class ApplicationWithdrawSchema(BaseModel):
    status: str = Field(examples=["withdrawn"])
    staff_id: int = Field(examples=[101, 102, 103])
    application_id: int = Field(examples=[201, 202, 203])
    withdraw_reason: Optional[str] = Field(default=None, examples=["Personal reasons", "Change of plans"])