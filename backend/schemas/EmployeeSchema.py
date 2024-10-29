from typing import Optional, List
from pydantic import BaseModel, Field
from .BaseSchema import BaseEmployeeSchema, BaseDepartmentInfo, BaseTeamInfo


class EmployeeSchema(BaseEmployeeSchema):
    department: Optional[BaseDepartmentInfo] = None
    team: Optional[BaseTeamInfo] = None
    directed_department: Optional[BaseDepartmentInfo] = None
    managed_team: Optional[BaseTeamInfo] = None
    direct_reports: Optional[List[BaseEmployeeSchema]] = None

    class Config:
        from_attributes = True


class EmployeeCreateSchema(BaseModel):
    staff_fname: str = Field(examples=["John", "Jane", "Doe"])
    staff_lname: str = Field(examples=["Doe", "Smith", "Doe"])
    position: str = Field(examples=["Manager", "Director"])
    team_id: int = Field(examples=[1, 2, 3])
    country: str = Field(examples=["USA", "UK", "Canada"])
    email: str = Field(examples=["test@gmail.com"])
    role: int = Field(examples=[1, 2, 3])
    password: str = Field(examples=["password123"])

    class Config:
        from_attributes = True


class EmployeeUpdateSchema(BaseModel):
    staff_fname: Optional[str] = Field(examples=["John", "Jane", "Doe"])
    staff_lname: Optional[str] = Field(examples=["Doe", "Smith", "Doe"])
    position: Optional[str] = Field(examples=["Manager", "Director"])
    team_id: Optional[int] = Field(examples=[1, 2, 3])
    country: Optional[str] = Field(examples=["USA", "UK", "Canada"])
    email: Optional[str] = Field(examples=["test@gmail.com"])
    role: Optional[int] = Field(examples=[1, 2, 3])

    class Config:
        from_attributes = True
