from sqlmodel import Session, select
from typing import List

from app.db.models import Route, Trip, StopTime
from app.schemas.base import RouteResponse


class RouteRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, route_id: str) -> RouteResponse | None:
        """
        Get a single route by ID.

        Args:
            route_id (str): Route ID to match.

        Returns:
            Route | None: Found route, None otherwise.
        """
        return self.session.get(Route, route_id)

    def get_all(self) -> List[RouteResponse]:
        """
        Get all routes.

        Returns:
            List[Route]: List of available routes.
        """
        query = select(Route)
        return self.session.exec(query).all()
