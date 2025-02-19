"""Module for defining redis configurations."""

import redis
import redis.exceptions
from redis.asyncio import ConnectionPool, Redis


class AsyncRedisConnection:
    """class encapsulate Redis connection logic, providing an asynchronous interface."""

    def __init__(
        self, host: str, port: int, db: int, password: str, max_connection: int
    ):
        """Instantiate an `AsyncRedisConnection` object."""
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.max_connection = max_connection

        self.redis_client: Redis | None = None
        self.connection_pool: ConnectionPool | None = None

    def get_client(self) -> Redis:
        """
        Lazily initializes and returns the Redis client.

        Returns
        -------
        redis.asyncio.Redis
            The Redis client.
        """
        if not self.redis_client:
            connection_pool = self.get_connection_pool()
            self.redis_client = Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                password=self.password,
                connection_pool=connection_pool,
            )
        return self.redis_client

    def get_connection_pool(self) -> ConnectionPool:
        """
        Lazily initializes and returns the Redis connection pool.

        Returns
        -------
        redis.asyncio.ConnectionPool
            The Redis connection pool.
        """
        if not self.connection_pool:
            self.connection_pool = ConnectionPool(
                host=self.host,
                port=self.port,
                db=self.db,
                max_connections=self.max_connection,
                encoding="utf-8",
                decode_responses=True,
            )
        return self.connection_pool

    def get_connection(self) -> Redis:
        """Return a `Redis` client from the connection pool."""
        redis_client = self.get_client()
        connection_pool = self.get_connection_pool()
        return redis_client.from_pool(connection_pool)

    async def disconnect(self) -> None:
        """Close the Redis client connection asynchronously."""
        if self.redis_client:
            await self.redis_client.aclose()
            self.redis_client = None

    async def test_connection(self) -> bool:
        """
        Tests the Redis connection by sending a PING command.

        Returns
        -------
        bool
            True if Redis is reachable, False otherwise.
        """
        redis_client = self.get_client()
        try:
            is_available: bool = await redis_client.ping()
            return is_available
        except redis.exceptions.ConnectionError:
            from config.base import logger

            logger.error("Redis instance is not available.", exc_info=True)

            return False
