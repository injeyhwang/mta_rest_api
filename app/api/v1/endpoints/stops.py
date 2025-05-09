from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from typing import List

from app.dependencies import get_stop_service
from app.exceptions.base import QueryInvalidError, ResourceNotFoundError
from app.schemas.stop import StopDetailedResponse, StopResponse
from app.schemas.trip import ServiceID
from app.services.stop import StopService
from app.utils.logger import logger


router = APIRouter(prefix="/stops", tags=["stops"])


@router.get("/",
            response_model=List[StopResponse],
            status_code=status.HTTP_200_OK,
            summary="Get all subway stops",
            description="Retrieve all subway stops",
            responses={500: {"description": "Error retrieving stops"}})
def get_stops(service: StopService = Depends(get_stop_service)) -> List[StopResponse]:
    try:
        return service.get_all()

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred")


@router.get("/{stop_id}",
            response_model=StopDetailedResponse,
            status_code=status.HTTP_200_OK,
            summary="Get subway stop and stop times by stop ID",
            description="Retrieve the subway stop details by given stop ID",
            responses={400: {"description": "Time must be in HH:MM:SS format (e.g., 13:22:15)"},
                       404: {"description": "Stop not found"},
                       500: {"description": "Error retrieving stop"}})
def get_stop_by_id(stop_id: str = Path(description="The stop ID to search"),
                   route_id: str | None = Query(
                       default=None,
                       description="The route ID to filter this stop's trips by"
                    ),
                   service_id: ServiceID | None = Query(
                       default=None,
                       description="The service ID to filter this stop's trips by"
                    ),
                   arrival_time: str | None = Query(
                       default=None,
                       description="The arrival time to filter this stop's trips by"
                    ),
                   departure_time: str | None = Query(
                       default=None,
                       description="The departure time to filter this stop's trips by"
                    ),
                   service: StopService = Depends(get_stop_service)) -> StopDetailedResponse:
    try:
        return service.get_by_id(stop_id,
                                 route_id,
                                 service_id.value if service_id is not None else None,
                                 arrival_time,
                                 departure_time)

    except QueryInvalidError as e:
        logger.error(f"Invalid time format of arrival_time and/or departure_time: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Time must be in HH:MM:SS format (e.g., 13:22:15)")

    except ResourceNotFoundError as e:
        logger.error(f"Stop with ID '{stop_id}' not found: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found")

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred")
