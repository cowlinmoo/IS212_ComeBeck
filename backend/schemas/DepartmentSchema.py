from typing import Optional, List
from pydantic import Field
from .BaseSchema import BaseDepartmentInfo, BaseEmployeeInfo
from .TeamSchema import TeamSchema


class DepartmentSchema(BaseDepartmentInfo):
    description: Optional[str] = (
        Field(examples=["The department that handles all engineering matters",
                        "The department that handles all marketing matters",
                        "The department that handles all finance matters"]))
    director_id: Optional[int] = Field(examples=[1, 2, 3])

    director: Optional[BaseEmployeeInfo] = None
    teams: Optional[List[TeamSchema]] = None

    class Config:
        from_attributes = True
