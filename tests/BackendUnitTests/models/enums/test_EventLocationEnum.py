import pytest
from backend.models.enums.EventLocationEnum import EventLocationEnum

def test_event_location_enum_values():
    """Test that the enum has the correct values for WFH and WFO."""
    assert EventLocationEnum.WFH.value == "wfh", "WFH enum value does not match expected 'wfh'"
    assert EventLocationEnum.WFO.value == "wfo", "WFO enum value does not match expected 'wfo'"

def test_event_location_enum_members():
    """Test that the enum has the correct members."""
    assert EventLocationEnum["WFH"] == EventLocationEnum.WFH, "WFH enum member not accessible as expected"
    assert EventLocationEnum["WFO"] == EventLocationEnum.WFO, "WFO enum member not accessible as expected"

def test_event_location_enum_types():
    """Test that the enum members are instances of EventLocationEnum."""
    assert isinstance(EventLocationEnum.WFH, EventLocationEnum), "WFH is not an instance of EventLocationEnum"
    assert isinstance(EventLocationEnum.WFO, EventLocationEnum), "WFO is not an instance of EventLocationEnum"
