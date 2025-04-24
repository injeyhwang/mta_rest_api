from fastapi import APIRouter

from app.api.v1.endpoints import subway


api_router = APIRouter(prefix="/v1")

api_router.include_router(subway.router, prefix="/subway", tags=["subway"])
