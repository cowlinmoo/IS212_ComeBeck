from fastapi import Depends

from backend.models import Employee
from backend.repositories.EmployeeRepository import EmployeeRepository
from backend.schemas.EmployeeSchema import EmployeeSchema


class EmployeeService:
    employeeRepository: EmployeeRepository

    def __init__(
        self, employeeRepository: EmployeeRepository = Depends()
    ) -> None:
        self.employeeRepository = employeeRepository

    def get_all_employees(self):
        return self.employeeRepository.get_all_employees()

    def get_employee_by_staff_id(self, staff_id: int):
        return self.employeeRepository.get_employee(staff_id)

    def create_employee(self, employee: EmployeeSchema):
        employee_dict = employee.model_dump(exclude_unset=True)
        employee_data = Employee(**employee_dict)
        return self.employeeRepository.create_employee(employee_data)

    def update_employee(self, staff_id: int, employee: EmployeeSchema):
        update_data = employee.model_dump(exclude_unset=True)
        return self.employeeRepository.update_employee(staff_id, update_data)

    def delete_employee_by_staff_id(self, staff_id: int):
        return self.employeeRepository.delete_employee(staff_id)
