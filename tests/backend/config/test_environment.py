import os
import pytest
from unittest.mock import patch, mock_open
from backend.config.Environment import get_env_filename, EnvironmentSettings, get_environment_variables

@pytest.fixture(autouse=True)
def clear_lru_cache():
    get_env_filename.cache_clear()
    get_environment_variables.cache_clear()

@pytest.fixture
def mock_env_test():
    return {"ENV": "test"}

@pytest.fixture
def mock_env_empty():
    return {}

def test_get_env_filename(mock_env_test, mock_env_empty):
    # Test with ENV set to "test"
    with patch.dict(os.environ, mock_env_test):
        print(f"ENV after patch: {os.environ.get('ENV')}")
        result = get_env_filename()
        print(f"Result with ENV='test': {result}")
        print(f"os.environ['ENV']: {os.environ.get('ENV')}")
        assert result.endswith('.env.test'), f"Expected filename ending with '.env.test', but got: {result}"

    # Clear the cache again before the second test
    get_env_filename.cache_clear()

    # Test without ENV set
    with patch.dict(os.environ, mock_env_empty, clear=True):
        print(f"ENV after patch: {os.environ.get('ENV')}")
        result = get_env_filename()
        print(f"Result without ENV set: {result}")
        print(f"os.environ['ENV']: {os.environ.get('ENV')}")
        assert result.endswith('.env'), f"Expected filename ending with '.env', but got: {result}"

@pytest.fixture
def mock_env_content():
    return """
    CURRENT_ENV=TEST
    DATABASE_DIALECT=postgresql
    DATABASE_HOSTNAME=localhost
    POSTGRES_DB=testdb
    POSTGRES_PASSWORD=testpass
    POSTGRES_PORT=5432
    POSTGRES_USER=testuser
    DEBUG_MODE=true
    SMTP_SERVER=smtp.test.com
    SMTP_PORT=587
    SENDER_EMAIL=test@example.com
    SENDER_PASSWORD=testpassword
    PRODUCTION_DB_USER=produser
    PRODUCTION_DB_PASSWORD=prodpass
    PRODUCTION_DB_HOSTNAME=prodhost
    PRODUCTION_DB_PORT=5433
    PRODUCTION_DB_NAME=proddb
    """
#
# @patch('backend.config.Environment.get_env_filename')
# def test_environment_settings(mock_get_env_filename, mock_env_content):
#     mock_get_env_filename.return_value = '.env.test'
#     with patch('builtins.open', mock_open(read_data=mock_env_content)):
#         settings = EnvironmentSettings()
#         assert settings.CURRENT_ENV == 'TEST'
#         assert settings.DATABASE_DIALECT == 'postgresql'
#         assert settings.DATABASE_HOSTNAME == 'localhost'
#         assert settings.POSTGRES_DB == 'testdb'
#         assert settings.POSTGRES_PASSWORD == 'testpass'
#         assert settings.POSTGRES_PORT == 5432
#         assert settings.POSTGRES_USER == 'testuser'
#         assert settings.DEBUG_MODE == True
#         assert settings.SMTP_SERVER == 'smtp.test.com'
#         assert settings.SMTP_PORT == 587
#         assert settings.SENDER_EMAIL == 'test@example.com'
#         assert settings.SENDER_PASSWORD == 'testpassword'
#         assert settings.PRODUCTION_DB_USER == 'produser'
#         assert settings.PRODUCTION_DB_PASSWORD == 'prodpass'
#         assert settings.PRODUCTION_DB_HOSTNAME == 'prodhost'
#         assert settings.PRODUCTION_DB_PORT == 5433
#         assert settings.PRODUCTION_DB_NAME == 'proddb'

@pytest.fixture
def mock_environment_settings():
    class MockSettings:
        DATABASE_DIALECT = 'postgresql'
        DATABASE_HOSTNAME = 'localhost'
    return MockSettings()

@patch('backend.config.Environment.EnvironmentSettings')
def test_get_environment_variables(mock_settings, mock_environment_settings):
    mock_settings.return_value = mock_environment_settings
    env_vars = get_environment_variables()
    assert env_vars.DATABASE_DIALECT == 'postgresql'
    assert env_vars.DATABASE_HOSTNAME == 'localhost'