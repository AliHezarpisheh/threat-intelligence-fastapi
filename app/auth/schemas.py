"""Module defines schemas for auth-related entities."""

from __future__ import annotations

from typing import Annotated

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
