from datetime import timedelta
from dateutil.relativedelta import relativedelta
from fastapi import Depends, HTTPException
from typing import List, Type

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from backend.config.EmailTemplates import (get_new_application_manager_email_subject,
                                           get_new_application_manager_email_template,
                                           get_new_application_employee_email_subject,
                                           get_new_application_employee_email_template,
                                           get_application_withdrawn_employee_email_subject,
                                           get_application_withdrawn_employee_email_template,
                                           get_application_withdrawn_manager_email_subject,
                                           get_application_withdrawn_manager_email_template)
from backend.models.enums.RecurrenceType import RecurrenceType
from backend.models.generators import get_current_datetime_sgt
from backend.models.generators import get_current_date
from backend.repositories.ApplicationRepository import ApplicationRepository
from backend.models import Application, Event, Employee
from backend.repositories.EmployeeRepository import EmployeeRepository
from backend.schemas.ApplicationSchema import (ApplicationCreateSchema, ApplicationUpdateSchema,
                                               ApplicationWithdrawSchema)
from backend.services.EmailService import EmailService
from backend.services.EventService import EventService


class ApplicationService:
    def __init__(self,
                 application_repository: ApplicationRepository = Depends(),
                 employee_repository: EmployeeRepository = Depends(),
                 email_service: EmailService = Depends(),
                 event_service: EventService = Depends()
                 ):

        self.event_service = event_service
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

    def create_application(self, application: ApplicationCreateSchema) -> ApplicationCreateSchema:
        # check if employee exists in the database
        employee = self.employee_repository.get_employee(application.staff_id)
        if employee is None:
            raise HTTPException(status_code=404, detail="Employee not found")

        # Check if recurring application has necessary fields
        if application.recurring:
            if not application.recurrence_type or not application.end_date:
                raise HTTPException(status_code=400,
                                    detail="Recurring applications must have recurrence_type and end_date set")

        max_end_date = application.requested_date + relativedelta(months=3)
        if application.end_date > max_end_date:
            raise HTTPException(status_code=400, detail="End date cannot be more than 3 months away from the requested date")
        # Prepare application data
        application_dict = application.model_dump(exclude={"requested_date", "location"})
        application_dict["status"] = "pending" # set status to pending as it is a new application
        application_dict["created_on"] = get_current_datetime_sgt()
        application_dict["last_updated_on"] = get_current_datetime_sgt()

        # Create new application
        new_application = self.application_repository.create_application(application_dict)

        if application.recurring:
            self._create_recurring_events(application, new_application.application_id)

        else:
            self._create_single_event(application, new_application.application_id)

        # Get Manager Details
        manager_id = employee.reporting_manager
        manager = self.employee_repository.get_employee(manager_id)
        manager_email = manager.email
        staff_name = f"{employee.staff_fname} {employee.staff_lname}"
        employee_email = employee.email

        # Send emails
        self._send_emails(application, new_application, manager, employee, staff_name)

        return application

    def _create_single_event(self, application: ApplicationCreateSchema, application_id: int):
        event = Event(
            requested_date=application.requested_date,
            location=application.location,
            application_id=application_id
        )
        self.event_service.create_event(event)

    def _create_recurring_events(self, application: ApplicationCreateSchema, application_id: int):
        current_date = application.requested_date
        end_date = application.end_date or (
                    current_date + timedelta(days=365))  # Default to one year if no end_date

        while current_date <= end_date:
            event = Event(
                requested_date=current_date,
                location=application.location,
                application_id=application_id
            )
            self.event_service.create_event(event)

            if application.recurrence_type == RecurrenceType.DAILY:
                current_date += timedelta(days=1)
            elif application.recurrence_type == RecurrenceType.WEEKLY:
                current_date += timedelta(weeks=1)
            elif application.recurrence_type == RecurrenceType.MONTHLY:
                # Move to the same day next month
                if current_date.month == 12:
                    current_date = current_date.replace(year=current_date.year + 1, month=1)
                else:
                    current_date = current_date.replace(month=current_date.month + 1)

    def _send_emails(self, application: ApplicationCreateSchema, new_application: Application, manager: Employee,
                     employee: Employee, staff_name: str):
        # Determine if the application is recurring
        is_recurring = application.recurring

        # Create base subject lines using the provided methods
        # Add prefix based on whether the application is recurring or one-time
        prefix = "RECURRING: " if is_recurring else "ONE-TIME: "

        # Send email to manager
        # Add "RECURRING: " to subject if the application is recurring
        base_manager_subject = get_new_application_manager_email_subject(application.staff_id, staff_name)
        manager_subject = f"{prefix}{base_manager_subject}"
        manager_body = get_new_application_manager_email_template(
            manager_name=f"{manager.staff_fname} {manager.staff_lname}",
            employee_name=staff_name,
            employee_id=application.staff_id,
            application_id=new_application.application_id,
            reason=application.reason,
            requested_date=application.requested_date,
            description=application.description,
            status=new_application.status,
            created_on=get_current_date(),
            recurring=application.recurring,
            recurrence_type=application.recurrence_type.value if application.recurring else None,
            end_date=application.end_date if application.recurring else None
        )
        self.email_service.send_email(manager.email, manager_subject, manager_body)

        # Send email to employee
        base_employee_subject = get_new_application_employee_email_subject(new_application.application_id)
        employee_subject = f"{prefix}{base_employee_subject}"
        employee_body = get_new_application_employee_email_template(
            employee_name=staff_name,
            application_id=new_application.application_id,
            reason=application.reason,
            requested_date=application.requested_date,
            description=application.description,
            status=new_application.status,
            created_on=get_current_date(),
            recurring=application.recurring,
            recurrence_type=application.recurrence_type.value if application.recurring else None,
            end_date=application.end_date if application.recurring else None
        )
        self.email_service.send_email(employee.email, employee_subject, employee_body)

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
        manager_id = employee.reporting_manager
        manager = self.employee_repository.get_employee(manager_id)
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
    
    def reject_old_applications(self) -> int:
        try:
            two_months_ago = get_current_datetime_sgt() - timedelta(days=60)
            rejected_count = self.application_repository.reject_applications_older_than(two_months_ago)
            print(f"Rejected {rejected_count} pending applications older than {two_months_ago}")
        except Exception as e:
            print(f"Error rejecting old applications: {str(e)}")
        
    def setup_application_cleanup_scheduler(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(
            self.reject_old_applications,
            trigger=CronTrigger(second='10'),  # Run at midnight every day
            id='reject_old_applications',
            name='Reject applications older than 2 months',
            replace_existing=True
        )
        return scheduler
