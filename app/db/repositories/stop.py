from sqlmodel import Session, select
from typing import List

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

    def get_all(self) -> List[Stop]:
        """
        Get all subway stops. This method will only return stops and will omit stations.

        Stations are stops that contain multiple stops with directions.

        E.g. stop_id: 101 has child stops: 101S and 101N

        Args:
            offset (int): Number of items to skip
            limit (int): Maximum number of items to return

        Returns:
            List[Stop]: List of subway stops
        """
        query = select(Stop).where(Stop.parent_station != None)
        return self.session.exec(query).all()
