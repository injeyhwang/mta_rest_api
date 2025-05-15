from typing import List, Tuple

from sqlmodel import Session, select

from app.db.models.gtfs import Stop, StopTime, Trip


class StopTimeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_by_stop_id(
            self,
            stop_id: str,
            route_id: str | None,
            service_id: str | None,
            arrival_time: str | None,
            departure_time: str | None) -> List[Tuple[StopTime, Trip]]:
        """
        Get stop times with trip info associated with a stop ID

        Args:
            stop_id (str): Stop ID to match
            route_id (str | None): Route ID to filter trips by
            service_id (str | None): Service ID to filter trips by
            arrival_time (str | None): Arrival time to filter stop times by
            departure_time (str | None): Departure time to filter stop times by

        Returns:
            List[Tuple[StopTime, Trip]]: Found stop times with associated trip
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

    def get_all_by_trip_id(
            self,
            trip_id: str,
            arrival_time: str | None,
            departure_time: str | None) -> List[Tuple[StopTime, Stop]]:
        """
        Get stop times with stop info associated with a trip ID

        Args:
            trip_id (str): Trip ID to match
            arrival_time (str | None): Arrival time to filter stop times by
            departure_time (str | None): Departure time to filter stop times by

        Returns:
            List[Tuple[StopTime, Stop]]: Found stop times with associated stop
        """
        query = (select(StopTime, Stop)
                 .join(Stop, StopTime.stop_id == Stop.stop_id)
                 .where(StopTime.trip_id == trip_id))

        if arrival_time is not None:
            query = query.where(StopTime.arrival_time >= arrival_time)

        if departure_time is not None:
            query = query.where(StopTime.departure_time <= departure_time)

        # TODO: add sort_by filter
        query = query.order_by(StopTime.arrival_time)
        return self.session.exec(query).all()
