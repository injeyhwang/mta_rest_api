import os

from sqlmodel import create_engine, SQLModel
from app.utils.logger import logger


def get_db_engine():
    """
    Create and return a database engine based on the DATABASE_URL environment variable.
    """
    DATABASE_URL = os.environ.get("DATABASE_URL")
    logger.info(f"Connecting to database: '{DATABASE_URL}'")
    engine = create_engine(DATABASE_URL)
    return engine


def create_db_tables(engine):
    """
    Create all database tables defined in SQLModel metadata if they don't exist.
    """
    logger.info("Creating database tables if they don't exist")
    SQLModel.metadata.create_all(engine)


def init_database():
    """
    Initialize the database by creating the engine and all tables.
    """
    engine = get_db_engine()
    create_db_tables(engine)
    logger.info("Database initialization completed")
    return engine


if __name__ == "__main__":
    init_database()
