from sqlmodel import Session
from typing import List

from app.db.models import Stop
from app.db.repositories.route import RouteRepository
from app.db.repositories.stop import StopRepository
from app.db.repositories.stop_time import StopTimeRepository
from app.exceptions.base import ResourceNotFoundError, QueryInvalidError
from app.schemas.stop import StopResponse, StopDetailedResponse, StopTimeResponse, StopTimeTrip
from app.schemas.trip import ServiceID
from app.utils.helpers import valid_time_format


class StopService:
    def __init__(self, session: Session):
        self.session = session
        self.route_repo = RouteRepository(session)
        self.stop_repo = StopRepository(session)
        self.stop_time_repo = StopTimeRepository(session)

    def get_detailed_by_id(self,
                           stop_id: str,
                           route_id: str | None = None,
                           service_id: str | None = None,
                           arrival_time: str | None = None,
                           departure_time: str | None = None) -> StopResponse:
        stop = self.stop_repo.get_by_id(stop_id)
        if not stop:
            raise ResourceNotFoundError(f"Stop with ID '{stop_id}' not found")

        if arrival_time is not None and not valid_time_format(arrival_time):
            raise QueryInvalidError(f"arrival_time must be in HH:MM:SS format (e.g., 13:22:15)")

        if departure_time is not None and not valid_time_format(departure_time):
            raise QueryInvalidError(f"departure_time must be in HH:MM:SS format (e.g., 13:22:15)")

        return self._detailed_responsify(stop, route_id, service_id, arrival_time, departure_time)

    def get_all(self) -> List[StopResponse]:
        stops = self.stop_repo.get_all()
        return [self._responsify(stop) for stop in stops]

    def _responsify(self, stop: Stop) -> StopResponse:
        return StopResponse(id=stop.stop_id,
                            name=stop.stop_name,
                            latitude=stop.stop_lat,
                            longitude=stop.stop_lon)

    def _detailed_responsify(self,
                             stop: Stop,
                             route_id: str | None,
                             service_id: str | None,
                             arrival_time: str | None,
                             departure_time: str | None) -> StopDetailedResponse:
        stop_times = self.stop_time_repo.get_all_by_stop_id(stop_id=stop.stop_id,
                                                            route_id=route_id,
                                                            service_id=service_id,
                                                            arrival_time=arrival_time,
                                                            departure_time=departure_time)

        results = []
        for stop_time, trip in stop_times:
            trip_res = StopTimeTrip(id=trip.trip_id,
                                    headsign=trip.trip_headsign,
                                    route_id=trip.route_id,
                                    service_id=ServiceID(trip.service_id))

            stop_time_res = StopTimeResponse(trip=trip_res,
                                             arrival_time=stop_time.arrival_time,
                                             departure_time=stop_time.departure_time)
            results.append(stop_time_res)

        return StopDetailedResponse(id=stop.stop_id,
                                    name=stop.stop_name,
                                    latitude=stop.stop_lat,
                                    longitude=stop.stop_lon,
                                    stop_times=results)
