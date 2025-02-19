"""Module holding enumerations related to the project's settings."""

from enum import StrEnum


class Env(StrEnum):
    """Enumeration class define different environments."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"
