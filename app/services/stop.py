from sqlmodel import Session
from typing import List

from app.db.models import Stop
from app.db.repositories.stop import StopRepository
from app.schemas.stop import StopResponse


class StopService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = StopRepository(session)

    def get_by_id(self, stop_id: str) -> StopResponse:
        stop = self.repository.get_by_id(stop_id)
        if not stop:
            raise ValueError(f"Stop with ID '{stop_id}' not found")

        return self._responsify(stop)

    def get_all(self) -> List[StopResponse]:
        stops = self.repository.get_all()
        results = [self._responsify(stop) for stop in stops]
        return results

    def _responsify(self, stop: Stop) -> StopResponse:
        return StopResponse(id=stop.stop_id,
                            name=stop.stop_name,
                            latitude=stop.stop_lat,
                            longitude=stop.stop_lon,
                            station=stop.parent_station)
