from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..schemas.ApplicationSchema import ApplicationSchema, ApplicationCreateSchema, ApplicationUpdateSchema
from ..services.ApplicationService import ApplicationService
from ..services.dependencies import role_required
from ..config.Database import get_db_connection

ApplicationRouter = APIRouter(
    prefix="/api/application",
    tags=["Application Endpoints"],
)

@ApplicationRouter.get("/", response_model=List[ApplicationSchema])
def get_all_applications(service: ApplicationService = Depends(),
    roles: Annotated[List[str], Depends(role_required(1, 2, 3))] = None
):
    return service.get_all_applications()

@ApplicationRouter.get("/{application_id}", response_model=ApplicationSchema)
def get_application_by_id(
    application_id: int,
    service: ApplicationService = Depends(),
    roles: Annotated[List[str], Depends(role_required(1, 2, 3))] = None
):
    return service.get_application_by_id(application_id)

@ApplicationRouter.get("/staff/{staff_id}", response_model=List[ApplicationSchema])
def get_applications_by_staff_id(
    staff_id: int,
    service: ApplicationService = Depends(),
    roles: Annotated[List[str], Depends(role_required(1, 2, 3))] = None
):
    return service.get_applications_by_staff_id(staff_id)

@ApplicationRouter.post("/", response_model=ApplicationSchema)
def create_application(
    application: ApplicationCreateSchema,
    service: ApplicationService = Depends(),
    roles: Annotated[List[str], Depends(role_required(1, 2, 3))] = None
):
    return service.create_application(application)

@ApplicationRouter.put("/{application_id}", response_model=ApplicationSchema)
def update_application(
    application_id: int,
    application: ApplicationUpdateSchema,
    service: ApplicationService = Depends(),
    roles: Annotated[List[str], Depends(role_required(1, 2, 3))] = None
):
    return service.update_application(application_id, application)

@ApplicationRouter.get("/status/{status}", response_model=List[ApplicationSchema])
def get_applications_by_status(
    status: str,
    service: ApplicationService = Depends(),
    roles: Annotated[List[str], Depends(role_required(1, 2, 3))] = None
):
    return service.get_applications_by_status(status)

@ApplicationRouter.put("/{application_id}/status", response_model=ApplicationSchema)
def update_application_status(
    application_id: int,
    new_status: str,
    service: ApplicationService = Depends(),
    roles: Annotated[List[str], Depends(role_required(1, 2, 3))] = None
):
    return service.update_application_status(application_id, new_status)