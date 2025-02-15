import pytest
from unittest.mock import patch, MagicMock, mock_open

from sqlalchemy import create_engine, text
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, scoped_session
import importlib


# Mock Environment class
class MockEnvironment:
    def __init__(self, env_dict):
        for key, value in env_dict.items():
            setattr(self, key, value)


@pytest.fixture
def mock_env():
    return {
        'CURRENT_ENV': 'DEV',
        'DATABASE_DIALECT': 'postgresql',
        'POSTGRES_USER': 'test_user',
        'POSTGRES_PASSWORD': 'test_password',
        'DATABASE_HOSTNAME': 'localhost',
        'POSTGRES_PORT': '5432',
        'POSTGRES_DB': 'test_db',
        'DEBUG_MODE': False,  # Changed to boolean
        'PRODUCTION_DB_USER': None,
        'PRODUCTION_DB_PASSWORD': None,
        'PRODUCTION_DB_HOSTNAME': None,
        'PRODUCTION_DB_PORT': None,
        'PRODUCTION_DB_NAME': None
    }


@pytest.fixture
def mock_env_prod():
    return {
        'CURRENT_ENV': 'PROD',
        'DATABASE_DIALECT': 'postgresql',
        'PRODUCTION_DB_USER': 'prod_user',
        'PRODUCTION_DB_PASSWORD': 'prod_password',
        'PRODUCTION_DB_HOSTNAME': 'prod_host',
        'PRODUCTION_DB_PORT': '5432',
        'PRODUCTION_DB_NAME': 'prod_db',
        'DEBUG_MODE': False,  # Changed to boolean
        'POSTGRES_USER': None,
        'POSTGRES_PASSWORD': None,
        'DATABASE_HOSTNAME': None,
        'POSTGRES_PORT': None,
        'POSTGRES_DB': None
    }


@pytest.fixture
def mock_get_environment_variables(request):
    env = request.getfixturevalue(request.param)
    with patch('backend.config.Environment.get_environment_variables',
               return_value=MockEnvironment(env)):
        yield env


@pytest.mark.unit
@pytest.mark.parametrize("mock_get_environment_variables", ["mock_env", "mock_env_prod"], indirect=True)
def test_database_url(mock_get_environment_variables):
    # Reload the Database module to use the mocked environment
    import backend.config.Database
    importlib.reload(backend.config.Database)

    env = mock_get_environment_variables
    if env['CURRENT_ENV'] == 'DEV':
        expected_url = (
            f"postgresql://{env['POSTGRES_USER']}:{env['POSTGRES_PASSWORD']}"
            f"@{env['DATABASE_HOSTNAME']}:{env['POSTGRES_PORT']}/{env['POSTGRES_DB']}"
        )
    else:
        expected_url = (
            f"postgresql://{env['PRODUCTION_DB_USER']}:{env['PRODUCTION_DB_PASSWORD']}"
            f"@{env['PRODUCTION_DB_HOSTNAME']}:{env['PRODUCTION_DB_PORT']}/{env['PRODUCTION_DB_NAME']}"
        )

    assert backend.config.Database.DATABASE_URL == expected_url, f"Actual URL: {backend.config.Database.DATABASE_URL}"


@pytest.mark.unit
@pytest.mark.parametrize("mock_get_environment_variables", ["mock_env"], indirect=True)
def test_engine_creation(mock_get_environment_variables):
    import backend.config.Database
    importlib.reload(backend.config.Database)
    assert isinstance(backend.config.Database.Engine, Engine)


@pytest.mark.unit
@pytest.mark.parametrize("mock_get_environment_variables", ["mock_env"], indirect=True)
def test_session_local_creation(mock_get_environment_variables):
    import backend.config.Database
    importlib.reload(backend.config.Database)
    assert isinstance(backend.config.Database.SessionLocal, sessionmaker().__class__)


@pytest.mark.unit
@pytest.mark.parametrize("mock_get_environment_variables", ["mock_env"], indirect=True)
def test_get_db_connection(mock_get_environment_variables):
    import backend.config.Database
    importlib.reload(backend.config.Database)
    db_generator = backend.config.Database.get_db_connection()
    db = next(db_generator)
    assert isinstance(db, scoped_session)
    try:
        next(db_generator)
    except StopIteration:
        pass  # This is expected


from unittest.mock import patch, MagicMock, ANY
from sqlalchemy.sql import text


@pytest.mark.unit
@pytest.mark.parametrize("mock_get_environment_variables", ["mock_env"], indirect=True)
def test_init_db(mock_get_environment_variables):
    # Mock the file reading
    mock_sql_content = "INSERT INTO departments (department_id, name) VALUES (1, 'Test Department');"
    mock_file = mock_open(read_data=mock_sql_content)

    # Create a mock engine
    mock_engine = MagicMock()
    mock_connection = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_connection

    # Mock the execute results
    mock_execute_result = MagicMock()
    mock_execute_result.scalar.return_value = False  # Simulate no existing data
    mock_connection.execute.return_value = mock_execute_result

    # Mock the entire sqlalchemy module
    with patch('builtins.open', mock_file), \
            patch('os.path.join', return_value='/fake/path/to/init.sql'), \
            patch('sqlalchemy.create_engine', return_value=mock_engine), \
            patch('sqlalchemy.engine.Engine', mock_engine):
        # Reload the Database module to use the mocked environment
        import backend.config.Database
        importlib.reload(backend.config.Database)

        from backend.config.Database import init_db
        init_db()

    # Assert that the connection was used
    mock_engine.connect.assert_called_once()

    # Assert that execute was called twice
    assert mock_connection.execute.call_count == 2

    # Check the first execute call (checking for existing data)
    first_call = mock_connection.execute.call_args_list[0]
    first_sql = str(first_call[0][0])
    assert "SELECT EXISTS (SELECT 1 FROM departments LIMIT 1)" in first_sql

    # Check the second execute call (inserting data)
    second_call = mock_connection.execute.call_args_list[1]
    second_sql = str(second_call[0][0])
    assert second_sql == mock_sql_content

    print("Test passed successfully!")


@pytest.mark.parametrize("data_exists", [True, False])
@pytest.mark.unit
@pytest.mark.parametrize("mock_get_environment_variables", ["mock_env"], indirect=True)
def test_init_db(mock_get_environment_variables, data_exists):
    mock_sql_content = "INSERT INTO departments (department_id, name) VALUES (1, 'Test Department');"
    mock_file = mock_open(read_data=mock_sql_content)

    mock_engine = MagicMock()
    mock_connection = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_connection

    mock_execute_result = MagicMock()
    mock_execute_result.scalar.return_value = data_exists  # Simulate existing or no existing data
    mock_connection.execute.return_value = mock_execute_result

    with patch('builtins.open', mock_file), \
            patch('os.path.join', return_value='/fake/path/to/init.sql'), \
            patch('sqlalchemy.create_engine', return_value=mock_engine), \
            patch('sqlalchemy.engine.Engine', mock_engine), \
            patch('builtins.print') as mock_print:

        import backend.config.Database
        importlib.reload(backend.config.Database)

        from backend.config.Database import init_db
        init_db()

    mock_engine.connect.assert_called_once()

    if data_exists:
        mock_print.assert_called_with("Data already exists in the database, skipping initialization")
        assert mock_connection.execute.call_count == 1  # Only check for existing data
    else:
        mock_print.assert_called_with("Initial data inserted into the database")
        assert mock_connection.execute.call_count == 2  # Check for existing data and insert new data

    print(f"Test passed successfully for data_exists={data_exists}!")