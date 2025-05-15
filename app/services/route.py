from typing import List

from sqlmodel import Session

from app.db.models.gtfs import Route
from app.db.repositories.route import RouteRepository
from app.exceptions.base import ResourceNotFoundError
from app.schemas.route import RouteResponse


class RouteService:
    def __init__(self, session: Session):
        self.session = session
        self.repository = RouteRepository(session)

    def get_by_id(self, route_id: str) -> RouteResponse:
        route = self.repository.get_by_id(route_id)
        if not route:
            raise ResourceNotFoundError(
                f"Route with ID '{route_id}' not found")

        return self._responsify(route)

    def get_all(self) -> List[RouteResponse]:
        routes = self.repository.get_all()
        results = [self._responsify(route) for route in routes]
        return results

    def _responsify(self, route: Route) -> RouteResponse:
        return RouteResponse(id=route.route_id,
                             short_name=route.route_short_name,
                             long_name=route.route_long_name,
                             description=route.route_desc,
                             url=route.route_url,
                             color=route.route_color,
                             text_color=route.route_text_color)
