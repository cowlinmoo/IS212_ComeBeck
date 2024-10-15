from datetime import datetime, date
from typing import Optional, List, Union, Dict

from sqlalchemy.orm import Query

from backend.schemas.EventSchema import EventCreateSchema


def get_new_application_manager_email_subject(staff_id: int, employee_name: str) -> str:
    return f"New Application Request from Employee ID: {staff_id} - {employee_name}"

def get_new_application_employee_email_subject(application_id: int) -> str:
    return f"Application Submitted - Application ID: {application_id}"

def get_application_withdrawn_manager_email_subject(staff_id: int, employee_name: str, withdrawn_by_employee: bool) -> str:
    action = "Withdrawn" if withdrawn_by_employee else "Cancelled"
    return f"Application {action} for Employee ID: {staff_id} - {employee_name}"

def get_application_withdrawn_employee_email_subject(application_id: int, withdrawn_by_employee: bool) -> str:
    action = "WITHDRAWN" if withdrawn_by_employee else "CANCELLED"
    return f"{action}: Application {action.lower()} - Application ID: {application_id}"

def get_application_auto_rejected_employee_email_subject(application_id: int) -> str:
    return f"REJECTED: Application Auto Rejected - Application ID: {application_id}"

def get_new_application_manager_email_template(
    manager_name: str,
    employee_name: str,
    employee_id: int,
    application_id: int,
    reason: str,
    requested_date: date,
    description: str,
    status: str,
    created_on: date,
    location: str,
    recurring: bool = False,
    recurrence_type: Optional[str] = None,
    end_date: Optional[date] = None,
    events: Optional[List[EventCreateSchema]] = None
) -> str:
    if events and len(events) > 1:
        event_info = "Multiple Dates:\n"
        for idx, event in enumerate(events, 1):
            event_info += f"Event {idx}: Date: {event.requested_date}\n"
    elif recurring:
        event_info = f"""
Recurring Details:
------------------
Recurrence Type: {recurrence_type}
Start Date: {requested_date}
End Date: {end_date}
"""
    else:
        event_info = f"Requested Date: {requested_date}\n"

    return f"""
Dear {manager_name},

This is to inform you that a new application has been submitted for your review.

Application Details:
--------------------
Employee Name: {employee_name}
Employee ID: {employee_id}
Application ID: {application_id}
Reason: {reason}
Description: {description if description else "No additional description provided"}
Location: {location}
Status: {status}
Submission Date: {created_on}

{event_info}

If you require any additional information or have any questions regarding this application, please don't hesitate to contact the HR department.

Thank you for your prompt attention to this matter.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """

def get_new_application_employee_email_template(
    employee_name: str,
    application_id: int,
    reason: str,
    requested_date: date,
    description: str,
    status: str,
    created_on: date,
    location: str,
    recurring: bool = False,
    recurrence_type: Optional[str] = None,
    end_date: Optional[date] = None,
    events: Optional[List[EventCreateSchema]] = None
) -> str:
    if events and len(events) > 1:
        event_info = "Multiple Dates:\n"
        for idx, event in enumerate(events, 1):
            event_info += f"Event {idx}: Date: {event.requested_date}\n"
    elif recurring:
        event_info = f"""
Recurring Details:
------------------
Recurrence Type: {recurrence_type}
Start Date: {requested_date}
End Date: {end_date}
"""
    else:
        event_info = f"Requested Date: {requested_date}\n"

    return f"""
Dear {employee_name},

This email confirms that your application has been successfully submitted.

Application Details:
--------------------
Application ID: {application_id}
Reason: {reason}
Description: {description if description else "No additional description provided"}
Location: {location}
Status: {status}
Submission Date: {created_on}

{event_info}

Your application has been received and will be reviewed by your manager. You will be notified of any updates or decisions regarding your application.

If you need to make any changes or have any questions about your application, please contact the HR department.

Thank you for using our application system.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """

def get_application_withdrawn_manager_email_template(manager_name: str, employee_name: str, employee_id: int, application_id: int, reason: str, status: str, withdrawn_on: datetime, withdrawn_by: str) -> str:
    action = "withdrawn" if withdrawn_by == "employee" else "cancelled"
    return f"""
Dear {manager_name},

This is to inform you that an application has been {action} {"by" if withdrawn_by == "employee" else "for"} one of your employees.

Application Details:
--------------------
Employee Name: {employee_name}
Employee ID: {employee_id}
Application ID: {application_id}
Reason: {reason}
Status: {status}
{action.capitalize()} On: {withdrawn_on}
{action.capitalize()} By: {withdrawn_by.capitalize()}

If you have any questions regarding this {action}, please contact the HR department.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """

