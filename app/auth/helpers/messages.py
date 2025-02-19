"""Module defines enumeration classes for auth response messages."""

from enum import StrEnum


class AuthMessages(StrEnum):
    """Enumeration class of messages used in auth responses."""

    SUCCESS_REGISTER_MESSAGE = "Registration has been successful"
    SUCCESS_LOGIN_MESSAGE = "Login has been successful"
    INVALID_CREDENTIALS = "Invalid email or password"
    TOKEN_EXPIRED = "The authentication token has expired"
    INVALID_TOKEN = "The authentication token is invalid or malformed"
    AUTHENTICATION_REQUIRED = "Authentication is required to access this resource"
    INVALID_AUTH_SCHEME = "Authentication scheme must be {token_type}"
    INTERNAL_TOKEN_ERROR = (
        "Internal error generating token. Check the logs for more info."
    )
