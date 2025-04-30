from fastapi import APIRouter

from app.api.v1.endpoints import feeds
from app.api.v1.endpoints import routes


v1_router = APIRouter(prefix="/v1")
v1_router.include_router(feeds.router)
v1_router.include_router(routes.router)
