# SQLModel is imported from app.db.database because Python executes all the code creating the classes
# inheriting from SQLModel and registering them in the SQLModel.metadata.
#
# https://sqlmodel.tiangolo.com/tutorial/create-db-and-table/#sqlmodel-metadata-order-matters

from app.db.database import get_db_engine, SQLModel
from app.db.scripts.init_db import create_db_tables
from app.utils.logger import logger


def drop_all_tables(engine):
    """
    Drop all tables defined in SQLModel metadata.
    """
    try:
        logger.info(f"Dropping all database tables")
        SQLModel.metadata.drop_all(engine)
        logger.info("All tables dropped successfully")
    except Exception as e:
        logger.exception(f"Error dropping tables: {e}")
        raise


def reset_database():
    """
    Reset the database by dropping all tables and then recreating them.
    """
    try:
        engine = get_db_engine()
        drop_all_tables(engine)
        create_db_tables(engine)
        logger.info("Database reset completed")
    except Exception as e:
        logger.exception(f"Database reset failed: {e}")
        raise
    finally:
        if engine:
            logger.info("Disposing database engine")
            engine.dispose()
            logger.info("Database connections closed")


if __name__ == "__main__":
    reset_database()
