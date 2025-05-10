from typing import List

from sqlmodel import Session, select

from app.db.models.stop import Stop


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

    def get_all(self, direction_id: int | None) -> List[Stop]:
        """
        Get all subway stops. This method will only return stops and will omit
        stations.

        Stations are stops that contain multiple stops with directions.

        E.g. stop_id: 101 has child stops: 101S and 101N

        Args:
            direction_id (int | None): Direction to filter by. 1 maps to N,
                                       0 maps to S

        Returns:
            List[Stop]: List of subway stops
        """
        query = select(Stop).where(Stop.parent_station is not None)

        if direction_id is not None:
            if direction_id == 1:
                query = query.where(Stop.stop_id.like("%N"))
            else:
                query = query.where(Stop.stop_id.like("%S"))

        return self.session.exec(query).all()
