from sqlmodel import func, Session, select
from typing import List, Tuple

from app.db.models import Stop


class StopRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, stop_id: str) -> Stop | None:
        """
        Get single stop by ID.

        Args:
            stop_id (str): Stop ID to match.

        Returns:
            Stop | None: Found stop, None otherwise.
        """
        return self.session.get(Stop, stop_id)

    def get_all(self, offset: int = 0, limit: int = 100) -> Tuple[List[Stop], int]:
        """
        Get all subway stops. This method will only return stops and will omit stations.

        Stations are stops that contain multiple stops with directions.

        E.g. stop_id: 101 has child stops: 101S and 101N

        Args:
            offset (int): Number of items to skip
            limit (int): Maximum number of items to return

        Returns:
            Tuple of (stops: List[Stop], total_items: int)
        """
        query = select(Stop).where(Stop.parent_station != None)

        # get total item count on filtered trips
        count_query = select(func.count()).select_from(query.subquery())
        total_items = self.session.exec(count_query).one()

        # apply pagination
        query = query.offset(offset).limit(limit)

        stops = self.session.exec(query).all()
        return stops, total_items
