from fastapi import APIRouter, Depends
import json

from app.dependencies import get_mta_rt_service
from app.services.mta_realtime import MTAFeed, MTAServiceRT


router = APIRouter()


@router.get("/")
async def get_long_island_rail_road_realtime_feed(service: MTAServiceRT = Depends(get_mta_rt_service)):
    feed_dict = service.get_mta_feed(feed=MTAFeed.LIRR)
    json_string = json.dumps(feed_dict)
    return json_string
