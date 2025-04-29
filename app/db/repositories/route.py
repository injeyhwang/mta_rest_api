from sqlmodel import Session, select
from typing import List

from app.db.models import Route as RouteTable, Trip as TripTable, StopTime as StopTimeTable
from app.schemas.base import Route


class RouteRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, route_id: str) -> Route | None:
        """
        Get a single route by ID.

        Args:
            route_id (str): Route ID to match.

        Returns:
            Route | None: Found route, None otherwise.
        """
        return self.session.get(RouteTable, route_id)

    def get_all(self) -> List[Route]:
        """
        Get all routes.

        Returns:
            List[Route]: List of available routes.
        """
        statement = select(RouteTable)
        return self.session.exec(statement).all()

    def get_routes_serving_stop(self, stop_id: str) -> List[Route]:
        """
        Get routes that serve a particular stop

        Args:
            stop_id (str): Stop ID to get routes for.
            offset (int, optional): Number of items skipped.
            limit (int, optional): Maximum number of items per page.

        Returns:
            List[Route]: List of routes serving a given stop.
        """
        statement = (
            select(RouteTable)
            .join(TripTable, Route.route_id == TripTable.route_id)
            .join(StopTimeTable, TripTable.trip_id == StopTimeTable.trip_id)
            .where(StopTimeTable.stop_id == stop_id)
            .distinct()
        )
        return self.session.exec(statement).all()
