"""Module for defining base configurations."""

from config.rabbitmq import AsyncRabbitmqManager
from config.redis import AsyncRedisConnection

from .database import AsyncDatabaseConnection
from .logging import LoggingConfig
from .settings.base import Settings

# Settings
settings = Settings()

# Logging
logger = LoggingConfig(env=settings.env).get_logger()

# Database
db = AsyncDatabaseConnection(database_url=settings.database_url)

# RabbitMQ
rabbitmq_manager = AsyncRabbitmqManager(amqp_url=settings.amqp_url)

# Redis
redis_manager = AsyncRedisConnection(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.redis_db,
    password=settings.redis_password,
    max_connection=settings.redis_pool_max_connection,
)

__all__ = ["AsyncRabbitmqManager"]