def get_application_withdrawn_employee_email_template(employee_name: str, application_id: int, reason: str, status: str, withdrawn_on: datetime, withdrawn_by: str) -> str:
    action = "withdrawn" if withdrawn_by == "you" else "cancelled"
    return f"""
Dear {employee_name},

This email confirms that your application has been {action} {"by you" if withdrawn_by == "you" else f"by your manager ({withdrawn_by})"}.

Application Details:
--------------------
Application ID: {application_id}
Reason: {reason}
Status: {status}
{action.capitalize()} On: {withdrawn_on}
{action.capitalize()} By: {withdrawn_by.capitalize()}

If you need to submit a new application or have any questions, please contact the HR department.

Thank you for using our application system.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """
def get_application_auto_rejected_employee_email_template(employee_name: str, application_id: int, reason: str, status: str, date_req: datetime) -> str:
    return f"""
Dear {employee_name},

This email is to notify you that your application has been auto rejected as 2 months has passed the requested date.

Application Details:
--------------------
Application ID: {application_id}
Reason: {reason}
Status: {status}
Date Requested: {date_req}

If you need to submit a new application or have any questions, please contact the HR department.

Thank you for using our application system.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """
def get_application_outcome_employee_email_subject(application_id: int, status: str) -> str:
    status_upper = status.upper()
    return f"Application {status_upper} - ID: {application_id}"

def get_application_outcome_approver_email_subject(application_id: int, status: str, employee_name: str) -> str:
    status_upper = status.upper()
    return f"Confirmation: Application {status_upper} - ID: {application_id} - {employee_name}"

def get_application_outcome_employee_email_template(
    employee_name: str,
    application_id: int,
    status: str,
    reason: str,
    description: str,
    decided_on: datetime,
    decided_by: str,
    app_type: str,
    event_info: Union[Dict, List]
) -> str:
    event_details = _format_event_details(app_type, event_info)

    reason_prefix = "Reason for rejection: " if status == "rejected" else "Reason: "

    return f"""
Dear {employee_name},

This email is to inform you that a decision has been made regarding your application.

Application Details:
--------------------
Application ID: {application_id}
Status: {status.upper()}
Description: {description if description else "No additional description provided"}

{event_details}

Decision Details:
-----------------
Decision made on: {decided_on}
Decision made by: {decided_by}
{reason_prefix}{reason}

If you have any questions about this decision, please contact your manager or the HR department.

Thank you for using our application system.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """

def get_application_outcome_approver_email_template(
    approver_name: str,
    employee_name: str,
    employee_id: str,
    application_id: int,
    status: str,
    reason: str,
    description: str,
    decided_on: datetime,
    app_type: str,
    event_info: Union[Dict, List]
) -> str:
    event_details = _format_event_details(app_type, event_info)

    reason_prefix = "Reason for rejection: " if status == "rejected" else "Reason: "

    return f"""
Dear {approver_name},

This email confirms that you have made a decision on the following application:

Application Details:
--------------------
Application ID: {application_id}
Employee: {employee_name} (ID: {employee_id})
Status: {status.upper()}
Description: {description if description else "No additional description provided"}

{event_details}

Decision Details:
-----------------
Decision made on: {decided_on}
{reason_prefix}{reason}

If you need to make any changes to this decision or have any questions, please contact the HR department.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """

def _format_event_details(app_type: str, event_info: Union[Dict, List]) -> str:
    if app_type == "recurring":
        return f"""
Recurring Application Details:
------------------------------
Recurrence Type: {event_info['recurrence_type']}
Start Date: {event_info['start_date']}
End Date: {event_info['end_date']}
"""
    elif app_type == "multiple_dates":
        details = "Multiple Dates Application:\n"
        for idx, event in enumerate(event_info, 1):
            details += f"Event {idx}: Date: {event['date']}, Location: {event['location']}\n"
        return details
    else:  # one_time
        return f"""
Application Details:
--------------------
Date: {event_info['date']}
Location: {event_info['location']}
"""
def get_cancellation_request_manager_email_subject(staff_id: int, employee_name: str) -> str:
    return f"Cancellation Request for Employee ID: {staff_id} - {employee_name}"

