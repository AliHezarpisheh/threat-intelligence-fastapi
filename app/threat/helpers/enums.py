"""Module defines enumeration classes for threat sub-app."""

from enum import StrEnum


class ThreatType(StrEnum):
    """Enumeration class, representing different threat types."""

    IP = "ip"
    EMAIL = "email"
    DOMAIN = "domain"
    FILE = "file"
    URL = "url"
    USER_AGENT = "user_agent"
