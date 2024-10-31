import pytest
from pydantic import ValidationError
from backend.schemas.TokenSchema import Token  # Make sure to import the Token class from the correct module

@pytest.mark.unit
def test_token_model_creation():
    # Arrange: Create valid data for the Token model
    valid_data = {
        "email": "test@gmail.com",
        "role": "HR",
        "access_token": "access_token",
        "token_type": "bearer",
        "staff_id": 1
    }

    # Act: Create an instance of the Token model
    token_instance = Token(**valid_data)

    # Assert: Verify that the attributes are set correctly
    assert token_instance.email == valid_data["email"]
    assert token_instance.role == valid_data["role"]
    assert token_instance.access_token == valid_data["access_token"]
    assert token_instance.token_type == valid_data["token_type"]
    assert token_instance.staff_id == valid_data["staff_id"]

@pytest.mark.unit
def test_token_model_missing_required_fields():
    # Arrange: Create data missing required fields
    incomplete_data = {
        "role": "HR",
        "access_token": "access_token",
        "token_type": "bearer",
        "staff_id": 1
    }

    # Act & Assert: Verify that creating the Token model raises a ValidationError
    with pytest.raises(ValidationError) as exc_info:
        Token(**incomplete_data)

    assert "1 validation error for Token" in str(exc_info.value)
    assert "email" in str(exc_info.value)
    assert "Field required" in str(exc_info.value)