def get_cancellation_request_employee_email_subject(application_id: int) -> str:
    return f"Cancellation Request Submitted - Application ID: {application_id}"

def get_cancellation_request_manager_email_template(
    manager_name: str,
    employee_name: str,
    employee_id: int,
    application_id: int,
    original_reason: str,
    requested_date: date,
    description: str,
    status: str,
    created_on: datetime,
    location: str,
    recurring: bool = False,
    recurrence_type: Optional[str] = None,
    end_date: Optional[date] = None,
    cancellation_reason: str = None
) -> str:
    if recurring:
        event_info = f"""
Recurring Details:
------------------
Recurrence Type: {recurrence_type}
Start Date: {requested_date}
End Date: {end_date}
"""
    else:
        event_info = f"Date: {requested_date}"

    return f"""
Dear {manager_name},

A cancellation request has been submitted for an existing application that requires your review.

Cancellation Request Details:
---------------------
Reason for Cancellation: {cancellation_reason if cancellation_reason else "No reason provided"}
Submission Date of Cancellation Request: {created_on}

Original Application Details:
--------------------
Employee Name: {employee_name}
Employee ID: {employee_id}
Application ID: {application_id}
Status: {status}
Location: {location}
Reason: {original_reason}
Description: {description if description else "No description provided"}
{event_info}

Please review this cancellation request and take appropriate action. If you require any additional information or have any questions regarding this cancellation request, please don't hesitate to contact the HR department.

Thank you for your prompt attention to this matter.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """

def get_cancellation_request_employee_email_template(
    employee_name: str,
    application_id: int,
    original_reason: str,
    requested_date: date,
    description: str,
    status: str,
    created_on: datetime,
    location: str,
    recurring: bool = False,
    recurrence_type: Optional[str] = None,
    end_date: Optional[date] = None,
    cancellation_reason: str = None
) -> str:
    if recurring:
        event_info = f"""
Recurring Details:
------------------
Recurrence Type: {recurrence_type}
Start Date: {requested_date}
End Date: {end_date}
"""
    else:
        event_info = f"Date: {requested_date}"

    return f"""
Dear {employee_name},

This email confirms that your cancellation request for an existing application has been successfully submitted.

Cancellation Request Details:
---------------------
Reason for Cancellation: {cancellation_reason if cancellation_reason else "No reason provided"}
Submission Date of Cancellation Request: {created_on}

Original Application Details:
--------------------
Application ID: {application_id}
Status: {status}
Location: {location}
Reason: {original_reason}
Description: {description if description else "No description provided"}
{event_info}

Your cancellation request has been received and will be reviewed by your manager. You will be notified of any updates or decisions regarding your request.

If you need to make any changes or have any questions about your cancellation request, please contact the HR department.

Thank you for using our application system.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """


def get_cancel_request_employee_email_template(employee_name, application_id, status, outcome_reason, current_time,
                                               is_recurring, recurrence_type):
    recurring_info = f"This is a recurring application with {recurrence_type} recurrence." if is_recurring else "This is a one-time application."

    if status == 'approved':
        body = f"""
Dear {employee_name},

Your cancellation request for Application ID: {application_id} has been approved.

{recurring_info}

The application has been successfully cancelled as per your request.

If you have any questions, please contact your reporting manager.

Date and Time: {current_time}

Best regards,
HR Department
        """
    else:  # status == 'rejected'
        body = f"""
Dear {employee_name},

Your cancellation request for Application ID: {application_id} has been rejected.

{recurring_info}

Reason for rejection: {outcome_reason}

The original approved application remains valid. If you have any questions, please contact your reporting manager.

Date and Time: {current_time}

Best regards,
HR Department
        """
    return body


def get_cancel_request_manager_email_template(manager_name, employee_name, application_id, status, outcome_reason,
                                              current_time, is_recurring, recurrence_type):
    recurring_info = f"This is a recurring application with {recurrence_type} recurrence." if is_recurring else "This is a one-time application."

    body = f"""
Dear {manager_name},

This is to confirm that you have {status} the cancellation request for the following application:

Employee: {employee_name}
Application ID: {application_id}

{recurring_info}

{"The application has been successfully cancelled." if status == 'approved' else "The original approved application remains valid."}

{"Reason for rejection: " + outcome_reason if status == 'rejected' else ""}

Date and Time: {current_time}

Best regards,
HR Department
    """
    return body

def get_change_request_manager_email_subject(staff_id, staff_name):
    return f"Change Request for Application from {staff_id} - {staff_name}"

