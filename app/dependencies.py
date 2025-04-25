from app.services.mta_realtime import MTAServiceRT


mta_rt_service = MTAServiceRT()


def get_mta_rt_service() -> MTAServiceRT:
    """
    Singleton factory for MTAServiceRT instance. The MTAServiceRT will be dependency injected into
    feed API routes.
    """
    return mta_rt_service
