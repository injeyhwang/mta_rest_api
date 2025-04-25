from fastapi import APIRouter

from app.api.v1.endpoints.feeds import feeds_router


api_router = APIRouter(prefix="/v1")
api_router.include_router(feeds_router, prefix="/feeds", tags=["feeds"])
