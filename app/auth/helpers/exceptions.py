"""Module defines exceptions related to user."""

from toolkit.api.exceptions import (
    DoesNotExistError,
    DuplicateResourceError,
    UnauthorizedError,
)


class UserDoesNotExistError(DoesNotExistError):
    """Exception raised when a requested user is not found."""


class DuplicateUserError(DuplicateResourceError):
    """Exception raised when a user already exists."""


class InvalidUserCredentials(UnauthorizedError):
    """Exception raised when the user is not authenticated."""


class InternalTokenError(UnauthorizedError):
    """Exception raised when a internal token-related error occur."""
