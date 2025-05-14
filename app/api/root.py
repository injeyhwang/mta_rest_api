from fastapi import APIRouter, HTTPException, status

from app.schemas.root import RootResponse
from app.settings import settings
from app.utils.logger import logger

router = APIRouter()


@router.get("/",
            response_model=RootResponse,
            status_code=status.HTTP_200_OK,
            summary="Get application metadata",
            description="Retrieve app metadata information",
            responses={500: {"description": "Error retrieving app metadata"}})
def read_root() -> RootResponse:
    try:
        return RootResponse(app_name=settings.app_name,
                            app_version=settings.app_version,
                            app_description=settings.app_description,
                            api_version=settings.api_version,
                            documentation_url="/docs")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred")
