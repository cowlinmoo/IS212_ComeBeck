from fastapi import HTTPException
from typing import List, Type
from sqlalchemy.orm import Session
from fastapi import Depends
from ..config.Database import get_db_connection
from ..models import Employee
from passlib.context import CryptContext
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class EmployeeRepository:
    def __init__(self, db: Session = Depends(get_db_connection)):
        self.db = db

    def get_employee(self, staff_id: int) -> Employee:
        employee = self.db.query(Employee).filter(
            Employee.staff_id == staff_id).first()
        if not employee:
            logging.error(f"Employee with staff ID {staff_id} not found")
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee

    def get_all_employees(self) -> List[Type[Employee]]:
        return self.db.query(Employee).all()

    def create_employee(self, employee_data: Employee) -> Employee:
        if self.db.query(Employee).filter(Employee.email == employee_data.email).first():
            raise HTTPException(
                status_code=400, detail="Employee with this email already exists")
        employee_data.password = pwd_context.hash(employee_data.password)
        new_employee = employee_data
        self.db.add(new_employee)
        self.db.commit()
        self.db.refresh(new_employee)
        return new_employee

    def update_employee(self, staff_id: int, update_data: dict) -> Employee:
        employee = self.db.query(Employee).filter(
            Employee.staff_id == staff_id).first()
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        for key, value in update_data.items():
            setattr(employee, key, value)

        self.db.commit()
        self.db.refresh(employee)
        return employee

    def delete_employee(self, staff_id: int) -> Employee:
        employee = self.get_employee(staff_id)
        self.db.delete(employee)
        self.db.commit()
        return employee

    def get_employee_email_by_staff_id(self, staff_id: int) -> str:
        employee = self.get_employee(staff_id)
        return employee.email

    def get_employees_by_ids(self, staff_ids: List[str]) -> List[Employee]:
        employees = self.db.query(Employee).filter(
            Employee.staff_id.in_(staff_ids)).all()
        return employees
