"""Module defining Base Pydantic schema for application schemas."""

from typing import Annotated, Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from toolkit.api.enums import HTTPStatusDoc, Status


class BaseSchema(BaseModel):
    """Base schema for API responses."""

    model_config = ConfigDict(
        allow_inf_nan=True,
        from_attributes=True,
        alias_generator=to_camel,
        populate_by_name=True,
        strict=True,
    )


class APIResponse(BaseSchema):
    """Schema for standard API responses, including status, message, and doc link."""

    status: Annotated[Status, Field(description="The status for the response.")]
    message: Annotated[str, Field(description="The response message.")]
    documentation_link: Annotated[
        HTTPStatusDoc,
        Field(
            description=(
                "A link to documentation providing further information on the response "
                "status code."
            )
        ),
    ]


class APISuccessResponse(APIResponse):
    """Schema for successful API responses, including the actual data."""

    data: Annotated[Any, Field(description="The actual data in the response.")]


class ErrorDetails(BaseSchema):
    """Schema representing additional error details, such as field and reason."""

    field: Annotated[str, Field(description="The reason for the error.")]
    reason: Annotated[
        str, Field(description="The field responsible for the error, if applicable.")
    ]


class APIErrorResponse(APIResponse):
    """Schema for API error responses, with optional error details."""

    details: Annotated[
        ErrorDetails | None, Field(description="Additional details about the error.")
    ] = None
