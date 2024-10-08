from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from .BaseSchema import BaseTeamInfo, BaseDepartmentInfo, BaseEmployeeInfo

class TeamSchema(BaseTeamInfo):
    created_on: datetime
    manager_id: Optional[int] = Field(examples=[1, 2, 3])
    department_id: int = Field(examples=[1, 2, 3])
    parent_team_id: Optional[int] = Field(examples=[1, 2, 3])

    department: Optional[BaseDepartmentInfo] = None
    manager: Optional[BaseEmployeeInfo] = None
    members: Optional[List[BaseEmployeeInfo]] = None
    parent_team: Optional[BaseTeamInfo] = None

    class Config:
        from_attributes = True

class TeamCreateSchema(BaseModel):
    name: str = Field(examples=["Frontend Team", "Backend Team", "DevOps Team"])
    description: Optional[str] = Field(examples=["Responsible for user interfaces", "Handles server-side logic", "Manages deployments and infrastructure"])
    manager_id: Optional[int] = Field(examples=[1, 2, 3])
    department_id: int = Field(examples=[1, 2, 3])
    parent_team_id: Optional[int] = Field(examples=[1, 2, 3])
    class Config:
        from_attributes = True

class TeamUpdateSchema(BaseModel):
    name: Optional[str] = Field(examples=["Frontend Team", "Backend Team", "DevOps Team"])
    description: Optional[str] = Field(examples=["Responsible for user interfaces", "Handles server-side logic", "Manages deployments and infrastructure"])
    manager_id: Optional[int] = Field(examples=[1, 2, 3])
    department_id: Optional[int] = Field(examples=[1, 2, 3])
    parent_team_id: Optional[int] = Field(examples=[1, 2, 3])
    class Config:
        from_attributes = True