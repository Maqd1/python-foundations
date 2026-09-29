class LibraryError(Exception):
    """Base exception for library-related errors."""


class ResourceUnavailableError(LibraryError):
    """Raised when a resource has no available copies."""