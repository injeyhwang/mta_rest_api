from typing import List

from sqlmodel import Session

from app.db.models import Stop
from app.db.repositories.stop import StopRepository
from app.db.repositories.stop_time import StopTimeRepository
from app.exceptions.base import QueryInvalidError, ResourceNotFoundError
from app.schemas.stop import (ScheduledTrip, StopDetailed, StopSchedule,
                              StopSimple)
from app.schemas.trip import ServiceID
from app.utils.helpers import valid_time_format


class StopService:
    def __init__(self, session: Session):
        self.session = session
        self.stop_repo = StopRepository(session)
        self.stop_time_repo = StopTimeRepository(session)

    def get_by_id(self,
                  stop_id: str,
                  route_id: str | None = None,
                  service_id: str | None = None,
                  arrival_time: str | None = None,
                  departure_time: str | None = None) -> StopSimple:
        stop = self.stop_repo.get_by_id(stop_id)
        if not stop:
            raise ResourceNotFoundError(f"Stop with ID '{stop_id}' not found")

        if (arrival_time is not None
                and not valid_time_format(arrival_time)):
            raise QueryInvalidError(
                "arrival_time must be in HH:MM:SS format (e.g., 13:22:15)")

        if (departure_time is not None
                and not valid_time_format(departure_time)):
            raise QueryInvalidError(
                "departure_time must be in HH:MM:SS format (e.g., 13:22:15)")

        return self._detailed_responsify(stop,
                                         route_id,
                                         service_id,
                                         arrival_time,
                                         departure_time)

    def get_all(self, direction_id: int | None = None) -> List[StopSimple]:
        stops = self.stop_repo.get_all(direction_id=direction_id)
        return [self._responsify(stop) for stop in stops]

    def _responsify(self, stop: Stop) -> StopSimple:
        return StopSimple(id=stop.stop_id,
                          name=stop.stop_name,
                          latitude=stop.stop_lat,
                          longitude=stop.stop_lon)

    def _detailed_responsify(self,
                             stop: Stop,
                             route_id: str | None,
                             service_id: str | None,
                             arrival_time: str | None,
                             departure_time: str | None) -> StopDetailed:
        stop_times = self.stop_time_repo.get_all_by_stop_id(
            stop_id=stop.stop_id,
            route_id=route_id,
            service_id=service_id,
            arrival_time=arrival_time,
            departure_time=departure_time)

        results = []
        for stop_time, trip in stop_times:
            trip_res = ScheduledTrip(id=trip.trip_id,
                                     headsign=trip.trip_headsign,
                                     route_id=trip.route_id,
                                     service_id=ServiceID(trip.service_id))

            stop_time_res = StopSchedule(
                trip=trip_res,
                arrival_time=stop_time.arrival_time,
                departure_time=stop_time.departure_time)
            results.append(stop_time_res)

        return StopDetailed(id=stop.stop_id,
                            name=stop.stop_name,
                            latitude=stop.stop_lat,
                            longitude=stop.stop_lon,
                            stop_times=results)
