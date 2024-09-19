from pydantic import BaseModel, Field


class EmployeeSchema(BaseModel):
    staff_id: int = Field(examples=[1, 2, 3])
    staff_fname: str = Field(examples=["John", "Jane", "Doe"])
    staff_lname: str = Field(examples=["Doe", "Smith", "Doe"])
    dept: str = Field(examples=["HR", "IT", "Finance"])
    position: str = Field(examples=["Manager", "Director"])
    country: str = Field(examples=["USA", "UK", "Canada"])
    email: str = Field(examples=["test@gmail.com"])
    reporting_manager: int = Field(examples=[1, 2, 3])
    role: int = Field(examples=[1, 2, 3])
    password: str = Field(examples=["password123"])