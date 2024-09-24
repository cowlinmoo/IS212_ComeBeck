from fastapi import Depends, HTTPException
from typing import List, Type

from backend.models.generators import get_current_datetime_sgt
from backend.repositories.ApplicationRepository import ApplicationRepository
from backend.models import Application
from backend.repositories.EmployeeRepository import EmployeeRepository
from backend.schemas.ApplicationSchema import ApplicationCreateSchema, ApplicationUpdateSchema

class ApplicationService:
    def __init__(self, application_repository: ApplicationRepository = Depends(), employee_repository: EmployeeRepository = Depends()):
        self.employee_repository = employee_repository
        self.application_repository = application_repository

    def get_all_applications(self) -> List[Type[Application]]:
        return self.application_repository.get_all_applications()

    def get_application_by_id(self, application_id: int) -> Application:
        # check if application exists in the database
        if self.application_repository.get_application_by_application_id(application_id) is None:
            raise HTTPException(status_code=404, detail="Application not found")
        return self.application_repository.get_application_by_application_id(application_id)

    def get_applications_by_staff_id(self, staff_id: int) -> List[Type[Application]]:
        # check if employee exists in the database
        if self.employee_repository.get_employee(staff_id) is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return self.application_repository.get_application_by_staff_id(staff_id)

    def create_application(self, application: ApplicationCreateSchema) -> Application:
        # check if employee exists in the database
        if self.employee_repository.get_employee(application.staff_id) is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        application_dict = application.model_dump()
        application_dict["status"] = "pending" # set status to pending as it is a new application
        application_dict["created_on"] = get_current_datetime_sgt()
        application_dict["last_updated_on"] = get_current_datetime_sgt()
        return self.application_repository.create_application(application_dict)

    def update_application(self, application_id: int, application: ApplicationUpdateSchema) -> Application:
        return self.application_repository.update_application(application_id, application)

    def get_applications_by_status(self, status: str) -> List[Type[Application]]:
        return self.application_repository.get_applications_by_status(status)

    def update_application_status(self, application_id: int, new_status: str) -> Application:
        return self.application_repository.update_application_status(application_id, new_status)