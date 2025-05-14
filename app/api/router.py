from fastapi import APIRouter

from app.api import root
from app.api.v1.endpoints import feeds, routes, stops, trips
from app.settings import settings

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(feeds.router)
v1_router.include_router(routes.router)
v1_router.include_router(stops.router)
v1_router.include_router(trips.router)


router = APIRouter()
router.include_router(root.router)
router.include_router(v1_router, prefix=settings.api_prefix)
