"""Module containing dependency services for the auth API."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.auth.services import AuthService, TokenService
from toolkit.api.database import get_async_db_session


async def get_auth_service(
    db_session: Annotated[
        async_scoped_session[AsyncSession], Depends(get_async_db_session)
    ],
) -> AuthService:
    """Get `AuthService` dependency, injecting db session."""
    return AuthService(db_session=db_session)


async def get_token_service() -> TokenService:
    """Get `TokenService` dependency."""
    return TokenService()
