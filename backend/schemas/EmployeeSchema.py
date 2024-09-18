from pydantic import BaseModel


class EmployeeSchema(BaseModel):
    staff_id: int
    staff_fname: str
    staff_lname: str
    dept: str
    position: str
    country: str
    email: str
    reporting_manager: int
    role: int
    hashed_password: str