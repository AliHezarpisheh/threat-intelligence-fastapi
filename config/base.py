"""Module for defining base configurations."""

from .database import AsyncDatabaseConnection
from .logging import LoggingConfig
from .settings.base import Settings

# Settings
settings = Settings()

# Logging
logger = LoggingConfig(env=settings.env).get_logger()

# Database
db = AsyncDatabaseConnection(database_url=settings.database_url)
