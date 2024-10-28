import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from .Environment import get_environment_variables

# Load environment variables
env = get_environment_variables()

DATABASE_HOSTNAME = env.DATABASE_HOSTNAME or 'localhost'

# Construct the DATABASE_URL
if env.CURRENT_ENV == 'PROD':
    # Use credentials from env if available,
    # otherwise fall back to environment variables
    production_username = env.PRODUCTION_DB_USER
    production_password = env.PRODUCTION_DB_PASSWORD
    production_hostname = env.PRODUCTION_DB_HOSTNAME
    production_port = env.PRODUCTION_DB_PORT
    production_db = env.PRODUCTION_DB_NAME

    DATABASE_URL = (f"postgresql://{production_username}:{production_password}"
                    f"@{production_hostname}:{production_port}/{production_db}")

elif env.CURRENT_ENV == 'TEST':
    DATABASE_URL = \
        "postgresql://test_user:test_password@spm_database_test:5432/test_spm"

else:  # Assuming 'development' or other environments
    DATABASE_URL = (
        f"{env.DATABASE_DIALECT}://{env.POSTGRES_USER}:{env.POSTGRES_PASSWORD}"
        f"@{env.DATABASE_HOSTNAME}:{env.POSTGRES_PORT}/{env.POSTGRES_DB}"
    )
print(f"DATABASE_URL: {DATABASE_URL}")
# Create the SQLAlchemy engine
Engine = create_engine(
    DATABASE_URL, echo=env.DEBUG_MODE, future=True
)

# Create a configured "Session" class
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=Engine
)


def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()


def init_db():
    init_sql_path = (
        os.path.join(os.path.dirname(__file__), '..', '..', 'postgres', 'init.sql'))

    with Engine.connect() as connection:
        # Explicitly start a transaction for the entire operation
        with connection.begin():
            # Check if data already exists in the departments table
            data_exists = connection.execute(text(
                "SELECT EXISTS (SELECT 1 FROM departments LIMIT 1)"
            )).scalar()

            if not data_exists:
                with open(init_sql_path, 'r') as file:
                    sql_script = file.read()

                # Execute the script within the same transaction
                connection.execute(text(sql_script))
                print("Initial data inserted into the database")
            else:
                print("Data already exists in the database, skipping initialization")
