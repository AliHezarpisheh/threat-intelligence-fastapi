"""Module defines schemas for auth-related."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Annotated, Literal

import pydantic
from pydantic import EmailStr, Field

from toolkit.api.schemas.base import APIResponse, BaseSchema
from toolkit.api.schemas.mixins import CommonMixins


class UserRegisterInput(BaseSchema):
    """Input schema for creating a new user."""

    username: Annotated[str, Field(description="Unique username")]
    email: Annotated[EmailStr, Field(description="Unique email address")]
    password: Annotated[str, Field(description="Raw password provided by the client")]


class UserAuthenticateInput(BaseSchema):
    """Input schema for user login."""

    email: Annotated[EmailStr, Field(description="Unique email address")]
    password: Annotated[str, Field(description="Raw password provided by the client")]


class UserOutputData(CommonMixins, BaseSchema):
    """User output data schema."""

    username: Annotated[str, Field(description="Unique username")]
    email: Annotated[str, Field(description="Unique email address")]
    is_active: Annotated[bool, Field(description="Indicates if the user is active")]


class UserOutput(APIResponse):
    """Output schema for successful user operations output, containing the user data."""

    data: UserOutputData


@pydantic.dataclasses.dataclass
class JwtClaims:
    """Pydantic dataclass representing JWT claims."""

    sub: int
    aud: list[str] | str
    iat: datetime
    nbf: datetime
    exp: datetime
    jti: str = Field(default_factory=lambda: str(uuid.uuid4()))
    issue: str = "rental_house_fastapi"


class TokenOutput(BaseSchema):
    """Output schema for granting user an access token with the token type."""

    access_token: str
    type: Literal["Bearer"] = "Bearer"
