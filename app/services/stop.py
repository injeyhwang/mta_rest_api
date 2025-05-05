from sqlmodel import Session

from app.db.models import Stop
from app.db.repositories.stop import StopRepository
from app.db.repositories.stop_time import StopTimeRepository
from app.schemas.pagination import PaginatedResponse
from app.schemas.stop import StopResponse, StopDetailedResponse, StopTimeResponse
from app.schemas.trip import DirectionID, ServiceID, TripResponse


class StopService:
    def __init__(self, session: Session):
        self.session = session
        self.stop_repo = StopRepository(session)
        self.stop_time_repo = StopTimeRepository(session)

    def get_detailed_by_id(self, stop_id: str) -> StopResponse:
        stop = self.stop_repo.get_by_id(stop_id)
        if not stop:
            raise ValueError(f"Stop with ID '{stop_id}' not found")

        return self._detailed_responsify(stop)

    def get_all(self, offset: int, limit: int) -> PaginatedResponse[StopResponse]:
        stops, total = self.stop_repo.get_all(offset, limit)
        results = [self._responsify(stop) for stop in stops]
        return PaginatedResponse[StopResponse](total=total, offset=offset, limit=limit, results=results)

    def _responsify(self, stop: Stop) -> StopResponse:
        return StopResponse(id=stop.stop_id,
                            name=stop.stop_name,
                            latitude=stop.stop_lat,
                            longitude=stop.stop_lon)

    def _detailed_responsify(self, stop: Stop) -> StopDetailedResponse:
        stop_times = self.stop_time_repo.get_all_by_stop_id(stop_id=stop.stop_id)

        results = []
        for stop_time, trip in stop_times:
            trip_res = TripResponse(id=trip.trip_id,
                                    headsign=trip.trip_headsign,
                                    route_id=trip.route_id,
                                    service_id=ServiceID(trip.service_id),
                                    direction_id=DirectionID(trip.direction_id))

            stop_time_res = StopTimeResponse(trip=trip_res,
                                             stop_sequence=stop_time.stop_sequence,
                                             arrival_time=stop_time.arrival_time,
                                             departure_time=stop_time.departure_time)
            results.append(stop_time_res)

        return StopDetailedResponse(id=stop.stop_id,
                                    name=stop.stop_name,
                                    latitude=stop.stop_lat,
                                    longitude=stop.stop_lon,
                                    stop_times=results)