def get_change_request_employee_email_subject(application_id):
    return f"Change Request Submitted for Application ID: {application_id}"
def get_change_request_manager_email_template(manager_name, employee_name, employee_id, original_application_id, new_application_id, original_details, updated_details, current_time):
    template = f"""
Dear {manager_name},

A change request has been submitted for an existing application that requires your review.

Employee: {employee_name} (ID: {employee_id})
New Application ID: {new_application_id}
Original Application ID: {original_application_id}
Submitted on: {current_time}

Updated Application Details:
----------------------------
{updated_details}

Original Application Details:
-----------------------------
{original_details}

Please review this change request and take appropriate action through the application management system.

Best regards,
HR Department
"""
    return template

def get_change_request_employee_email_template(employee_name, original_application_id, new_application_id, original_details, updated_details, current_time):
    template = f"""
Dear {employee_name},

Your change request for Application ID: {original_application_id} has been submitted successfully.

New Application ID: {new_application_id}
Original Application ID: {original_application_id}
Submitted on: {current_time}

Updated Application Details:
----------------------------
{updated_details}

Original Application Details:
-----------------------------
{original_details}

Your manager will review this change request and take appropriate action. You will be notified of any updates.

Best regards,
HR Department
"""
    return template


def format_application_details(application):
    details = [
        f"Reason: {application.reason}",
        f"Description: {application.description or 'N/A'}",
        f"Recurring: {'Yes' if application.recurring else 'No'}"
    ]

    # Handle location and events
    if hasattr(application, 'location') and application.location:
        details.append(f"Location: {application.location}")

    if hasattr(application, 'requested_date') and application.requested_date:
        details.append(f"Requested Date: {application.requested_date}")

    # Handle recurring information and events
    if application.recurring:
        if hasattr(application, 'events'):
            first_event = application.events.first() if isinstance(application.events, Query) else next(iter(application.events), None)
            if first_event:
                details.append(f"Location: {first_event.location}")
                details.append(f"Requested Date: {first_event.requested_date}")
        recurrence_type = getattr(application.recurrence_type, 'value', application.recurrence_type) if application.recurrence_type else 'N/A'
        details.extend([
            f"Recurrence Type: {recurrence_type}",
            f"End Date: {application.end_date or 'N/A'}"
        ])
    elif hasattr(application, 'events') and application.events:
        details.append("\nEvents:")
        for event in application.events:
            details.append(f"- Date: {event.requested_date}")
    elif not (hasattr(application, 'location') and application.location):
        details.append("No location or event information available.")

    return "\n".join(details)

def get_change_request_outcome_employee_email_subject(application_id: int, status: str) -> str:
    return f"Change Request {status.capitalize()} for Application #{application_id}"

def get_change_request_outcome_employee_email_template(
    employee_name: str,
    application_id: int,
    status: str,
    outcome_reason: str,
    current_time: datetime,
    original_details: str,
    updated_details: str
) -> str:
    return f"""
Dear {employee_name},

Your change request for Application ID: {application_id} has been {status}.

Status: {status.capitalize()}
Reason: {outcome_reason}
Decision Time: {current_time}

{"Note: The original approved application remains valid. If you have any questions, please contact your reporting manager." if status == 'rejected' else ""}

Updated Application Details:
----------------------------
{updated_details}

Original Application Details:
-----------------------------
{original_details}

If you have any questions, please contact your manager.

Best regards,
HR Department
"""

def get_change_request_outcome_manager_email_subject(employee_name: str, status: str) -> str:
    return f"Change Request {status.capitalize()} for {employee_name}"

def get_change_request_outcome_manager_email_template(
    manager_name: str,
    employee_name: str,
    application_id: int,
    status: str,
    outcome_reason: str,
    current_time: datetime,
    original_details: str,
    updated_details: str
) -> str:
    return f"""
Dear {manager_name},

The change request for {employee_name}'s Application ID: {application_id} has been {status}.

Status: {status.capitalize()}
Reason: {outcome_reason}
Decision Time: {current_time}

Employee: {employee_name}
Application ID: {application_id}

Updated Application Details:
----------------------------
{updated_details}

Original Application Details:
----------------------------
{original_details}

Best regards,
HR Department
"""
def get_event_withdrawn_manager_email_subject(event_id: int, application_id: int) -> str:
    return f"Event Withdrawn - Event ID: {event_id} (Application ID: {application_id})"

