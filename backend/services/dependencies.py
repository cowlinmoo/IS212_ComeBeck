from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from backend.config.Database import get_db_connection
from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.repositories.ApplicationRepository import ApplicationRepository
from backend.repositories.EmployeeRepository import EmployeeRepository
from backend.repositories.EventRepository import EventRepository
from backend.services.ApplicationService import ApplicationService
from backend.services.AuthenticationService import SECRET_KEY, ALGORITHM
from backend.services.EmailService import EmailService
from backend.services.EventService import EventService
from backend.services.SchedulerService import SchedulerService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/authenticate")

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


def get_application_repository(db: Session = Depends(get_db_connection)):
    return ApplicationRepository(db)


def get_employee_repository(db: Session = Depends(get_db_connection)):
    return EmployeeRepository(db)


def get_email_service():
    return EmailService()


def get_event_repository(db: Session = Depends(get_db_connection)):
    return EventRepository(db)


def get_event_service(event_repository: EventRepository = Depends(get_event_repository)):
    return EventService(event_repository)


def get_application_service(
        application_repository: ApplicationRepository = Depends(get_application_repository),
        employee_repository: EmployeeRepository = Depends(get_employee_repository),
        email_service: EmailService = Depends(get_email_service),
        event_repository: EventRepository = Depends(get_event_repository),
        event_service: EventService = Depends(get_event_service)
):
    return ApplicationService(
        application_repository,
        employee_repository,
        email_service,
        event_repository,
        event_service
    )


def get_scheduler_service():
    db = next(get_db_connection())
    application_repository = ApplicationRepository(db)
    employee_repository = EmployeeRepository(db)
    email_service = EmailService()
    event_repository = EventRepository(db)
    event_service = EventService(event_repository)

    application_service = ApplicationService(
        application_repository,
        employee_repository,
        email_service,
        event_repository,
        event_service
    )

    return SchedulerService(application_service)
