from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .Environment import get_environment_variables

# Load environment variables
env = get_environment_variables()

DATABASE_HOSTNAME = env.DATABASE_HOSTNAME or 'localhost'

# Construct the DATABASE_URL
if env.CURRENT_ENV == 'PROD':
    # Use credentials from env if available, otherwise fall back to environment variables
    production_username = env.PRODUCTION_DB_USER
    production_password = env.PRODUCTION_DB_PASSWORD

    DATABASE_URL = f'postgresql://{production_username}:{production_password}@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres'
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