def get_event_withdrawn_employee_email_subject(event_id: int, application_id: int) -> str:
    return f"Event Withdrawal Confirmation - Event ID: {event_id}"

def get_event_withdrawn_manager_email_template(manager_name: str, employee_name: str, event_id: int, application_id: int, requested_date: date, location: str, withdrawn_on: datetime, withdrawn_by: str) -> str:
    return f"""
Dear {manager_name},

This is to inform you that an event associated with an application has been withdrawn.

Event Details:
--------------------
Employee Name: {employee_name}
Event ID: {event_id}
Application ID: {application_id}
Requested Date: {requested_date}
Location: {location}
Withdrawn On: {withdrawn_on}
Withdrawn By: {withdrawn_by}

If you have any questions regarding this withdrawal, please contact the HR department.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """

def get_event_withdrawn_employee_email_template(employee_name: str, event_id: int, application_id: int, requested_date: date, location: str, withdrawn_on: datetime, withdrawn_by: str) -> str:
    return f"""
Dear {employee_name},

This email confirms that your event has been withdrawn.

Event Details:
--------------------
Event ID: {event_id}
Application ID: {application_id}
Requested Date: {requested_date}
Location: {location}
Withdrawn On: {withdrawn_on}
Withdrawn By: {withdrawn_by}

If you need to submit a new event or have any questions, please contact the HR department.

Thank you for using our application system.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """
def get_event_cancellation_manager_email_template(manager_name: str, employee_name: str, employee_id: int, event_id: int, requested_date: date, location: str, cancellation_reason: str, current_time: datetime) -> str:
    return f"""
Dear {manager_name},

An event cancellation request has been submitted by {employee_name}.

Event Details:
--------------------
Employee Name: {employee_name}
Employee ID: {employee_id}
Event ID: {event_id}
Requested Date: {requested_date}
Location: {location}
Cancellation Reason: {cancellation_reason if cancellation_reason else "No reason provided"}
Submission Date and Time: {current_time}

Please review this cancellation request and take appropriate action. If you have any questions, please contact the HR department.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """

def get_event_cancellation_employee_email_template(employee_name: str, event_id: int, requested_date: date, location: str, cancellation_reason: str, current_time: datetime) -> str:
    return f"""
Dear {employee_name},

Your event cancellation request has been submitted successfully.

Event Details:
--------------------
Event ID: {event_id}
Requested Date: {requested_date}
Location: {location}
Cancellation Reason: {cancellation_reason if cancellation_reason else "No reason provided"}
Submission Date and Time: {current_time}

Your request will be reviewed by your manager. You will be notified of any updates.

If you have any questions, please contact the HR department.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """
def get_event_cancellation_manager_email_subject(event_id: int, employee_name: str) -> str:
    return f"Event Cancellation Request - Event ID: {event_id} - {employee_name}"

def get_event_cancellation_employee_email_subject(event_id: int) -> str:
    return f"Event Cancellation Submitted - Event ID: {event_id}"

def get_cancel_one_request_outcome_manager_email_template(manager_name: str, employee_name: str, event_id: int, outcome: str, current_time: datetime) -> str:
    outcome_message = "approved" if outcome == "approved" else "rejected"
    return f"""
Dear {manager_name},

The cancellation request for Event ID: {event_id} has been {outcome_message}.

Event Details:
--------------------
Employee Name: {employee_name}
Event ID: {event_id}
Outcome: {outcome_message.capitalize()}
Date and Time: {current_time}

Please contact the HR department if you have any questions.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """

def get_cancel_one_request_outcome_employee_email_template(employee_name: str, event_id: int, outcome: str, current_time: datetime) -> str:
    outcome_message = "approved" if outcome == "approved" else "rejected"
    return f"""
Dear {employee_name},

Your cancellation request for Event ID: {event_id} has been {outcome_message}.

Event Details:
--------------------
Event ID: {event_id}
Outcome: {outcome_message.capitalize()}
Date and Time: {current_time}

Please contact your manager if you have any questions.

Best regards,
HR Department

This is an automated message. Please do not reply directly to this email.
    """
def get_cancel_one_request_outcome_manager_email_subject(event_id: int, outcome: str) -> str:
    return f"Cancellation Request {outcome.capitalize()} - Event ID: {event_id}"

def get_cancel_one_request_outcome_employee_email_subject(event_id: int, outcome: str) -> str:
    return f"Cancellation Request {outcome.capitalize()} - Event ID: {event_id}"