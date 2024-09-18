from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .Environment import get_environment_variables

# Load environment variables
env = get_environment_variables()

# Construct the DATABASE_URL
DATABASE_URL = (
    f"{env.DATABASE_DIALECT}://{env.POSTGRES_USER}:{env.POSTGRES_PASSWORD}"
    f"@{env.DATABASE_HOSTNAME}:{env.POSTGRES_PORT}/{env.POSTGRES_DB}"
)

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
