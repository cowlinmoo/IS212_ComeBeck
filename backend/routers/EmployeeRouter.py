from typing import List, Annotated
from fastapi import APIRouter, Depends

from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.schemas.EmployeeSchema import EmployeeSchema, EmployeeCreateSchema, EmployeeUpdateSchema
from backend.services.EmployeeService import EmployeeService
from backend.services.dependencies import role_required

EmployeeRouter = APIRouter(
    prefix="/api/employee",
    tags=["Employee Endpoints"],
)

@EmployeeRouter.get("", response_model=List[EmployeeSchema])
def get_all_employees(employee_service: EmployeeService = Depends(),
                    current_user: dict = Depends(role_required(EmployeeRole.HR, EmployeeRole.MANAGER, EmployeeRole.STAFF))):
    return employee_service.get_all_employees()

@EmployeeRouter.get("/{staff_id}", response_model=EmployeeSchema)
def get_employee(staff_id: int, employee_service: EmployeeService = Depends(),
                    current_user: dict = Depends(role_required(EmployeeRole.HR, EmployeeRole.MANAGER, EmployeeRole.STAFF))):
    return employee_service.get_employee_by_staff_id(staff_id)

@EmployeeRouter.post("", response_model=EmployeeSchema)
def create_employee(employee: EmployeeCreateSchema, employee_service: EmployeeService = Depends()):
    return employee_service.create_employee(employee)

@EmployeeRouter.put("/{staff_id}", response_model=EmployeeSchema)
def update_employee(
    staff_id: int,
    employee: EmployeeUpdateSchema,  # Change this to EmployeeUpdateSchema
    employee_service: EmployeeService = Depends(),
    current_user: dict = Depends(role_required(EmployeeRole.HR, EmployeeRole.MANAGER))
):
    return employee_service.update_employee(staff_id, employee)

@EmployeeRouter.delete("/{staff_id}", response_model=EmployeeSchema)
def delete_employee(staff_id: int, employee_service: EmployeeService = Depends(),
                    current_user: dict = Depends(role_required(EmployeeRole.HR, EmployeeRole.MANAGER))):
    return employee_service.delete_employee_by_staff_id(staff_id)