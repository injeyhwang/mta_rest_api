from app.exceptions.base import ServiceError


class MTAServiceError(ServiceError):
    """Base exception for MTA service errors"""
    pass


class MTAEndpointNotFoundError(MTAServiceError):
    """Raised when a feed endpoint configuration is missing"""
    pass


class MTAFeedFetchError(MTAServiceError):
    """Raised when there's an error fetching the feed from MTA API"""
    pass


class MTAFeedTimeoutError(MTAServiceError):
    """Raised when a request to the MTA API times out"""
    pass


class MTAFeedProcessingError(MTAServiceError):
    """Raised when there's an error processing the feed data"""
    pass
