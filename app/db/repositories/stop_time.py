from sqlmodel import Session, select
from typing import List

from app.db.models import StopTime, Trip


class StopTimeRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_by_stop_id(self, stop_id: str) -> List[StopTime]:
        """
        Get single stop time by stop ID.

        Args:
            stop_id (str): Stop ID to match.

        Returns:
            List[StopTime]: Found stop times.
        """
        query = (select(StopTime, Trip)
                    .join(Trip, StopTime.trip_id == Trip.trip_id)
                    .where(StopTime.stop_id == stop_id))
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
