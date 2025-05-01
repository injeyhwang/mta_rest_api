from sqlmodel import Session

from app.db.models import Trip
from app.db.repositories.trip import TripRepository
from app.schemas.pagination import PaginatedResponse
from app.schemas.trip import TripResponse


class TripService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = TripRepository(session)

    def get_by_id(self, trip_id: str) -> TripResponse:
        trip = self.repository.get_by_id(trip_id)
        if not trip:
            raise ValueError(f"Trip with ID '{trip_id}' not found")

        return self._responsify(trip)

    def get_all(self,
                route_id: str | None = None,
                service_id: str | None = None,
                direction_id: str | None = None,
                offset: int = 0,
                limit: int = 100) -> PaginatedResponse[TripResponse]:

        trips, total = self.repository.get_all(route_id, service_id, direction_id, offset, limit)
        results = [self._responsify(trip) for trip in trips]

        return PaginatedResponse[TripResponse](total=total, offset=offset, limit=limit, results=results)

    def _responsify(self, trip: Trip) -> TripResponse:
        return TripResponse(id=trip.trip_id,
                            headsign=trip.trip_headsign,
                            route_id=trip.route_id,
                            service_id=trip.service_id,
                            direction_id=trip.direction_id)
