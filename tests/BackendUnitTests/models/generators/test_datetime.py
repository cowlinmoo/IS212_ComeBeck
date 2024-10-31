import pytest
from freezegun import freeze_time
from datetime import datetime, date
import pytz
from backend.models.generators import get_current_datetime_sgt, get_current_date  # Replace 'your_module' with the actual module name


@pytest.fixture
def mock_singapore_time():
    # This fixture sets a fixed time in UTC
    return datetime(2023, 6, 15, 6, 30, 0, tzinfo=pytz.UTC)

@pytest.mark.unit
def test_get_current_datetime_sgt(mock_singapore_time):
    with freeze_time(mock_singapore_time):
        result = get_current_datetime_sgt()

        assert isinstance(result, datetime)
        assert result.tzinfo.zone == 'Asia/Singapore'
        assert result.year == 2023
        assert result.month == 6
        assert result.day == 15
        assert result.hour == 14  # 6 UTC is 14 in Singapore (SGT is UTC+8)
        assert result.minute == 30
        assert result.second == 0

@pytest.mark.unit
def test_get_current_date(mock_singapore_time):
    with freeze_time(mock_singapore_time):
        result = get_current_date()

        assert isinstance(result, date)
        assert result.year == 2023
        assert result.month == 6
        assert result.day == 15

@pytest.mark.unit
def test_timezone_difference():
    # This test is now redundant with the main test, but we'll keep it for clarity
    utc_time = datetime(2023, 6, 15, 6, 30, 0, tzinfo=pytz.UTC)
    with freeze_time(utc_time):
        result = get_current_datetime_sgt()

        assert result.hour == 14  # 6 UTC should be 14 in Singapore (SGT is UTC+8)