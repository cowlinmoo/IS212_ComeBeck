import os
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone
from typing import Optional, Tuple, Any

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend.models.EmployeeModel import Employee
from ..config.Database import get_db_connection
from ..models.enums.EmployeeRoleEnum import EmployeeRole

SECRET_KEY = 'c1894f82128da39efc2d93fddb4b7d53c6fddd33270dd8f58bd48b56be0a7544'
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthenticationService:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)):
        self.db = db

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def authenticate_employee(self, email: str, password: str) -> tuple[Any, EmployeeRole] | None:
        try:
            employee = self.db.query(Employee).filter(Employee.email == email).first()
            if employee and bcrypt_context.verify(password, employee.password):
                employee_role = EmployeeRole(employee.role)
                print(f"Employee authenticated: {employee.email}, Role: {employee_role.name}")
                return employee, employee_role
        except Exception as e:
            print(f"Authentication error: {str(e)}")
        return None, None