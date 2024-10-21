from pydantic import BaseModel, Field
from typing import Optional
from backend.models.enums.EmployeeRoleEnum import EmployeeRole

class BaseEmployeeInfo(BaseModel):
    staff_id: int = Field(examples=[1, 2, 3])
    staff_fname: str = Field(examples=["John", "Jane", "Doe"])
    staff_lname: str = Field(examples=["Doe", "Smith", "Doe"])
    position: str = Field(examples=["Manager", "Director"])
    team_id: int = Field(examples=[1, 2, 3])
    country: str = Field(examples=["USA", "UK", "Canada"])
    email: str = Field(examples=["test@gmail.com"])
    class Config:
        from_attributes = True

class BaseDepartmentInfo(BaseModel):
    department_id: int = Field(examples=[1, 2, 3])
    name: str = Field(examples=["Engineering", "Marketing", "Finance"])
    class Config:
        from_attributes = True

class BaseTeamInfo(BaseModel):
    team_id: int = Field(examples=[1, 2, 3])
    name: str = Field(examples=["Frontend Team", "Backend Team", "DevOps Team"])
    description: Optional[str] = Field(examples=["Responsible for user interfaces", "Handles server-side logic", "Manages deployments and infrastructure"])
    class Config:
        from_attributes = True

class BaseEmployeeSchema(BaseEmployeeInfo):
    position: str = Field(examples=["Manager", "Director"])
    department_id: int = Field(examples=[1, 2, 3])
    team_id: int = Field(examples=[1, 2, 3])
    country: str = Field(examples=["USA", "UK", "Canada"])
    email: str = Field(examples=["test@gmail.com"])
    reporting_manager: Optional[int] = Field(default=None, examples=[1, 2, 3])
    role: int = Field(examples=[1, 2, 3])
    class Config:
        from_attributes = True
