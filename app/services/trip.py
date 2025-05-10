from sqlmodel import Session

from app.db.models import Trip
from app.db.repositories.stop_time import StopTimeRepository
from app.db.repositories.trip import TripRepository
from app.exceptions.base import QueryInvalidError, ResourceNotFoundError
from app.schemas.pagination import Paginated
from app.schemas.trip import (ScheduledStop, TripDetailed, TripSchedule,
                              TripSimple)
from app.utils.helpers import valid_time_format


class TripService:
    def __init__(self, session: Session):
        self.session = session
        self.stop_time_repo = StopTimeRepository(session)
        self.trip_repo = TripRepository(session)

    def get_by_id(self,
                  trip_id: str,
                  arrival_time: str | None = None,
                  departure_time: str | None = None) -> TripDetailed:
        trip = self.trip_repo.get_by_id(trip_id)
        if not trip:
            raise ResourceNotFoundError(f"Trip with ID '{trip_id}' not found")

        if (arrival_time is not None
                and not valid_time_format(arrival_time)):
            raise QueryInvalidError(
                "arrival_time must be in HH:MM:SS format (e.g., 13:22:15)")

        if (departure_time is not None
                and not valid_time_format(departure_time)):
            raise QueryInvalidError(
                "departure_time must be in HH:MM:SS format (e.g., 13:22:15)")

        return self._detailed_responsify(trip, arrival_time, departure_time)

    def get_all(self,
                route_id: str | None = None,
                service_id: str | None = None,
                direction_id: str | None = None,
                offset: int = 0,
                limit: int = 100) -> Paginated[TripSimple]:
        trips, total = self.trip_repo.get_all(
            route_id, service_id, direction_id, offset, limit)
        results = [self._responsify(trip) for trip in trips]

        return Paginated[TripSimple](total=total,
                                     offset=offset,
                                     limit=limit,
                                     results=results)

    def _responsify(self, trip: Trip) -> TripSimple:
        return TripSimple(id=trip.trip_id,
                          headsign=trip.trip_headsign,
                          route_id=trip.route_id,
                          service_id=trip.service_id,
                          direction_id=trip.direction_id)

    def _detailed_responsify(
            self,
            trip: Trip,
            arrival_time: str | None,
            departure_time: str | None) -> TripDetailed:
        stop_times = self.stop_time_repo.get_all_by_trip_id(
            trip_id=trip.trip_id,
            arrival_time=arrival_time,
            departure_time=departure_time)

        results = []
        for stop_time, stop in stop_times:
            stop_res = ScheduledStop(id=stop.stop_id,
                                     name=stop.stop_name,
                                     latitude=stop.stop_lat,
                                     longitude=stop.stop_lon)

            stop_time_res = TripSchedule(
                stop=stop_res,
                stop_sequence=stop_time.stop_sequence,
                arrival_time=stop_time.arrival_time,
                departure_time=stop_time.departure_time)
            results.append(stop_time_res)

        return TripDetailed(id=trip.trip_id,
                            headsign=trip.trip_headsign,
                            route_id=trip.route_id,
                            service_id=trip.service_id,
                            direction_id=trip.direction_id,
                            stop_times=results)
