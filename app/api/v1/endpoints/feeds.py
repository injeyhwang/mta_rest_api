from fastapi import APIRouter, Depends, HTTPException, Path, status
from app.dependencies import get_mta_rt_service
from app.models.realtime_models import Feed, FeedResponse
from app.services.mta_realtime import MTAServiceRT

from app.logger import logger


router = APIRouter()


@router.get("/{feed}",
            response_model=FeedResponse,
            status_code=status.HTTP_200_OK,
            summary="Get real-time subway line feed",
            description="Retrieve real-time data for a given subway feed",
            responses={502: {"description": "Error fetching GTFS-RT feed"},
                       504: {"description": "Timeout fetching GTFS-RT feed"}})
async def get_ace_feed(feed: Feed = Path(description=""),
                       service: MTAServiceRT = Depends(get_mta_rt_service)) -> str:
    try:
        feed_data = service.get_mta_feed(feed.value)
        return FeedResponse(**feed_data)

    except Exception as e:
        logger.exception(f"Error fetching feed '{feed}': {e}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail=f"Error fetching GTFS-RT '{feed}' feed: {e}")
