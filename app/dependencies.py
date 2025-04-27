from sqlmodel import Session

from app.db.database import get_db_session as db_session
from app.services.mta_realtime import MTAServiceRT


mta_rt_service = MTAServiceRT()


def get_db_session() -> Session:
    """
    A singleton for the database session instance. The session object will be dependency
    injected into database dependent endpoints.
    """
    return db_session


def get_mta_rt_service() -> MTAServiceRT:
    """
    A singleton for MTAServiceRT instance. The MTAServiceRT object will be dependency injected into
    feed API routes.
    """
    return mta_rt_service
