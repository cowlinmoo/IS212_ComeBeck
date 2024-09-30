from functools import lru_cache
import os
from pydantic_settings import BaseSettings


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    env_filename = f".env.{runtime_env}" if runtime_env else ".env"
    # Go two levels up from the current directory
    base_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', '..'))
    env_file_path = os.path.join(base_dir, env_filename)
    print(f"Trying to load environment variables from: {env_file_path}")
    return env_file_path

class EnvironmentSettings(BaseSettings):
    CURRENT_ENV: str = 'DEV' # Default to 'DEV' if not provided
    PRODUCTION_DB_USER: str = None # Optional
    PRODUCTION_DB_PASSWORD: str = None # Optional
    PRODUCTION_DB_HOSTNAME: str = None # Optional
    PRODUCTION_DB_PORT: int = None # Optional
    PRODUCTION_DB_NAME: str = None # Optional
    DATABASE_DIALECT: str
    DATABASE_HOSTNAME: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    DEBUG_MODE: bool
    SMTP_SERVER: str
    SMTP_PORT: int
    SENDER_EMAIL: str
    SENDER_PASSWORD: str

    class Config:
        extra = 'allow'
        env_file = get_env_filename()
        env_file_encoding = "utf-8"


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()
