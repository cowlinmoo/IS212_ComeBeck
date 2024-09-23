from fastapi import Depends, HTTPException
from typing import List, Type

from backend.config.EmailTemplates import (get_new_application_manager_email_subject,
                                           get_new_application_manager_email_template,
                                           get_new_application_employee_email_subject,
                                           get_new_application_employee_email_template,
                                           get_application_withdrawn_employee_email_subject,
                                           get_application_withdrawn_employee_email_template,
                                           get_application_withdrawn_manager_email_subject,
                                           get_application_withdrawn_manager_email_template)
from backend.models.generators import get_current_datetime_sgt
from backend.repositories.ApplicationRepository import ApplicationRepository
from backend.models import Application
from backend.repositories.EmployeeRepository import EmployeeRepository
from backend.schemas.ApplicationSchema import (ApplicationCreateSchema, ApplicationUpdateSchema,
                                               ApplicationWithdrawSchema)
from backend.services.EmailService import EmailService

class ApplicationService:
    def __init__(self,
                 application_repository: ApplicationRepository = Depends(),
                 employee_repository: EmployeeRepository = Depends(),
                 email_service: EmailService = Depends()
                 ):

        self.employee_repository = employee_repository
        self.application_repository = application_repository
        self.email_service = email_service

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
        employee = self.employee_repository.get_employee(application.staff_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        application_dict = application.model_dump()
        application_dict["status"] = "pending" # set status to pending as it is a new application
        application_dict["created_on"] = get_current_datetime_sgt()
        application_dict["last_updated_on"] = get_current_datetime_sgt()
        new_application = self.application_repository.create_application(application_dict)
        manager = self.employee_repository.get_manager(application.staff_id)
        manager_email = manager.email
        staff_name = employee.staff_fname + " " + employee.staff_lname
        employee_email = employee.email
        # Send email to manager
        manager_subject = get_new_application_manager_email_subject(application.staff_id, staff_name)
        manager_body = get_new_application_manager_email_template(
            manager_name=manager.staff_fname + " " + manager.staff_lname,
            employee_name=staff_name,
            employee_id=application.staff_id,
            reason=application.reason,
            description=application.description,
            status=new_application.status,
            created_on=get_current_datetime_sgt(),
            application_id = new_application.application_id
        )
        self.email_service.send_email(manager_email, manager_subject, manager_body)

        # Send email to employee
        employee_subject = get_new_application_employee_email_subject(new_application.application_id)
        employee_body = get_new_application_employee_email_template(
            employee_name=staff_name,
            reason=application.reason,
            description=application.description,
            status=new_application.status,
            created_on=get_current_datetime_sgt(),
            application_id = new_application.application_id
        )
        self.email_service.send_email(employee_email, employee_subject, employee_body)

        return new_application

    def update_application(self, application_id: int, application: ApplicationUpdateSchema) -> Application:
        return self.application_repository.update_application(application_id, application)

    def withdraw_application(self, application_id: int, application: ApplicationWithdrawSchema) -> Application:
        existing_application = self.application_repository.get_application_by_application_id(application_id)

        if existing_application is None:
            raise HTTPException(status_code=404, detail="Application not found")

        if existing_application.staff_id != application.staff_id:
            employee = self.employee_repository.get_employee(application.staff_id)
            if employee is None:
                raise HTTPException(status_code=404, detail="Employee not found")
            raise HTTPException(status_code=403, detail="You can only withdraw your own application")

        if existing_application.status == "withdrawn":
            raise HTTPException(status_code=403, detail="Application already withdrawn")

        withdrawn_application = self.application_repository.withdraw_application(application_id, application)

        # Fetch employee data
        employee = self.employee_repository.get_employee(withdrawn_application.staff_id)
        staff_name = f"{employee.staff_fname} {employee.staff_lname}"
        manager = self.employee_repository.get_manager(application.staff_id)
        manager_email = manager.email
        # Prepare email data
        current_time = get_current_datetime_sgt()

        # Send email to manager
        if manager_email:
            manager_subject = get_application_withdrawn_manager_email_subject(withdrawn_application.staff_id,
                                                                              staff_name)
            manager_body = get_application_withdrawn_manager_email_template(
                manager_name=f"{manager.staff_fname} {manager.staff_lname}",
                employee_name=staff_name,
                employee_id=withdrawn_application.staff_id,
                application_id=withdrawn_application.application_id,
                reason=withdrawn_application.reason,
                status=withdrawn_application.status,
                withdrawn_on=current_time
            )
            self.email_service.send_email(manager_email, manager_subject, manager_body)

        # Send email to employee
        employee_subject = get_application_withdrawn_employee_email_subject(withdrawn_application.application_id)
        employee_body = get_application_withdrawn_employee_email_template(
            employee_name=staff_name,
            application_id=withdrawn_application.application_id,
            reason=withdrawn_application.reason,
            status=withdrawn_application.status,
            withdrawn_on=current_time
        )
        self.email_service.send_email(employee.email, employee_subject, employee_body)

        return withdrawn_application

    def get_applications_by_status(self, status: str) -> List[Type[Application]]:
        return self.application_repository.get_applications_by_status(status)

    def update_application_status(self, application_id: int, new_status: str) -> Application:
        return self.application_repository.update_application_status(application_id, new_status)