from pydantic import BaseModel, Field

from backend.models.enums.EmployeeRoleEnum import EmployeeRole


class EmployeeSchema(BaseModel):
    staff_id: int = Field(examples=[1, 2, 3])
    staff_fname: str = Field(examples=["John", "Jane", "Doe"])
    staff_lname: str = Field(examples=["Doe", "Smith", "Doe"])
    dept: str = Field(examples=["HR", "IT", "Finance"])
    position: str = Field(examples=["Manager", "Director"])
    country: str = Field(examples=["USA", "UK", "Canada"])
    email: str = Field(examples=["test@gmail.com"])
    reporting_manager: int = Field(examples=[1, 2, 3])
    role: EmployeeRole = Field(examples=[EmployeeRole.HR, EmployeeRole.STAFF, EmployeeRole.MANAGER])
    password: str = Field(examples=["password123"])

    class Config:
        from_attributes = True

class EmployeeInfo(BaseModel):
    staff_id: int = Field(examples=[1, 2, 3])
    staff_fname: str = Field(examples=["John", "Jane", "Doe"])
    staff_lname: str = Field(examples=["Doe", "Smith", "Doe"])
