class ApplicationError(Exception):
    """Base exception for all application errors"""
    pass


class ServiceError(ApplicationError):
    """Base exception for all service-related errors"""
    pass
