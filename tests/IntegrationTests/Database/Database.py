import pytest
from sqlalchemy import inspect, create_engine
from sqlalchemy.orm import sessionmaker

# Assuming your database URL for the test database is in the format:
DATABASE_URL = "postgresql://admin:admin@localhost/spm"

# Initialize the database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# List of expected tables and columns based on your models
expected_tables = {
    "application": [
        "application_id", "reason", "description", "created_on", "last_updated_on",
        "status", "application_state", "staff_id", "approver_id", "outcome_reason",
        "original_application_id", "recurring", "recurrence_type", "end_date"
    ],
    "departments": [
        "department_id", "name", "description", "director_id"
    ],
    "employees": [
        "staff_id", "staff_fname", "staff_lname", "position", "department_id",
        "team_id", "country", "email", "reporting_manager", "role", "password"
    ],
    "event": [
        "event_id", "requested_date", "application_hour", "location",
        "application_id", "original_event_id"
    ],
    "teams": [
        "team_id", "name", "description", "manager_id", "department_id",
        "parent_team_id"
    ]
}


# Test to verify database tables and columns
@pytest.mark.integration
def test_database_schema():
    inspector = inspect(engine)

    # Check each table in the expected tables
    for table_name, expected_columns in expected_tables.items():
        # Verify table exists
        assert inspector.has_table(table_name), f"Table '{table_name}' is missing."

        # Get actual columns for the table
        actual_columns = [col['name'] for col in inspector.get_columns(table_name)]

        # Verify all expected columns are in the actual columns
        for column in expected_columns:
            assert column in actual_columns, f"Column '{column}' is missing in table '{table_name}'."

    print("All tables and columns verified successfully.")

