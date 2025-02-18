"""Module defining Pydantic models for OpenAPI settings."""

from typing import Any

from pydantic import AnyHttpUrl, BaseModel, EmailStr
from pydantic_settings import BaseSettings

from toolkit.api.schemas.errors import (
    BadRequest,
    Conflict,
    Forbidden,
    InternalServerError,
    NotFound,
    Unauthorized,
    UnprocessableEntity,
)


class ContactSettings(BaseModel):
    """Contact information for the API."""

    name: str
    email: EmailStr


class LicenseSettings(BaseModel):
    """License information for the API."""

    name: str
    url: AnyHttpUrl


class TagSettings(BaseModel):
    """Tag information for the API."""

    name: str
    description: str


class OpenAPISettings(BaseSettings):
    """Settings for OpenAPI configuration."""

    title: str
    version: str
    description: str
    contact: ContactSettings
    license: LicenseSettings
    tags: list[TagSettings]


# response variable holding additional responses for app instance
responses: dict[str | int, dict[str, Any]] = {
    "400": {
        "model": BadRequest,
        "description": "Bad request. Invalid or missing parameters.",
    },
    "401": {
        "model": Unauthorized,
        "description": "Unauthorized. User is not authenticated.",
    },
    "403": {
        "model": Forbidden,
        "description": (
            "Forbidden. User does not have permission to access this resource."
        ),
    },
    "404": {
        "model": NotFound,
        "description": "Not Found. The requested resource does not exist.",
    },
    "409": {
        "model": Conflict,
        "description": (
            "Conflict. The request conflicts with the current state of the server."
        ),
    },
    "422": {
        "model": UnprocessableEntity,
        "description": (
            "Unprocessable Entity. The request is well-formed but unable to be "
            "processed due to semantic errors."
        ),
    },
    "500": {
        "model": InternalServerError,
        "description": (
            "Internal Server Error. An unexpected condition was "
            "encountered on the server."
        ),
    },
}
