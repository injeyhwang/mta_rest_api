from fastapi import APIRouter

from app.api.v1.endpoints import lirr
from app.api.v1.endpoints import mnr
from app.api.v1.endpoints import subway


api_router = APIRouter(prefix="/v1")

api_router.include_router(lirr.router, prefix="/lirr", tags=["lirr"])
api_router.include_router(mnr.router, prefix="/mnr", tags=["mnr"])
api_router.include_router(subway.router, prefix="/subway", tags=["subway"])
