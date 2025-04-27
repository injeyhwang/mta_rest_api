# SQLModel is imported from app.db.database because Python executes all the code creating the classes
# inheriting from SQLModel and registering them in the SQLModel.metadata.
#
# https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata-order-matters

from app.db.database import get_db_engine, SQLModel
from app.utils.logger import logger


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
    try:
        engine = get_db_engine()
        create_db_tables(engine)
        logger.info("Database initialization completed")
    except Exception as e:
        logger.exception(f"Database initialization failed: {e}")
        raise
    finally:
        if engine:
            logger.info("Disposing database engine")
            engine.dispose()
            logger.info("Database connections closed")


if __name__ == "__main__":
    init_database()
