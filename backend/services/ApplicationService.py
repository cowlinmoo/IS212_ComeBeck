from dateutil.relativedelta import relativedelta
from fastapi import Depends, HTTPException
from typing import List, Type
from sqlalchemy.orm import InstrumentedAttribute
from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.models.enums.RecurrenceType import RecurrenceType
from backend.models.generators import get_current_datetime_sgt
from backend.models.generators import get_current_date
from backend.repositories.ApplicationRepository import ApplicationRepository
from backend.models import Application, Event
from backend.repositories.EmployeeRepository import EmployeeRepository
from backend.schemas.ApplicationSchema import (ApplicationCreateSchema,
                                               ApplicationWithdrawSchema, ApplicationApproveRejectSchema,
                                               ApprovedApplicationLocationSchema, ApplicationWithdrawEventSchema)
from backend.services.EmailService import EmailService
from backend.repositories.EventRepository import EventRepository
from backend.services.EventService import EventService


class ApplicationService:
    def __init__(self,
                 application_repository: ApplicationRepository = Depends(),
                 employee_repository: EmployeeRepository = Depends(),
                 email_service: EmailService = Depends(),
                 event_repository: EventRepository = Depends(),
                 event_service: EventService = Depends()
                 ):

        self.event_repository = event_repository
        self.event_service = event_service
        self.employee_repository = employee_repository
        self.application_repository = application_repository
        self.email_service = email_service

    def get_all_applications(self) -> List[Type[Application]]:
        return self.application_repository.get_all_applications()

    def get_application_by_id(self, application_id: int) -> Application:
        # check if application exists in the database
        if self.application_repository.get_application_by_application_id(application_id) is None:
            raise HTTPException(
                status_code=404, detail="Application not found")
        return self.application_repository.get_application_by_application_id(application_id)

    def get_applications_by_staff_id(self, staff_id: int) -> List[Type[Application]]:
        # check if employee exists in the database
        if self.employee_repository.get_employee(staff_id) is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return self.application_repository.get_application_by_staff_id(staff_id)

    def get_employee_approved_application_locations(self, manager_id: int, current_user_role: EmployeeRole) -> List[ApprovedApplicationLocationSchema]:
        employee_locations: List[ApprovedApplicationLocationSchema] = []
        approved_applications: List[Application] = self.application_repository.get_applications_by_status(
            status="approved")
        if current_user_role == EmployeeRole.MANAGER:
            employees = self.employee_repository.get_employees_under_manager(
                manager_id=manager_id)
            approved_applications = [application for application in approved_applications if application.staff_id in [
                employee.staff_id for employee in employees]]
        elif current_user_role == EmployeeRole.HR:
            pass
        for approved_application in approved_applications:
            user = self.employee_repository.get_employee(
                staff_id=approved_application.staff_id)
            for event in self.event_repository.get_event_by_application_id(application_id=approved_application.application_id):
                employee_locations.append(
                    ApprovedApplicationLocationSchema(
                        role=user.role,
                        application_hour=event.application_hour,
                        employee_fname=user.staff_fname,
                        employee_lname=user.staff_lname,
                        location=event.location,
                        position=user.position,
                        date=event.requested_date.isoformat()
                    )
                )
        return employee_locations
    def get_applications_by_approver_id(self, approver_id: int) -> List[Type[Application]]:
        # check if employee exists in the database
        if self.employee_repository.get_employee(approver_id) is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        return self.application_repository.get_applications_by_approver_id(approver_id)

    def create_application(self, application: ApplicationCreateSchema, application_state: str) -> Application:
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
        if application.end_date and application.end_date > max_end_date:
            raise HTTPException(status_code=400,
                                detail="End date cannot be more than 3 months away from the requested date")
        # Prepare application data
        application_dict = application.model_dump(
            exclude={"events", "location", "requested_date", "application_hour"})
        # set status to pending as it is a new application
        application_dict["status"] = "pending"
        application_dict["created_on"] = get_current_datetime_sgt()
        application_dict["last_updated_on"] = get_current_datetime_sgt()
        application_dict["approver_id"] = employee.reporting_manager
        application_dict["application_state"] = application_state
        # Create new application
        new_application = self.application_repository.create_application(
            application_dict)
        # Create events
        self.event_service.create_events(application, new_application.application_id)
        # Get Manager Details
        manager_id = employee.reporting_manager
        manager = self.employee_repository.get_employee(manager_id)
        staff_name = f"{employee.staff_fname} {employee.staff_lname}"
        # Send emails
        if application_state == "new_application":
            self.email_service.send_application_creation_emails(application, new_application, manager, employee, staff_name)
        return new_application

    def update_application(self, application_id: int, application: ApplicationCreateSchema) -> Application:
        existing_application = self.application_repository.get_application_by_application_id(
            application_id)
        if existing_application.status == "pending":
            return self.application_repository.update_application(application_id, application)
        elif existing_application.status == "withdrawn" or existing_application.status == "rejected":
            raise HTTPException(
                status_code=409, detail="Application has already been withdrawn or rejected")
        else:
            return self.change_request(existing_application, application)

    def withdraw_application_event(self, application_id, event_id, application:ApplicationWithdrawEventSchema) -> Event:
        existing_application = self.application_repository.get_application_by_application_id(application_id)
        existing_event = self.event_repository.get_event_by_event_id(event_id)
        # remove the event from the application

        if existing_application is None:
            raise HTTPException(
                status_code=404, detail="Application not found")

        # Fetch employee and editor data
        employee = self.employee_repository.get_employee(existing_application.staff_id)
        manager = self.employee_repository.get_employee(employee.reporting_manager)
        editor = self.employee_repository.get_employee(application.editor_id)

        if editor is None:
            raise HTTPException(status_code=404, detail="Editor not found")

        # Check if the editor is authorized (either the employee themselves or their manager)
        is_employee = existing_application.staff_id == application.editor_id
        is_manager = employee.reporting_manager == application.editor_id

        if not (is_employee or is_manager):
            raise HTTPException(status_code=403, detail="You are not authorized to withdraw this application")

        if existing_application.status == "withdrawn":
            raise HTTPException(status_code=409, detail="Application already withdrawn")

        if existing_application.status == "approved" and is_employee:
            return self.cancel_request_one(application_id, event_id, application.withdraw_reason)
        self.event_repository.delete_event(event_id)

        # Prepare email data
        current_time = get_current_datetime_sgt()
        # Send withdrawal emails
        self.email_service.send_event_withdrawal_emails(
            withdrawn_event=existing_event,
            employee=employee,
            manager=manager,
            is_employee=is_employee,
            current_time=current_time
        )
        return existing_event

    def withdraw_application(self, application_id: int, application: ApplicationWithdrawSchema) -> Application:
        existing_application = self.application_repository.get_application_by_application_id(
            application_id)

        if existing_application is None:
            raise HTTPException(
                status_code=404, detail="Application not found")

        # Fetch employee and editor data
        employee = self.employee_repository.get_employee(existing_application.staff_id)
        manager = self.employee_repository.get_employee(employee.reporting_manager)
        editor = self.employee_repository.get_employee(application.editor_id)

        if editor is None:
            raise HTTPException(status_code=404, detail="Editor not found")

        # Check if the editor is authorized (either the employee themselves or their manager)
        is_employee = existing_application.staff_id == application.editor_id
        is_manager = employee.reporting_manager == application.editor_id

        if not (is_employee or is_manager):
            raise HTTPException(status_code=403, detail="You are not authorized to withdraw this application")

        if existing_application.status == "withdrawn":
            raise HTTPException(status_code=409, detail="Application already withdrawn")

        if existing_application.status == "approved" and is_employee:
            return self.cancel_request(existing_application, application)
        withdrawn_application = self.application_repository.withdraw_application(application_id, application)

        # Prepare email data
        current_time = get_current_datetime_sgt()
        # Send withdrawal emails
        self.email_service.send_withdrawal_emails(
            withdrawn_application=withdrawn_application,
            employee=employee,
            editor=editor,
            manager=manager,
            is_employee=is_employee,
            current_time=current_time
        )
        return withdrawn_application

    def get_applications_by_status(self, status: str) -> List[Type[Application]]:
        return self.application_repository.get_applications_by_status(status)

    def update_application_status(self, application_id: int, new_status: str, outcome_reason: str) -> Application:
        return self.application_repository.update_application_status(application_id, new_status, outcome_reason)

    def reject_old_applications(self):
        pending_applications = self.application_repository.get_pending_applications()
        application_ids: List[int] = [int(getattr(app, 'application_id')
                                          if isinstance(app.application_id, InstrumentedAttribute)
                                          else app.application_id)
                                      for app in pending_applications
                                      if app.application_id is not None
                                      ]
        events = self.event_repository.get_events_by_application_ids(
            application_ids)

        two_months_ago = get_current_date() - relativedelta(months=2)
        rejected_count = 0

        event_application_ids = []
        for event in events:
            print(event_application_ids, "over here")
            if event.requested_date < two_months_ago:
                if event.application_id not in event_application_ids:
                    event_application_ids.append(event.application_id)
                    application=self.application_repository.update_application_status(event.application_id, 'rejected', 'Application automatically rejected due to old requested date')
                    rejected_count += 1
                    self.email_service.send_rejection_emails(application,event.requested_date)
        

        print(f"""Rejected {rejected_count} applications with events older than {
              two_months_ago}""")

    def approve_reject_pending_applications(self, application:ApplicationApproveRejectSchema) -> Application:
        application_id = application.application_id
        existing_application = self.application_repository.get_application_by_application_id(application_id)
        if not existing_application:
            raise HTTPException(status_code=404, detail="Application not found")
        if existing_application.status != 'pending':
            raise HTTPException(status_code=400, detail="Application is not pending")
        if existing_application.approver_id != application.approver_id:
            raise HTTPException(status_code=403, detail="You are not authorized to approve this application")
        if existing_application.application_state == "new_application":
            if application.status == "approved":
                self.application_repository.update_application_status(application_id, 'approved', application.outcome_reason)
            else:
                self.application_repository.update_application_status(application_id, 'rejected', application.outcome_reason)
            modified_application = self.application_repository.get_application_by_application_id(application_id)
            self.email_service.send_outcome_emails(modified_application)
        elif existing_application.application_state == "cancel_request":
            if application.status == "approved":
                self.application_repository.update_application_status(application_id, 'withdrawn', application.outcome_reason)
            else:
                self.application_repository.update_application_status(application_id, 'approved', application.outcome_reason)
            modified_application = self.application_repository.get_application_by_application_id(application_id)
            self.email_service.send_cancel_request_outcome_emails(modified_application)
        elif existing_application.application_state=="change_request":
            old_application = self.application_repository.get_application_by_application_id(existing_application.original_application_id)
            if application.status == "approved":
                self.application_repository.update_application_status(existing_application.application_id, 'approved', application.outcome_reason)
                self.application_repository.update_application_status(old_application.application_id, 'superseded', f"Superseded by change request (Application ID: {existing_application.application_id})")
            else:
                self.application_repository.update_application_status(existing_application.application_id, 'rejected', application.outcome_reason)
                self.application_repository.update_application_status(old_application.application_id, 'approved', f"Change request rejected (Application ID: {existing_application.application_id})")
            modified_application = self.application_repository.get_application_by_application_id(existing_application.application_id)
            self.email_service.send_change_request_outcome_emails(modified_application)
        elif existing_application.application_state=="cancel_one_request":
            if application.status == "approved":
                event = self.event_repository.get_first_event_by_application_id(application_id)
                self.event_repository.delete_event(event.event_id)
                self.application_repository.delete_application(application_id)
                self.email_service.send_cancel_one_request_outcome_emails(event, "approved")
            elif application.status == "rejected":
                previous_application = self.application_repository.get_application_by_application_id(existing_application.original_application_id)
                event = self.event_repository.get_first_event_by_application_id(application_id)
                self.event_repository.update_application_id(event.event_id, previous_application.application_id)
                self.application_repository.delete_application(application_id)
                self.email_service.send_cancel_one_request_outcome_emails(event, "rejected")
            modified_application = self.application_repository.get_application_by_application_id(existing_application.original_application_id)
        else:
            modified_application = existing_application
        return modified_application

    def cancel_request(self, existing_application: Application,
                       cancellation_request: ApplicationWithdrawSchema) -> Application:
        # Update application state to 'cancellation_request'
        updated_application = self.application_repository.update_application_state(
            existing_application.application_id,
            "cancel_request",
            "Cancellation requested",
            "pending"
        )
        # Fetch employee and manager data
        employee = self.employee_repository.get_employee(existing_application.staff_id)
        manager = self.employee_repository.get_employee(employee.reporting_manager)
        # Prepare email data
        current_time = get_current_datetime_sgt()
        # Send cancellation request emails
        self.email_service.send_cancellation_request_emails(
            existing_application,
            cancellation_request,
            employee,
            manager,
            current_time
        )
        return updated_application

    def change_request(self, existing_application: Application, change_request: ApplicationCreateSchema) -> Application:
        # Create a new application based on the change request
        new_application_dict = change_request.model_dump(exclude={"events", "location", "requested_date"})
        new_application_dict["status"] = "pending"
        new_application_dict["created_on"] = get_current_datetime_sgt()
        new_application_dict["last_updated_on"] = get_current_datetime_sgt()
        new_application_dict["approver_id"] = existing_application.approver_id
        new_application_dict["application_state"] = "change_request"
        new_application_dict["staff_id"] = existing_application.staff_id
        new_application_dict["original_application_id"] = existing_application.application_id

        # Create the new application
        new_application = self.application_repository.create_application(new_application_dict)

        # Create new events for the new application
        self.event_service.create_events(change_request, new_application.application_id)

        # Update the existing application to reference the new application
        self.application_repository.update_application_state(
            existing_application.application_id,
            "change_request",
            f"Superseded by change request (Application ID: {new_application.application_id})",
            "superseded"
        )

        # Fetch employee and manager data
        employee = self.employee_repository.get_employee(existing_application.staff_id)
        manager = self.employee_repository.get_employee(employee.reporting_manager)

        # Prepare email data
        current_time = get_current_datetime_sgt()

        # Send change request emails
        self.email_service.send_change_request_emails(
            existing_application,
            new_application,
            change_request,
            employee,
            manager,
            current_time
        )

        return new_application

    def cancel_request_one(self, application_id, event_id, withdraw_reason) -> Event:
        existing_application = self.application_repository.get_application_by_application_id(application_id)
        existing_event = self.event_repository.get_event_by_event_id(event_id)
        existing_date = existing_event.requested_date
        # create a new application with the event to be removed, and mark the status as pending
        application_to_be_cancelled = ApplicationCreateSchema(
            location=existing_event.location,
            application_hour=existing_event.application_hour,
            reason=existing_application.reason,
            requested_date=existing_date,
            description=existing_application.description,
            staff_id=existing_application.staff_id
        )
        new_application = self.create_application(application_to_be_cancelled, "cancel_one_request")
        self.application_repository.update_original_application_id(new_application.application_id, application_id)
        # remove the event from the application
        new_event = self.event_repository.get_first_event_by_application_id(new_application.application_id)
        self.event_repository.update_original_event_id(new_event.event_id, event_id)
        self.event_repository.delete_event(event_id)
        # Prepare email data
        employee = self.employee_repository.get_employee(existing_application.staff_id)
        manager = self.employee_repository.get_employee(employee.reporting_manager)
        current_time = get_current_datetime_sgt()
        # Send cancellation emails
        cancellation_reason = withdraw_reason
        self.email_service.send_cancel_one_request_emails(existing_event, employee, manager, cancellation_reason)
        return existing_event