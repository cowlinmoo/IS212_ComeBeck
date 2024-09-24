from fastapi import APIRouter, Depends, HTTPException, status, Body, Form
from fastapi.security import OAuth2PasswordRequestForm

from backend.services.AuthenticationService import AuthenticationService
from backend.schemas.TokenSchema import Token

AuthRouter = APIRouter(
    prefix="/api/authenticate",
    tags=["Authentication Endpoints"],
)

@AuthRouter.post("/", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: AuthenticationService = Depends()
):
    employee, employee_role = auth_service.authenticate_employee(form_data.username, form_data.password)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(
        data={"sub": employee.email, "role": employee.role}
    )

    return Token(email=employee.email, role=employee_role.name, access_token=access_token, token_type="bearer")