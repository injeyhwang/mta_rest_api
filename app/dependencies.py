from functools import lru_cache

from app.services.mta_realtime import MTAServiceRT
from app.config import Settings


@lru_cache()
def get_mta_rt_service() -> MTAServiceRT:
    """
    Singleton factory for MTAServiceRT instance. The MTAServiceRT will be dependency injected into
    relevant API routes.

    The @lru_cache() decorator ensures this function is only executed once, and the same instance
    is returned for subsequent calls.
    """
    return MTAServiceRT()
