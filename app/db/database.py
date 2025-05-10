# SQLModel and app.db.models is imported because Python executes all the code
# creating the classes inheriting from SQLModel and registering them in the
# SQLModel.metadata.
#
# https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata-order-matters

from sqlmodel import SQLModel, create_engine  # noqa: F401

import app.db.models  # noqa: F401
from app.config import settings as s
from app.utils.logger import logger

DATABASE_URL = f"postgresql://{s.db_user}:{s.db_password}@{s.db_host}:{
    s.db_port}/{s.db_name}"


engine = create_engine(
    DATABASE_URL,
    # set to True for SQL query logging (development only)
    echo=False,
    # verify connection is still alive before using from pool
    pool_pre_ping=True,
    # recycle connections after one hour to avoid stale connections
    pool_recycle=3600,)


def get_db_engine():
    """
    Return the database engine instance.

    Returns:
        Engine: A SQLModel engine that handles the connection and
        communication with the database.
    """
    database_name = DATABASE_URL.split("/")[-1]
    logger.info(f"Using database: '{database_name}'")
    return engine
