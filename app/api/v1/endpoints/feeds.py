from fastapi import (APIRouter, Depends, HTTPException, Path, Query, Response,
                     status)

from app.dependencies import get_feed_service
from app.exceptions.feed import (FeedEndpointNotFoundError, FeedFetchError,
                                 FeedProcessingError, FeedTimeoutError)
from app.schemas.feed import Entity, Feed
from app.schemas.pagination import PaginatedResponse
from app.services.feed import FeedService
from app.utils.logger import logger

router = APIRouter(prefix="/feeds", tags=["feeds"])


@router.get("/{feed}",
            response_model=PaginatedResponse[Entity],
            status_code=status.HTTP_200_OK,
            summary="Get all real-time subway feed",
            description="Retrieve real-time data for a given subway feed",
            responses={
                500: {"description": "Error processing GTFS-RT feed"},
                502: {"description": "Error fetching GTFS-RT feed"},
                504: {"description": "Timeout fetching GTFS-RT feed"}})
async def get_all_feed(
        response: Response,
        feed: Feed = Path(description="The subway feed to request"),
        route_id: str | None = Query(
            default=None,
            description="The route ID to filter feed entities by"),
        stop_id: str | None = Query(
            default=None,
            description="The stop ID to filter feed entities by"),
        trip_id: str | None = Query(
            default=None,
            description="The trip ID to filter this feed entities by"),
        offset: int = Query(
            default=0,
            ge=0,
            description="Number of entities to skip"),
        limit: int = Query(
            default=10,
            ge=1,
            le=1000,
            description="Maximum number of entities to return"),
        service: FeedService = Depends(get_feed_service)
) -> PaginatedResponse[Entity]:
    try:
        res, total = service.get_all_feed(feed.value,
                                          route_id,
                                          stop_id,
                                          trip_id,
                                          offset,
                                          limit)

        response.headers["X-GTFS-RT-Version"] = \
            res.header.gtfs_realtime_version
        response.headers["X-GTFS-RT-Timestamp"] = res.header.timestamp

        return PaginatedResponse[Entity](total=total,
                                         offset=offset,
                                         limit=limit,
                                         results=res.entity)

    except FeedEndpointNotFoundError as e:
        logger.error(f"Endpoint not found for feed '{feed}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

    except FeedFetchError as e:
        logger.error(f"Error fetching feed '{feed}': {e}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,
                            detail=str(e))

    except FeedTimeoutError as e:
        logger.error(f"Timeout fetching feed '{feed}': {e}")
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                            detail=str(e))

    except FeedProcessingError as e:
        logger.error(f"Processing error for feed '{feed}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=str(e))

    except Exception as e:
        logger.exception(f"Unexpected error for feed '{feed}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="An unexpected error occurred")
