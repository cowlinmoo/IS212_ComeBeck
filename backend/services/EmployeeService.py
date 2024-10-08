from typing import List

from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy import inspect

from backend.models import Employee
from backend.repositories.DepartmentRepository import DepartmentRepository
from backend.repositories.EmployeeRepository import EmployeeRepository
from backend.repositories.TeamRepository import TeamRepository
from backend.schemas.BaseSchema import BaseEmployeeSchema
from backend.schemas.EmployeeSchema import EmployeeSchema, EmployeeCreateSchema, EmployeeUpdateSchema


class EmployeeService:
    employeeRepository: EmployeeRepository
    teamRepository: TeamRepository
    departmentRepository: DepartmentRepository

    def __init__(
        self, employeeRepository: EmployeeRepository = Depends(), teamRepository: TeamRepository = Depends(),
            departmentRepository: DepartmentRepository = Depends()
    ) -> None:
        self.employeeRepository = employeeRepository
        self.teamRepository = teamRepository
        self.departmentRepository = departmentRepository

    def get_all_employees(self) -> List[EmployeeSchema]:
        employees = self.employeeRepository.get_all_employees()
        return [self.employee_to_schema(employee) for employee in employees]

    def get_employee_by_staff_id(self, staff_id: int) -> EmployeeSchema:
        employee = self.employeeRepository.get_employee(staff_id)
        return self.employee_to_schema(employee)

    def create_employee(self, employee: EmployeeCreateSchema) -> EmployeeSchema:
        # Validate team_id
        team = self.teamRepository.get_team_by_id(employee.team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Team ID does not exist")

        # Get department_id from team
        department_id = team.department_id

        # Validate manager
        if not team.manager_id:
            raise HTTPException(status_code=400, detail="Team has no manager assigned")

        # Create employee data dictionary
        employee_data_dict = employee.model_dump(exclude_unset=True)
        employee_data_dict['department_id'] = department_id
        employee_data_dict['reporting_manager'] = team.manager_id

        employee_data = Employee(**employee_data_dict)
        new_employee = self.employeeRepository.create_employee(employee_data)

        return self.employee_to_schema(new_employee)

    def employee_to_schema(self, employee: Employee) -> EmployeeSchema:
        department = self.departmentRepository.get_department_by_id(employee.department_id)
        team = self.teamRepository.get_team_by_id(employee.team_id)
        managed_team = None
        try:
            managed_team = self.teamRepository.get_team_by_manager_id(employee.staff_id)
        except HTTPException:
            pass

        direct_reports = self.employeeRepository.get_employees_by_manager_id(employee.staff_id)
        directed_department = None
        try:
            directed_department = self.departmentRepository.get_department_by_director_id(employee.staff_id)
        except HTTPException:
            pass

        def orm_to_dict(obj):
            return {c.key: getattr(obj, c.key)
                    for c in inspect(obj).mapper.column_attrs}

        employee_dict = {
            "staff_id": employee.staff_id,
            "staff_fname": employee.staff_fname,
            "staff_lname": employee.staff_lname,
            "position": employee.position,
            "department_id": employee.department_id,
            "team_id": employee.team_id,
            "country": employee.country,
            "email": employee.email,
            "reporting_manager": employee.reporting_manager,
            "role": employee.role,
            "department": orm_to_dict(department) if department else None,
            "team": orm_to_dict(team) if team else None,
            "managed_team": orm_to_dict(managed_team) if managed_team else None,
            "direct_reports": [BaseEmployeeSchema.model_validate(orm_to_dict(report)) for report in
                               direct_reports] if direct_reports else None,
            "directed_department": orm_to_dict(directed_department) if directed_department else None
        }

        return EmployeeSchema.model_validate(employee_dict)

    def update_employee(self, staff_id: int, employee: EmployeeUpdateSchema) -> EmployeeSchema:
        update_data = employee.model_dump(exclude_unset=True)

        if 'team_id' in update_data:
            # Validate team_id
            team = self.teamRepository.get_team_by_id(update_data['team_id'])
            if not team:
                raise HTTPException(status_code=404, detail="Team ID does not exist")

            # Get department_id from team
            update_data['department_id'] = team.department_id

            # Update reporting manager
            if team.manager_id:
                update_data['reporting_manager'] = team.manager_id
            else:
                raise HTTPException(status_code=400, detail="Team has no manager assigned")

        updated_employee = self.employeeRepository.update_employee(staff_id, update_data)
        return self.employee_to_schema(updated_employee)

    def delete_employee_by_staff_id(self, staff_id: int):
        return self.employeeRepository.delete_employee(staff_id)
