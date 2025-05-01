from sqlmodel import Session, select
from typing import List

from app.db.models import Route


class RouteRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, route_id: str) -> Route | None:
        """
        Get single route by ID.

        Args:
            route_id (str): Route ID to match.

        Returns:
            Route | None: Found route, None otherwise.
        """
        return self.session.get(Route, route_id)

    def get_all(self) -> List[Route]:
        """
        Get all routes.

        Returns:
            List[Route]: List of all available routes.
        """
        query = select(Route)
        return self.session.exec(query).all()
