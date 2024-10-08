from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from .BaseSchema import BaseTeamInfo, BaseDepartmentInfo, BaseEmployeeInfo

class TeamSchema(BaseTeamInfo):
    department: Optional[BaseDepartmentInfo] = None
    manager: Optional[BaseEmployeeInfo] = None
    parent_team: Optional[BaseTeamInfo] = None
    child_teams: Optional[List[BaseTeamInfo]] = None
    members: Optional[List[BaseEmployeeInfo]] = None
    class Config:
        from_attributes = True