from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from backend.models.BaseModel import EntityMeta
from backend.models.enums.EmployeeRoleEnum import EmployeeRole

class Employee(EntityMeta):
    __tablename__ = 'employees'

    staff_id = Column(Integer, primary_key=True)
    staff_fname = Column(String(50), nullable=False)
    staff_lname = Column(String(50), nullable=False)
    dept = Column(String(50), nullable=False)
    position = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    reporting_manager = Column(Integer, ForeignKey('employees.staff_id'), nullable=False)
    role = Column(Integer, nullable=False)
    password = Column(String(128), nullable=False)

    class Config:
        orm_mode = True
