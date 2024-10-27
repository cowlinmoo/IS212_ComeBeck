from typing import List, Type

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from backend.config.Database import get_db_connection
from backend.models import Department


class DepartmentRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)):
        self.db = db

    def get_all_department_ids(self) -> List[int]:
        return [department.department_id for department in self.db.query(Department).all()]

    def get_department_by_id(self, department_id: int) -> Department:
        department = self.db.query(Department).filter(Department.department_id == department_id).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        return department

    def get_department_by_director_id(self, director_id: int) -> Department:
        department = self.db.query(Department).filter(Department.director_id == director_id).first()
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        return department

    def get_employees_by_department_id(self, department_id: int) -> List[Type[Department]]:
        department = self.get_department_by_id(department_id)
        return department.employees

    def get_all_departments(self):
        return self.db.query(Department).all()