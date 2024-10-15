import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastapi import Depends, HTTPException

from backend.config.EmailTemplates import get_new_application_manager_email_subject, \
    get_new_application_manager_email_template, get_new_application_employee_email_subject, \
    get_new_application_employee_email_template, get_cancellation_request_manager_email_subject, \
    get_cancellation_request_manager_email_template, get_cancellation_request_employee_email_subject, \
    get_cancellation_request_employee_email_template, get_application_outcome_employee_email_subject, \
    get_application_outcome_employee_email_template, get_application_outcome_approver_email_subject, \
    get_application_outcome_approver_email_template, get_application_auto_rejected_employee_email_subject, \
    get_application_auto_rejected_employee_email_template, get_application_withdrawn_manager_email_subject, \
    get_application_withdrawn_manager_email_template, get_application_withdrawn_employee_email_subject, \
    get_application_withdrawn_employee_email_template, get_cancel_request_manager_email_template, \
    get_cancel_request_employee_email_template, format_application_details, get_change_request_manager_email_subject, \
    get_change_request_manager_email_template, \
    get_change_request_employee_email_template, get_change_request_employee_email_subject, \
    get_change_request_outcome_manager_email_subject, get_change_request_outcome_manager_email_template, \
    get_change_request_outcome_employee_email_template, get_change_request_outcome_employee_email_subject, \
    get_event_withdrawn_manager_email_subject, get_event_withdrawn_employee_email_subject, \
    get_event_withdrawn_manager_email_template, get_event_withdrawn_employee_email_template, \
    get_event_cancellation_employee_email_template, get_event_cancellation_manager_email_template, \
    get_event_cancellation_manager_email_subject, get_event_cancellation_employee_email_subject, \
    get_cancel_one_request_outcome_manager_email_subject, get_cancel_one_request_outcome_employee_email_subject, \
    get_cancel_one_request_outcome_manager_email_template, get_cancel_one_request_outcome_employee_email_template
from backend.config.Environment import get_environment_variables
from backend.models import Application, Employee, Event
from backend.models.generators import get_current_date, get_current_datetime_sgt
from backend.repositories.EmployeeRepository import EmployeeRepository
from backend.schemas.ApplicationSchema import ApplicationCreateSchema, ApplicationWithdrawSchema

env = get_environment_variables()

