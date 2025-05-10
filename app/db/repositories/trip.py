from typing import List, Tuple

from sqlmodel import Session, func, select

from app.db.models.trip import Trip


class TripRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, trip_id: str) -> Trip | None:
        """
        Get single trip by ID.

        Args:
            trip_id (str): Trip ID to match.

        Returns:
            Trip | None: Found trip, None otherwise.
        """
        return self.session.get(Trip, trip_id)

    def get_all(self,
                route_id: str | None,
                service_id: str | None,
                direction_id: int | None,
                offset: int = 0,
                limit: int = 100) -> Tuple[List[Trip], int]:
        """
        Get all paginated trips

        Args:
            route_id (str | None): Filter by route ID
            service_id (str | None): Filter by service ID
            direction_id (int | None): Filter by direction ID
            offset (int): Number of trips to skip
            limit (int): Maximum number of trips to return

        Returns:
            Tuple of (trips: List[Trip], total_items: int)
        """
        query = select(Trip)
        if route_id is not None:
            query = query.where(Trip.route_id == route_id)
        if service_id is not None:
            query = query.where(Trip.service_id == service_id)
        if direction_id is not None:
            query = query.where(Trip.direction_id == direction_id)

        # get total item count on filtered trips
        count_query = select(func.count()).select_from(query.subquery())
        total_items = self.session.exec(count_query).one()

        # apply pagination
        query = query.offset(offset).limit(limit)

        trips = self.session.exec(query).all()
        return trips, total_items
