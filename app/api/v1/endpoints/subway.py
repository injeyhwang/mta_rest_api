from fastapi import APIRouter, Depends, HTTPException
import json

from app.dependencies import get_mta_rt_service
from app.services.mta_realtime import MTAFeed, MTAServiceRT


router = APIRouter()


@router.get("/{line}")
async def get_subway_realtime_feed(line: str, service: MTAServiceRT = Depends(get_mta_rt_service)):
    if not line in MTAFeed.SUBWAY_LINES:
        raise HTTPException(status_code=404, detail=f"No real-time feed found for subway line: '{line}'.")

    feed_dict = service.get_mta_feed(feed=line)
    json_string = json.dumps(feed_dict)
    return json_string
