"""Module defining security schemes and dependencies."""

from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.auth.dependencies import get_token_service
from app.auth.helpers.messages import AuthMessages
from app.auth.services import TokenService
from toolkit.api.exceptions import UnauthorizedError

security = HTTPBearer()


async def verify_token_dependency(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
) -> None:
    """
    FastAPI dependency that verifies the JWT token without returning user data.

    Parameters
    ----------
    credentials : HTTPAuthorizationCredentials
        The HTTP authorization credentials containing the JWT token.

    Raises
    ------
    UnauthorizedError
        If the token is missing, expired, or invalid.
    """
    if not credentials:
        raise UnauthorizedError(AuthMessages.AUTHENTICATION_REQUIRED)

    if credentials.scheme.lower() != token_service.TOKEN_TYPE.lower():
        raise UnauthorizedError(
            AuthMessages.INVALID_AUTH_SCHEME.format(token_type=token_service.TOKEN_TYPE)
        )

    token_service.verify_token(credentials.credentials)
