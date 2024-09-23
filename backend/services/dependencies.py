from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.services.AuthenticationService import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/authenticate/")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: int = payload.get("role")
        if email is None or role is None:
            raise credentials_exception
        return {"email": email, "role": EmployeeRole(role)}
    except JWTError:
        raise credentials_exception

def role_required(*allowed_roles: EmployeeRole):
    def wrapper(current_user: dict = Depends(get_current_user)):
        if current_user["role"] not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sorry you don't have enough permissions to perform this action"
            )
        return current_user
    return wrapper