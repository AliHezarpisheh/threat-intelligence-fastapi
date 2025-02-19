"""Module defines routers related to auth."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.auth.dependencies import (
    get_auth_service,
)
from app.auth.schemas import (
    TokenOutput,
    UserAuthenticateInput,
    UserOutput,
    UserRegisterInput,
)
from app.auth.services import AuthService
from toolkit.api.enums import OpenAPITags

router = APIRouter(tags=[OpenAPITags.AUTH])


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOutput,
)
async def register(
    user_input: UserRegisterInput,
    user_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict[str, Any]:
    """
    Register a new user with the provided details.

    This endpoint accepts user details such as username, email, and password,
    and creates a new user account.

    - **username**: Unique identifier for the user.
    - **email**: The email address of the user, which must be valid.
    - **password**: A secure password for the user account.
    \f
    Parameters
    ----------
    user_input : UserRegisterInput
        A Pydantic schema containing the user's registration data.
    user_service : AuthService
        A service dependency for handling user operations.

    Returns
    -------
    dict
        A dictionary containing the status, message, documentation link,
        and user data if registration is successful.
    """
    return await user_service.register(user_input=user_input)


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenOutput,
    response_model_exclude_none=True,
)
async def login(
    user_input: UserAuthenticateInput,
    user_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict[str, Any]:
    """
    Authenticate a user through the user's credentials.

    This endpoint validates the user's credentials (e.g., email and password)
    and returns a JWT token upon successful authentication.

    - **password**: The password provided by the client.
    - **email**: The email address of the user, which must be valid.

    \f
    Parameters
    ----------
    user_input : UserAuthenticateInput
        The input data containing the user's credentials.
    user_service : AuthService
        A service dependency for performing user authentication.

    Returns
    -------
    dict
        A dictionary containing the token and token type.

    Notes
    -----
    - The credentials are validated against stored user data.
    - If authentication fails, an appropriate error message will be returned.
    """
    return await user_service.authenticate(user_input=user_input)
