import os
from sqlmodel import SQLModel, create_engine, Session

# SQLModel and app.db.models is imported because Python executes all the code creating the classes
# inheriting from SQLModel and registering them in the SQLModel.metadata.
#
# https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata-order-matters
import app.db.models
from app.utils.logger import logger


DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(
    DATABASE_URL,
    echo=False,         # set to True for SQL query logging (development only)
    pool_pre_ping=True, # verify connection is still alive before using from pool
    pool_recycle=3600,  # recycle connections after one hour to avoid stale connections
)

def get_db_engine():
    """
    Return the database engine instance.

    Returns:
        Engine: A SQLModel engine that handles the connection and communication with the database.
    """
    database_name = DATABASE_URL.split("/")[-1]
    logger.info(f"Using database: '{database_name}'")
    return engine


def get_session():
    """
    Creates a new database session and closes it after use. This function is designed to be used
    as a FastAPI dependency.

    Yields:
        Session: A SQLModel session connected to the database.
    """
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
