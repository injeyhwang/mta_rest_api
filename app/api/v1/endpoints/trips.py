from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.dependencies import get_trip_service
from app.schemas.pagination import PaginatedResponse
from app.schemas.trip import DirectionID, ServiceID, TripResponse
from app.services.trip import TripService
from app.utils.logger import logger


router = APIRouter(prefix="/trips", tags=["trips"])


@router.get("/",
            response_model=PaginatedResponse[TripResponse],
            status_code=status.HTTP_200_OK,
            summary="Get all paginated subway trips",
            description="Retrieve all paginated subway trips. Can be further filtered down by their \
                route_id, service_id, and/or direction_id",
            responses={500: {"description": "Error retrieving trips"}})
def get_trips(route_id: str | None = Query(default=None,
                                           description="The route ID to filter by"),
              service_id: ServiceID | None = Query(default=None,
                                                   description="The service ID to filter by"),
              direction_id: DirectionID | None = Query(default=None,
                                                       description="The direction ID to filter by"),
              offset: int = Query(default=0, ge=0, description="Number of trips to skip"),
              limit: int = Query(default=100,
                                 ge=1,
                                 le=1000,
                                 description="Maximum number of trips to return"),
              service: TripService = Depends(get_trip_service)) -> PaginatedResponse[TripResponse]:
    try:
        return service.get_all(route_id,
                               service_id.value if service_id is not None else None,
                               direction_id,
                               offset,
                               limit)

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred")


@router.get("/{trip_id}",
            response_model=TripResponse,
            status_code=status.HTTP_200_OK,
            summary="Get a single subway trip by ID",
            description="Retrieve subway trip by ID",
            responses={404: {"description": "Trip not found"},
                       500: {"description": "Error retrieving trip"}})
def get_trip_by_id(trip_id: str = Path(description="The trip ID to search"),
                   service: TripService = Depends(get_trip_service)) -> TripResponse:
    try:
        return service.get_by_id(trip_id)

    except ValueError:
        logger.error(f"Trip with ID '{trip_id}' not found: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trip not found")

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred")

