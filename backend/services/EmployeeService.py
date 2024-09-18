from fastapi import Depends

from backend.repositories.EmployeeRepository import EmployeeRepository

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

    def create_employee(self, employee):
        return self.employeeRepository.create_employee(employee)

    def update_employee(self,staff_id, employee):
        return self.employeeRepository.update_employee(staff_id, employee)

    def delete_employee_by_staff_id(self, staff_id: int):
        return self.employeeRepository.delete_employee(staff_id)
