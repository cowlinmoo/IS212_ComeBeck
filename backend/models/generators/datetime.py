from datetime import datetime, date
import pytz

def get_current_datetime_sgt() -> datetime:
    """
    Returns the current datetime in Singapore timezone.
    """
    sgt_timezone = pytz.timezone('Asia/Singapore')
    return datetime.now(sgt_timezone)

def get_current_date() -> date:
    """
    Returns the current date in Singapore timezone.
    """
    return get_current_datetime_sgt().date()