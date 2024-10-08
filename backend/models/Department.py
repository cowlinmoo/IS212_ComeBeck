from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship

from backend.models.BaseModel import EntityMeta

class Department(EntityMeta):
    __tablename__ = 'departments'

    department_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    director_id = Column(Integer, ForeignKey('employees.staff_id'), nullable=True)

    director = relationship("Employee", foreign_keys=[director_id], back_populates="directed_department")
    teams = relationship("Team", back_populates="department")
    employees = relationship("Employee", back_populates="department", foreign_keys="Employee.department_id")
