"""Module defines enumeration classes for auth response messages."""

from enum import StrEnum


class AuthMessages(StrEnum):
    """Enumeration class of messages used in auth responses."""

    SUCCESS_REGISTER_MESSAGE = "Registration has been successful"
    SUCCESS_LOGIN_MESSAGE = "Login has been successful"
    INVALID_CREDENTIALS = "Invalid email or password."
