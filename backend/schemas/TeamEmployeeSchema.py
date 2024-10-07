from pydantic import BaseModel


class TeamEmployeeSchema(BaseModel):
    team_id: int
    employee_id: int

    class Config:
        from_attributes = True

class TeamEmployeeResponseSchema(BaseModel):
    team_id: int
