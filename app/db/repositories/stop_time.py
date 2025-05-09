from sqlmodel import Session, select
from typing import List

from app.db.models import StopTime, Trip


class StopTimeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_by_stop_id(self,
                           stop_id: str,
                           route_id: str | None,
                           service_id: str | None,
                           arrival_time: str | None,
                           departure_time: str | None) -> List[StopTime]:
        """
        Get single stop time by stop ID.

        Args:
            stop_id (str): Stop ID to match.
            route_id (str | None): Route ID to filter trips by.
            service_id (str | None): Service ID to filter trips by.
            arrival_time (str | None): Arrival time to filter trips by.
            departure_time (str | None): Departure time to filter trips by.

        Returns:
            List[StopTime]: Found stop times.
        """
        query = (select(StopTime, Trip)
                    .join(Trip, StopTime.trip_id == Trip.trip_id)
                    .where(StopTime.stop_id == stop_id))
        if route_id is not None:
            query = query.where(Trip.route_id == route_id)

        if service_id is not None:
            query = query.where(Trip.service_id == service_id)

        if arrival_time is not None:
            query = query.where(StopTime.arrival_time >= arrival_time)

        if departure_time is not None:
            query = query.where(StopTime.departure_time <= departure_time)

        # TODO: add sort_by filter
        query = query.order_by(StopTime.arrival_time)
        return self.session.exec(query).all()

    def get_all_by_trip_id(self, trip_id: str) -> List[StopTime]:
        """
        Get single stop time by trip ID.

        Args:
            trip_id (str): Trip ID to match.

        Returns:
            List[StopTime]: Found stop times.
        """
        query = select(StopTime).where(StopTime.trip_id == trip_id)
        return self.session.exec(query).all()
