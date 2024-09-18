from fastapi import HTTPException
from typing import Annotated, List, Type

from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session, class_mapper

from ..config.Database import get_db_connection
from ..models import Employee

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class EmployeeRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)):
        self.db = db

    def get_all_employees(self) -> list[Type[Employee]]:
         employees = self.db.query(Employee).all()
         if employees is not None:
             return employees
         else:
                return []
    def get_employee(self, staff_id: int) -> Employee:
        employee = self.db.query(Employee).filter(Employee.staff_id  == staff_id ).first()
        if employee is not None:
            return employee
        else:
            raise HTTPException(status_code=404, detail="Employee not found")

    def create_employee(self, employee: Employee) -> Employee:
        temp_employee = self.db.query(Employee).filter(Employee.staff_id == employee.staff_id).first()
        if temp_employee is not None:
            raise HTTPException(status_code=400, detail="Employee already exists")
        new_employee = Employee(
            staff_id=employee.staff_id,
            email=employee.email,
            staff_fname=employee.staff_fname,
            staff_lname=employee.staff_lname,
            dept=employee.dept,
            position=employee.position,
            country=employee.country,
            reporting_manager=employee.reporting_manager,
            role=employee.role,
            hashed_password=pwd_context.hash(employee.hashed_password)
        )
        self.db.add(new_employee)
        self.db.commit()
        self.db.refresh(new_employee)
        return new_employee

    from sqlalchemy.orm import class_mapper

    def update_employee(self, staff_id: int, employee: Employee) -> Employee:
        db_employee = self.db.query(Employee).filter(Employee.staff_id == staff_id).first()
        if db_employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        columns = [column.key for column in class_mapper(Employee).columns]
        for column in columns:
            if hasattr(employee, column):
                setattr(db_employee, column, getattr(employee, column))
        self.db.commit()
        self.db.refresh(db_employee)  # Refresh the db_employee object
        return db_employee

    def delete_employee(self, staff_id: int) -> Employee:
        employee = self.db.query(Employee).filter(Employee.staff_id == staff_id).first()
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        self.db.delete(employee)
        self.db.commit()
        return employee