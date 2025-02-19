"""Define enumeration constants for API response messages."""

from enum import StrEnum


class Messages(StrEnum):
    """Enumeration of messages used in API responses."""

    UNAUTHORIZED = (
        "Authentication failed or user does not have permissions for the desired "
        "action."
    )
    FORBIDDEN = (
        "Authentication succeeded but authenticated user does not have access to the "
        "resource."
    )
    METHOD_NOT_ALLOWED = (
        "The requested method is not allowed for the specified resource."
    )

    INTERNAL_SERVER_ERROR = "An unexpected error occurred on the server."
    NOT_IMPLEMENTED = "The requested method is not implemented."
    SERVICE_UNAVAILABLE = (
        "The server is currently unable to handle the request due to a temporary "
        "overloading or maintenance of the server."
    )
