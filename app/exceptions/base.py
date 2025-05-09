class ApplicationError(Exception):
    """Base exception for all application errors"""
    pass


class ServiceError(ApplicationError):
    """Base exception for all service-related errors"""
    pass


class ResourceNotFoundError(ServiceError):
    """Raised when requested resource is not found"""
    pass


class QueryInvalidError(ServiceError):
    """Raised when a request query is in invalid format"""
    pass
