from datetime import datetime, date
from typing import Optional, List, Union, Dict

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