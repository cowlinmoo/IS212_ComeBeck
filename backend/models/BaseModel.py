from sqlalchemy.ext.declarative import declarative_base
from ..config.Database import Engine

# Base Entity Model Schema
EntityMeta = declarative_base()


def create_database():
    print("Initializing database...")
    print(EntityMeta.metadata.tables)  # Print the reflected tables
    EntityMeta.metadata.create_all(bind=Engine)
    print("Database initialization complete.")
