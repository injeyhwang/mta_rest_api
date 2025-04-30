from app.exceptions.base import ServiceError


class FeedServiceError(ServiceError):
    """Base exception for MTA Feed service errors"""
    pass


class FeedEndpointNotFoundError(FeedServiceError):
    """Raised when a feed endpoint configuration is missing"""
    pass


class FeedFetchError(FeedServiceError):
    """Raised when there's an error fetching the feed from MTA API"""
    pass


class FeedTimeoutError(FeedServiceError):
    """Raised when a request to the MTA API times out"""
    pass


class FeedProcessingError(FeedServiceError):
    """Raised when there's an error processing the feed data"""
    pass
