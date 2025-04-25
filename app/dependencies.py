from functools import lru_cache

from app.services.mta_realtime import MTAServiceRT
from app.config import Settings


@lru_cache()
def mta_service_realtime() -> MTAServiceRT:
    """
    Singleton factory for MTAServiceRT instance. The MTAServiceRT will be dependency injected into
    feed API routes.

    The @lru_cache() decorator ensures this function is only executed once, and the same instance
    is returned for subsequent calls.
    """
    return MTAServiceRT()
