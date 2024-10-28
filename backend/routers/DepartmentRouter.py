from typing import List

from fastapi import APIRouter, Depends

from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.schemas.DepartmentSchema import DepartmentSchema
from backend.services.DepartmentService import DepartmentService
from backend.services.dependencies import role_required

DepartmentRouter = APIRouter(
    prefix="/api/department",
    tags=["Department Endpoints"],
)


@DepartmentRouter.get("/{department_id}", response_model=DepartmentSchema)
def get_department_by_department_id(department_id: int,
                                    service: DepartmentService = Depends(),
                                    current_user: dict =
                                    Depends(role_required(EmployeeRole.HR,
                                                          EmployeeRole.MANAGER,
                                                          EmployeeRole.STAFF))):
    return service.get_department_by_department_id(department_id)


@DepartmentRouter.get("", response_model=List[DepartmentSchema])
def get_all_departments(service: DepartmentService = Depends(),
                        current_user: dict =
                        Depends(role_required(EmployeeRole.HR,
                                              EmployeeRole.MANAGER,
                                              EmployeeRole.STAFF))):
    return service.get_all_departments()
