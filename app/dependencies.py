from sqlmodel import Session

from app.db.database import get_db_session as db_session
from app.services.realtime import MTAService


mta_service = MTAService()


def get_db_session() -> Session:
    """
    A singleton for the database session instance. The session object will be dependency
    injected into database dependent endpoints.
    """
    return db_session


def get_realtime_service() -> MTAService:
    """
    A singleton for MTAService instance. The MTAService object will be dependency injected into feed
    API routes.
    """
    return mta_service
