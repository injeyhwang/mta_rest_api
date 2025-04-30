from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlmodel import Session
from typing import List

from app.db.repositories.route import RouteRepository
from app.dependencies import get_db_session
from app.schemas.base import RouteResponse
from app.utils.logger import logger


router = APIRouter(prefix="/routes", tags=["routes"])


@router.get("/",
            response_model=List[RouteResponse],
            status_code=status.HTTP_200_OK,
            summary="Get all subway routes",
            description="Retrieve all subway routes",
            responses={500: {"description": "Error retrieving routes"}})
def get_routes(session: Session = Depends(get_db_session)) -> List[RouteResponse]:
    try:
        route_repo = RouteRepository(session)
        return route_repo.get_all()

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
                    session: Session = Depends(get_db_session)) -> RouteResponse:
    try:
        route_repo = RouteRepository(session)
        found = route_repo.get_by_id(route_id)
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Route not found")
        return found

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred")
