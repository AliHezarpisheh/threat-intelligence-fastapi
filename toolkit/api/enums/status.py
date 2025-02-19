"""Define enumeration constants for status messages."""

from enum import StrEnum


class Status(StrEnum):
    """Enumeration of status messages used in API responses."""

    SUCCESS = "success"
    FAILURE = "failure"
    ERROR = "error"
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    FORBIDDEN = "forbidden"
    CONFLICT = "conflict"
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"
