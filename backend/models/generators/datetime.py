from datetime import datetime
import pytz

def get_current_datetime_sgt() -> datetime:
    """
    Returns the current datetime in Singapore timezone.
    """
    sgt_timezone = pytz.timezone('Asia/Singapore')
    return datetime.now(sgt_timezone)
