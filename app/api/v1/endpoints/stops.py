from fastapi import APIRouter, Depends, HTTPException, Path, status
from typing import List

from app.dependencies import get_stop_service
from app.schemas.stop import StopResponse
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
            response_model=StopResponse,
            status_code=status.HTTP_200_OK,
            summary="Get subway stop by ID",
            description="Retrieve the subway stop by given ID",
            responses={404: {"description": "Stop not found"},
                       500: {"description": "Error retrieving stop"}})
def get_stop_by_id(stop_id: str = Path(description="The stop ID to search"),
                   service: StopService = Depends(get_stop_service)) -> StopResponse:
    try:
        return service.get_by_id(stop_id)

    except ValueError as e:
        logger.error(f"Stop with ID '{stop_id}' not found: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stop not found")

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred")
