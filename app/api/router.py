from fastapi import APIRouter

from app.api.v1.endpoints import feeds


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(feeds.router, prefix="/feeds", tags=["feeds"])
