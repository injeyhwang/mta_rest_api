from fastapi import APIRouter, Depends, HTTPException, Path, status
from typing import List

from app.dependencies import get_route_service
from app.schemas.route import RouteResponse
from app.services.route import RouteService
from app.utils.logger import logger


router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("/",
            response_model=List[RouteResponse],
            status_code=status.HTTP_200_OK,
            summary="Get all subway routes",
            description="Retrieve all subway routes",
            responses={500: {"description": "Error retrieving routes"}})
def get_routes(service: RouteService = Depends(get_route_service)) -> List[RouteResponse]:
    try:
        return service.get_all()

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred")


@router.get("/{route_id}",
            response_model=RouteResponse,
            status_code=status.HTTP_200_OK,
            summary="Get subway route by ID",
            description="Retrieve the subway route by given ID",
            responses={404: {"description": "Route not found"},
                       500: {"description": "Error retrieving route"}})
def get_route_by_id(route_id: str = Path(description="The route ID to search"),
                    service: RouteService = Depends(get_route_service)) -> RouteResponse:
    try:
        return service.get_by_id(route_id)

    except ValueError as e:
        logger.error(f"Route with ID '{route_id}' not found: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred")
