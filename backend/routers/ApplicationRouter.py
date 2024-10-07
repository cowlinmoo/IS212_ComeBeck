from typing import List
from fastapi import APIRouter, Depends

from ..models.enums.EmployeeRoleEnum import EmployeeRole
from ..schemas.ApplicationSchema import (ApplicationSchema, ApplicationCreateSchema, ApplicationUpdateSchema,
                                         ApplicationWithdrawSchema, ApplicationResponse)
from ..services.ApplicationService import ApplicationService
from ..services.dependencies import role_required


ApplicationRouter = APIRouter(
    prefix="/api/application",
    tags=["Application Endpoints"],
)


@ApplicationRouter.get("/", response_model=List[ApplicationResponse])
def get_all_applications(
        service: ApplicationService = Depends(),
        current_user: dict = Depends(role_required(
            EmployeeRole.HR, EmployeeRole.MANAGER, EmployeeRole.STAFF))
):
    return service.get_all_applications()


@ApplicationRouter.get("/{application_id}", response_model=ApplicationResponse)
def get_application_by_id(
    application_id: int,
    service: ApplicationService = Depends(),
    current_user: dict = Depends(role_required(
        EmployeeRole.HR, EmployeeRole.MANAGER, EmployeeRole.STAFF))
):
    return service.get_application_by_id(application_id)


@ApplicationRouter.get("/staff/{staff_id}", response_model=List[ApplicationResponse])
def get_applications_by_staff_id(
    staff_id: int,
    service: ApplicationService = Depends(),
    current_user: dict = Depends(role_required(
        EmployeeRole.HR, EmployeeRole.MANAGER, EmployeeRole.STAFF))
):
    return service.get_applications_by_staff_id(staff_id)


@ApplicationRouter.post("/", response_model=ApplicationCreateSchema)
def create_application(
    application: ApplicationCreateSchema,
    service: ApplicationService = Depends(),
    current_user: dict = Depends(role_required(
        EmployeeRole.HR, EmployeeRole.MANAGER, EmployeeRole.STAFF))
):
    return service.create_application(application)


@ApplicationRouter.put("/{application_id}", response_model=ApplicationResponse)
def update_application(
    application_id: int,
    application: ApplicationUpdateSchema,
    service: ApplicationService = Depends(),
    current_user: dict = Depends(role_required(
        EmployeeRole.HR, EmployeeRole.MANAGER, EmployeeRole.STAFF))
):
    return service.update_application(application_id, application)


@ApplicationRouter.put("/withdraw/{application_id}", response_model=ApplicationResponse)
def withdraw_application(
    application_id: int,
    application: ApplicationWithdrawSchema,
    service: ApplicationService = Depends(),
    current_user: dict = Depends(role_required(
        EmployeeRole.HR, EmployeeRole.MANAGER, EmployeeRole.STAFF))
):
    return service.withdraw_application(application_id, application)


@ApplicationRouter.get("/status/{status}", response_model=List[ApplicationResponse])
def get_applications_by_status(
    status: str,
    service: ApplicationService = Depends(),
    current_user: dict = Depends(role_required(
        EmployeeRole.HR, EmployeeRole.MANAGER, EmployeeRole.STAFF))
):
    return service.get_applications_by_status(status)


@ApplicationRouter.put("/{application_id}/status", response_model=ApplicationResponse)
def update_application_status(
    application_id: int,
    new_status: str,
    service: ApplicationService = Depends(),
    current_user: dict = Depends(role_required(
        EmployeeRole.HR, EmployeeRole.MANAGER, EmployeeRole.STAFF))
):
    return service.update_application_status(application_id, new_status)


@ApplicationRouter.get("/locations")
def get_all_approved_locatons(service: ApplicationService = Depends()):
    return service.get_employee_approved_application_locations()
