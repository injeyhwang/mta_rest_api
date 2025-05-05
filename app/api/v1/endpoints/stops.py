from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.dependencies import get_stop_service
from app.schemas.pagination import PaginatedResponse
from app.schemas.stop import StopDetailedResponse, StopResponse
from app.services.stop import StopService
from app.utils.logger import logger


router = APIRouter(prefix="/stops", tags=["stops"])


@router.get("/",
            response_model=PaginatedResponse[StopResponse],
            status_code=status.HTTP_200_OK,
            summary="Get all subway stops",
            description="Retrieve all subway stops",
            responses={500: {"description": "Error retrieving stops"}})
def get_stops(offset: int = Query(default=0, ge=0, description="Number of stops to skip"),
              limit: int = Query(default=10,
                                 ge=1,
                                 le=1000,
                                 description="Maximum number of stops to return"),
              service: StopService = Depends(get_stop_service)) -> PaginatedResponse[StopResponse]:
    try:
        return service.get_all(offset=offset, limit=limit)

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred")


@router.get("/{stop_id}",
            response_model=StopDetailedResponse,
            status_code=status.HTTP_200_OK,
            summary="Get subway stop and stop times by stop ID",
            description="Retrieve the subway stop details by given stop ID",
            responses={404: {"description": "Stop not found"},
                       500: {"description": "Error retrieving stop"}})
def get_stop_by_id(stop_id: str = Path(description="The stop ID to search"),
                   service: StopService = Depends(get_stop_service)) -> StopDetailedResponse:
    try:
        return service.get_detailed_by_id(stop_id)

    except ValueError as e:
        logger.error(f"Stop with ID '{stop_id}' not found: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found")

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred")
