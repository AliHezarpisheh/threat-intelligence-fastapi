"""Module for setting lifespan context manager for FastAPI application."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter

from config.base import redis_manager


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Set lifespan context manager for FastAPI application."""
    redis_connection = redis_manager.get_connection()
    await FastAPILimiter.init(redis=redis_connection)
    yield
    await FastAPILimiter.close()
