from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship, backref

from backend.models.BaseModel import EntityMeta


class Employee(EntityMeta):
    __tablename__ = 'employees'

    staff_id = Column(Integer, primary_key=True)
    staff_fname = Column(String(50), nullable=False)
    staff_lname = Column(String(50), nullable=False)
    position = Column(String(50), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.department_id'), nullable=False)
    team_id = Column(Integer, ForeignKey('teams.team_id'), nullable=False)
    country = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    reporting_manager = Column(Integer, ForeignKey('employees.staff_id'), nullable=True)
    role = Column(Integer, nullable=False)
    password = Column(String(128), nullable=False)

    department = relationship("Department", foreign_keys=[department_id], back_populates="employees")
    team = relationship("Team", foreign_keys=[team_id], back_populates="members")
    managed_team = relationship("Team", back_populates="manager", foreign_keys="Team.manager_id")
    applications = relationship("Application", foreign_keys="Application.staff_id", back_populates="staff")
    approved_applications = relationship("Application", foreign_keys="Application.approver_id",
                                         back_populates="approver")

    direct_reports = relationship("Employee",
                                  backref="manager",
                                  remote_side=[staff_id])

    directed_department = relationship("Department", back_populates="director", foreign_keys="Department.director_id")