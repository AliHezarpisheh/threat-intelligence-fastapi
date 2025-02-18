"""Module defining Pydantic models for error handling in API responses."""

from pydantic import ConfigDict
from pydantic.alias_generators import to_camel

from toolkit.api.schemas.base import APIErrorResponse


class BadRequest(APIErrorResponse):
    """Represents a 400 Bad Request error."""

    model_config = ConfigDict(
        allow_inf_nan=True,
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "status": "error",
                    "message": "Bad request. Invalid or missing parameters.",
                    "documentationLink": (
                        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400"
                    ),
                    "details": {
                        "field": "parameter_name",
                        "reason": (
                            "Description of the reason why the parameter is invalid "
                            "or missing."
                        ),
                    },
                }
            ]
        },
    )


class Unauthorized(APIErrorResponse):
    """Represents a 401 Unauthorized error."""

    model_config = ConfigDict(
        allow_inf_nan=True,
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "status": "unauthorized",
                    "message": "Unauthorized. User is not authenticated.",
                    "documentationLink": (
                        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401"
                    ),
                }
            ]
        },
    )


class Forbidden(APIErrorResponse):
    """Represents a 403 Forbidden error."""

    model_config = ConfigDict(
        allow_inf_nan=True,
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "status": "forbidden",
                    "message": "User does not have permission to access this resource.",
                    "documentationLink": (
                        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403"
                    ),
                }
            ]
        },
    )


class NotFound(APIErrorResponse):
    """Represents a 404 Not Found error."""

    model_config = ConfigDict(
        allow_inf_nan=True,
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "status": "not_found",
                    "message": "Not Found. The requested resource does not exist.",
                    "documentationLink": (
                        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404"
                    ),
                }
            ]
        },
    )


class Conflict(APIErrorResponse):
    """Represents a 409 Conflict error."""

    model_config = ConfigDict(
        allow_inf_nan=True,
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "status": "conflict",
                    "message": (
                        "Conflict. The request conflicts with the current state of "
                        "the server."
                    ),
                    "documentationLink": (
                        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/409"
                    ),
                }
            ]
        },
    )


class UnprocessableEntity(APIErrorResponse):
    """Represents a 422 Unprocessable Entity error."""

    model_config = ConfigDict(
        allow_inf_nan=True,
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "status": "validation_error",
                    "message": (
                        "Unprocessable Entity. The request is well-formed but unable "
                        "to be processed due to semantic errors."
                    ),
                    "documentationLink": (
                        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/422"
                    ),
                    "details": {
                        "field": "entity_name",
                        "reason": "Description of the semantic error.",
                    },
                }
            ]
        },
    )


class InternalServerError(APIErrorResponse):
    """Represents a 500 Internal Server Error."""

    model_config = ConfigDict(
        allow_inf_nan=True,
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
        strict=True,
        json_schema_extra={
            "examples": [
                {
                    "status": "error",
                    "message": (
                        "Internal Server Error. An unexpected condition was "
                        "encountered on the server."
                    ),
                    "documentationLink": (
                        "https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500"
                    ),
                }
            ]
        },
    )