class EmailService:
    def __init__(self,
                 employee_repository: EmployeeRepository = Depends()):
        self.smtp_server = env.SMTP_SERVER
        self.smtp_port = env.SMTP_PORT
        self.sender_email = env.SENDER_EMAIL
        self.sender_password = env.SENDER_PASSWORD
        self.employee_repository = employee_repository

    def send_email(self, recipient_email, subject, body):
        message = MIMEMultipart()
        message['From'] = self.sender_email
        message['To'] = recipient_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            print(f"Email sent successfully to {recipient_email}")
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

    def send_application_creation_emails(self, application: ApplicationCreateSchema, new_application: Application, manager: Employee,
                     employee: Employee, staff_name: str):
        # Determine if the application has multiple events
        has_multiple_events = len(application.events) > 1 if application.events else False

        # Create base subject lines
        prefix = "MULTIPLE: " if has_multiple_events else ("RECURRING: " if application.recurring else "ONE-TIME: ")

        # Send email to manager
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
            location=application.location,
            recurrence_type=application.recurrence_type.value if application.recurring else None,
            end_date=application.end_date if application.recurring else None,
            events=application.events if has_multiple_events else None
        )
        self.send_email(manager.email, manager_subject, manager_body)

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
            location=application.location,
            recurrence_type=application.recurrence_type.value if application.recurring else None,
            end_date=application.end_date if application.recurring else None,
            events=application.events if has_multiple_events else None
        )
        self.send_email(employee.email, employee_subject, employee_body)

    def send_outcome_emails(self, application):
        # Fetch employee and approver data
        employee = self.employee_repository.get_employee(application.staff_id)
        approver = self.employee_repository.get_employee(application.approver_id)

        if not employee or not approver:
            raise HTTPException(status_code=404, detail="Employee or approver not found")

        current_time = get_current_datetime_sgt()
        staff_name = f"{employee.staff_fname} {employee.staff_lname}"
        approver_name = f"{approver.staff_fname} {approver.staff_lname}"

        # Determine application type and prepare event_info
        if application.recurring:
            app_type = "recurring"
            event_info = {
                "recurrence_type": application.recurrence_type.value,
                "start_date": application.events[0].requested_date,
                "end_date": application.end_date
            }
        elif len(application.events) > 1:
            app_type = "multiple_dates"
            event_info = [{"date": event.requested_date, "location": event.location} for event in application.events]
        else:
            app_type = "one_time"
            event_info = {
                "date": application.events[0].requested_date,
                "location": application.events[0].location
            }

        # Send email to employee
        employee_subject = get_application_outcome_employee_email_subject(
            application_id=application.application_id,
            status=application.status,
        )
        employee_body = get_application_outcome_employee_email_template(
            employee_name=staff_name,
            application_id=application.application_id,
            status=application.status,
            reason=application.outcome_reason,
            description=application.description,
            decided_on=current_time,
            decided_by=approver_name,
            app_type=app_type,
            event_info=event_info
        )
        self.send_email(employee.email, employee_subject, employee_body)

        # Send email to approver (confirmation of their action)
        approver_subject = get_application_outcome_approver_email_subject(
            application_id=application.application_id,
            status=application.status,
            employee_name=staff_name,
        )
        approver_body = get_application_outcome_approver_email_template(
            approver_name=approver_name,
            employee_name=staff_name,
            employee_id=application.staff_id,
            application_id=application.application_id,
            status=application.status,
            reason=application.outcome_reason,
            description=application.description,
            decided_on=current_time,
            app_type=app_type,
            event_info=event_info
        )
        self.send_email(approver.email, approver_subject, approver_body)

    def send_change_request_emails(self, existing_application: Application, new_application: Application,
                                   change_request: ApplicationCreateSchema, employee: Employee, manager: Employee,
                                   current_time: datetime):
        staff_name = f"{employee.staff_fname} {employee.staff_lname}"
        manager_name = f"{manager.staff_fname} {manager.staff_lname}"

        original_details = format_application_details(existing_application)
        updated_details = format_application_details(change_request)

        # Send email to manager
        manager_subject = get_change_request_manager_email_subject(employee.staff_id, staff_name)
        manager_body = get_change_request_manager_email_template(
            manager_name=manager_name,
            employee_name=staff_name,
            employee_id=employee.staff_id,
            original_application_id=existing_application.application_id,
            new_application_id=new_application.application_id,
            original_details=original_details,
            updated_details=updated_details,
            current_time=current_time
        )
        self.send_email(manager.email, manager_subject, manager_body)

        # Send email to employee
        employee_subject = get_change_request_employee_email_subject(new_application.application_id)
        employee_body = get_change_request_employee_email_template(
            employee_name=staff_name,
            original_application_id=existing_application.application_id,
            new_application_id=new_application.application_id,
            original_details=original_details,
            updated_details=updated_details,
            current_time=current_time
        )
        self.send_email(employee.email, employee_subject, employee_body)

    def send_cancellation_request_emails(self, existing_application: Application, cancellation_request: ApplicationWithdrawSchema,
                                         employee: Employee, manager: Employee, current_time: datetime):
        staff_name = f"{employee.staff_fname} {employee.staff_lname}"
        manager_name = f"{manager.staff_fname} {manager.staff_lname}"

        # Determine if it's a recurring application
        recurring = existing_application.recurring

        # Get the first event's requested date and location
        first_event = existing_application.events[0] if existing_application.events else None
        requested_date = first_event.requested_date if first_event else None
        location = first_event.location if first_event else None

        # Prepare common email data
        common_email_data = {
            "application_id": existing_application.application_id,
            "original_reason": existing_application.reason,
            "requested_date": requested_date,
            "description": existing_application.description,
            "status": existing_application.status,
            "created_on": current_time,
            "location": location,
            "recurring": recurring,
            "recurrence_type": existing_application.recurrence_type,
            "end_date": existing_application.end_date,
            "cancellation_reason": cancellation_request.withdraw_reason
        }

        # Send email to manager
        manager_subject = get_cancellation_request_manager_email_subject(existing_application.staff_id, staff_name)
        manager_body = get_cancellation_request_manager_email_template(
            manager_name=manager_name,
            employee_name=staff_name,
            employee_id=existing_application.staff_id,
            **common_email_data
        )
        self.send_email(manager.email, manager_subject, manager_body)

        # Send email to employee
        employee_subject = get_cancellation_request_employee_email_subject(existing_application.application_id)
        employee_body = get_cancellation_request_employee_email_template(
            employee_name=staff_name,
            **common_email_data
        )
        self.send_email(employee.email, employee_subject, employee_body)

    def send_rejection_emails(self, application: Application,req_date):
        employee = self.employee_repository.get_employee(application.staff_id)
        staff_name = f"{employee.staff_fname} {employee.staff_lname}"

        employee_subject = get_application_auto_rejected_employee_email_subject(application.application_id)
        employee_body = get_application_auto_rejected_employee_email_template(
            employee_name=staff_name,
            application_id=application.application_id,
            reason=application.outcome_reason,
            status=application.status,
            date_req=req_date
        )
        self.send_email(employee.email, employee_subject, employee_body)
    def send_withdrawal_emails(self, withdrawn_application: Application, employee: Employee, editor: Employee,
                               manager: Employee, is_employee: bool, current_time: datetime):
        staff_name = f"{employee.staff_fname} {employee.staff_lname}"
        editor_name = f"{editor.staff_fname} {editor.staff_lname}"

        # Send email to manager
        if manager and manager.email:
            manager_subject = get_application_withdrawn_manager_email_subject(
                withdrawn_application.staff_id, staff_name, is_employee
            )
            manager_body = get_application_withdrawn_manager_email_template(
                manager_name=f"{manager.staff_fname} {manager.staff_lname}",
                employee_name=staff_name,
                employee_id=withdrawn_application.staff_id,
                application_id=withdrawn_application.application_id,
                reason=withdrawn_application.outcome_reason,
                status=withdrawn_application.status,
                withdrawn_on=current_time,
                withdrawn_by="employee" if is_employee else "you"
            )
            self.send_email(manager.email, manager_subject, manager_body)

        # Send email to employee
        employee_subject = get_application_withdrawn_employee_email_subject(
            withdrawn_application.application_id, is_employee
        )
        employee_body = get_application_withdrawn_employee_email_template(
            employee_name=staff_name,
            application_id=withdrawn_application.application_id,
            reason=withdrawn_application.outcome_reason,
            status=withdrawn_application.status,
            withdrawn_on=current_time,
            withdrawn_by="you" if is_employee else editor_name
        )
        self.send_email(employee.email, employee_subject, employee_body)

    def send_cancel_request_outcome_emails(self, modified_application: Application):
        # Fetch employee and manager data
        employee = self.employee_repository.get_employee(modified_application.staff_id)
        manager = self.employee_repository.get_employee(modified_application.approver_id)

        # Prepare email data
        current_time = get_current_datetime_sgt()
        status = modified_application.status
        if status == "withdrawn":
            status = "approved"
        elif status == "approved":
            status = "rejected"

        # Send email to employee
        self.send_email_to_employee(employee, modified_application, status, current_time)

        # Send email to manager
        self.send_email_to_manager(manager, employee, modified_application, status, current_time)

    def send_email_to_employee(self, employee: Employee, application: Application, status: str, current_time: datetime):
        subject = f"Cancel Request {status.capitalize()} for Application #{application.application_id}"

        body = get_cancel_request_employee_email_template(
            employee_name=employee.staff_fname,
            application_id=application.application_id,
            status=status,
            outcome_reason=application.outcome_reason,
            current_time=current_time,
            is_recurring=application.recurring,
            recurrence_type=application.recurrence_type.value if application.recurrence_type else None
        )

        self.send_email(employee.email, subject, body)

    def send_email_to_manager(self, manager: Employee, employee: Employee, application: Application, status: str,
                              current_time: datetime):
        subject = f"Cancel Request {status.capitalize()} for {employee.staff_fname} {employee.staff_lname}"

        body = get_cancel_request_manager_email_template(
            manager_name=manager.staff_fname,
            employee_name=f"{employee.staff_fname} {employee.staff_lname}",
            application_id=application.application_id,
            status=status,
            outcome_reason=application.outcome_reason,
            current_time=current_time,
            is_recurring=application.recurring,
            recurrence_type=application.recurrence_type.value if application.recurrence_type else None
        )

        self.send_email(manager.email, subject, body)

    def send_change_request_outcome_emails(self, modified_application: Application):
        # Fetch employee and manager data
        employee = self.employee_repository.get_employee(modified_application.staff_id)
        manager = self.employee_repository.get_employee(modified_application.approver_id)

        if not employee or not manager:
            raise HTTPException(status_code=404, detail="Employee or manager not found")

        # Prepare email data
        current_time = get_current_datetime_sgt()
        status = modified_application.status
        staff_name = f"{employee.staff_fname} {employee.staff_lname}"
        manager_name = f"{manager.staff_fname} {manager.staff_lname}"

        # Format application details
        original_details = format_application_details(modified_application.original_application)
        updated_details = format_application_details(modified_application)

        # Send email to employee
        employee_subject = get_change_request_outcome_employee_email_subject(
            modified_application.application_id, status
        )
        employee_body = get_change_request_outcome_employee_email_template(
            employee_name=employee.staff_fname,
            application_id=modified_application.application_id,
            status=status,
            outcome_reason=modified_application.outcome_reason,
            current_time=current_time,
            original_details=original_details,
            updated_details=updated_details
        )
        self.send_email(employee.email, employee_subject, employee_body)

        # Send email to manager
        manager_subject = get_change_request_outcome_manager_email_subject(staff_name, status)
        manager_body = get_change_request_outcome_manager_email_template(
            manager_name=manager_name,
            employee_name=staff_name,
            application_id=modified_application.application_id,
            status=status,
            outcome_reason=modified_application.outcome_reason,
            current_time=current_time,
            original_details=original_details,
            updated_details=updated_details
        )
        self.send_email(manager.email, manager_subject, manager_body)

    def send_event_withdrawal_emails(self, withdrawn_event, employee, manager, is_employee, current_time):
        event_id = withdrawn_event.event_id
        application_id = withdrawn_event.application_id
        employee_name = f"{employee.staff_fname} {employee.staff_lname}"
        withdrawn_by = "you" if is_employee else manager.staff_fname

        # Determine the email subjects
        manager_subject = get_event_withdrawn_manager_email_subject(event_id, application_id)
        employee_subject = get_event_withdrawn_employee_email_subject(event_id, application_id)

        # Prepare the email bodies
        manager_body = get_event_withdrawn_manager_email_template(
            manager_name=manager.staff_fname,
            employee_name=employee_name,
            event_id=event_id,
            application_id=application_id,
            requested_date=withdrawn_event.requested_date,
            location=withdrawn_event.location,
            withdrawn_on=current_time,
            withdrawn_by=withdrawn_by
        )

        employee_body = get_event_withdrawn_employee_email_template(
            employee_name=employee_name,
            event_id=event_id,
            application_id=application_id,
            requested_date=withdrawn_event.requested_date,
            location=withdrawn_event.location,
            withdrawn_on=current_time,
            withdrawn_by=withdrawn_by
        )

        # Send emails
        self.send_email(manager.email, manager_subject, manager_body)
        self.send_email(employee.email, employee_subject, employee_body)

    def send_cancel_one_request_emails(self, event: Event, employee: Employee, manager: Employee,
                                       cancellation_reason: str):
        staff_name = f"{employee.staff_fname} {employee.staff_lname}"
        manager_name = f"{manager.staff_fname} {manager.staff_lname}"

        # Get current time for the email
        current_time = datetime.now()

        # Prepare subjects
        manager_subject = get_event_cancellation_manager_email_subject(event.event_id, staff_name)
        employee_subject = get_event_cancellation_employee_email_subject(event.event_id)

        # Prepare email bodies
        manager_body = get_event_cancellation_manager_email_template(
            manager_name=manager_name,
            employee_name=staff_name,
            employee_id=employee.staff_id,
            event_id=event.event_id,
            requested_date=event.requested_date,
            location=event.location,
            cancellation_reason=cancellation_reason,
            current_time=current_time
        )

        employee_body = get_event_cancellation_employee_email_template(
            employee_name=staff_name,
            event_id=event.event_id,
            requested_date=event.requested_date,
            location=event.location,
            cancellation_reason=cancellation_reason,
            current_time=current_time
        )

        # Send emails
        self.send_email(manager.email, manager_subject, manager_body)
        self.send_email(employee.email, employee_subject, employee_body)

    def send_cancel_one_request_outcome_emails(self, event, outcome: str):
        employee = self.employee_repository.get_employee(event.application.staff_id)
        manager = self.employee_repository.get_employee(employee.reporting_manager)
        current_time = datetime.now()

        # Prepare email subjects
        manager_subject = get_cancel_one_request_outcome_manager_email_subject(event.original_event_id, outcome)
        employee_subject = get_cancel_one_request_outcome_employee_email_subject(event.original_event_id, outcome)

        # Prepare email bodies
        manager_body = get_cancel_one_request_outcome_manager_email_template(
            manager_name=f"{manager.staff_fname} {manager.staff_lname}",
            employee_name=f"{employee.staff_fname} {employee.staff_lname}",
            event_id=event.original_event_id,
            outcome=outcome,
            current_time=current_time
        )

        employee_body = get_cancel_one_request_outcome_employee_email_template(
            employee_name=f"{employee.staff_fname} {employee.staff_lname}",
            event_id=event.original_event_id,
            outcome=outcome,
            current_time=current_time
        )

        # Send emails
        self.send_email(manager.email, manager_subject, manager_body)
        self.send_email(employee.email, employee_subject, employee_body)