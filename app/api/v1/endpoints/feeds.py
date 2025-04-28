from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from app.dependencies import get_mta_service
from app.exceptions.mta import (
    MTAEndpointNotFoundError,
    MTAFeedFetchError,
    MTAFeedTimeoutError,
    MTAFeedProcessingError
)
from app.schemas.realtime_schemas import Feed, PaginatedFeedResponse
from app.services.mta_service import MTAService

from app.utils.logger import logger


router = APIRouter()


@router.get("/{feed}",
            response_model=PaginatedFeedResponse,
            status_code=status.HTTP_200_OK,
            summary="Get real-time subway line feed",
            description="Retrieve real-time data for a given subway feed",
            responses={500: {"description": "Error processing GTFS-RT feed"},
                       502: {"description": "Error fetching GTFS-RT feed"},
                       504: {"description": "Timeout fetching GTFS-RT feed"}})
async def get_subway_feed(feed: Feed = Path(description="The subway feed to request"),
                          offset: int = Query(default=0, ge=0, description="Number of entities to skip"),
                          limit: int = Query(default=10,
                                             ge=1,
                                             le=500,
                                             description="Maximum number of entities to return"),
                          service: MTAService = Depends(get_mta_service)) -> PaginatedFeedResponse:
    try:
        res, total_items = service.get_paginated_mta_feed(feed.value, offset, limit)

        return PaginatedFeedResponse(header=res.header,
                                     total=total_items,
                                     offset=offset,
                                     limit=limit,
                                     results=res.entity)

    except MTAEndpointNotFoundError as e:
        logger.error(f"Endpoint not found for feed '{feed}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    except MTAFeedFetchError as e:
        logger.error(f"Error fetching feed '{feed}': {e}")
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))

    except MTAFeedTimeoutError as e:
        logger.error(f"Timeout fetching feed '{feed}': {e}")
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=str(e))

    except MTAFeedProcessingError as e:
        logger.error(f"Processing error for feed '{feed}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    except Exception as e:
        logger.exception(f"Unexpected error for feed '{feed}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                           detail="An unexpected error occurred")
