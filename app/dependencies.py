from sqlmodel import Session
from fastapi import Depends
from typing import Any, Generator

from app.db.database import engine
from app.services.realtime import MTAService
from app.services.route import RouteService
from app.services.trip import TripService


mta_service = MTAService()


def get_db_session() -> Generator[Session, Any, None]:
    """
    Creates a new database session and closes it after use. The session object will be dependency
    injected into database dependent endpoints.

    Yields:
        Session: A SQLModel session connected to the database.
    """
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()


def get_route_service(session: Session = Depends(get_db_session)) -> RouteService:
    """
    A getter function for the RouteService instance. The RouteService object will be dependency
    injected into the routes API endpoints.

    Returns:
        RouteService: A service layer for the Route GTFS Static data.
    """
    return RouteService(session)


def get_trip_service(session: Session = Depends(get_db_session)) -> RouteService:
    """
    A getter function for the TripService instance. The TripService object will be dependency
    injected into the trips API endpoints.

    Returns:
        TripService: A service layer for the Trip GTFS Static data.
    """
    return TripService(session)


def get_realtime_service() -> MTAService:
    """
    A getter function for the MTAService instance. The MTAService object will be dependency injected
    into the feeds API endpoints.

    Returns:
        MTAService: A service layer for the MTA GTFS-RT API.
    """
    return mta_service
