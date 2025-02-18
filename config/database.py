"""Module for defining base database configurations."""

from __future__ import annotations

from asyncio import current_task

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)


class AsyncDatabaseConnection:
    """Class for managing async database connections."""

    def __init__(self, database_url: str) -> None:
        """Initialize AsyncDatabaseConnection."""
        self._database_url = database_url
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None

    def get_engine(self) -> AsyncEngine:
        """
        Get the async database engine.

        Returns
        -------
        sqlalchemy.ext.asyncio.AsyncEngine
            The async database engine object.
        """
        if not self._engine:
            self._engine = create_async_engine(self._database_url)
        return self._engine

    def get_session_factory(self) -> async_sessionmaker[AsyncSession]:
        """
        Get the session factory.

        Returns
        -------
        sqlalchemy.ext.asyncio.async_sessionmaker
            The session factory.
        """
        if not self._session_factory:
            engine = self.get_engine()
            self._session_factory = async_sessionmaker(
                bind=engine, expire_on_commit=False
            )
        return self._session_factory

    def get_session(self) -> async_scoped_session[AsyncSession]:
        """
        Get a scoped async database session.

        Returns
        -------
        sqlalchemy.ext.asyncio.async_scoped_session
            A scoped async session object.
        """
        session = self.get_session_factory()
        return async_scoped_session(session, scopefunc=current_task)

    async def close_engine(self) -> None:
        """Close the async database engine."""
        if self._engine:
            await self._engine.dispose()

    async def test_connection(self) -> bool:
        """
        Test the database connection.

        Returns
        -------
        bool
            True if the connection is successful, False otherwise.
        """
        try:
            engine = self.get_engine()
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError:
            return False
