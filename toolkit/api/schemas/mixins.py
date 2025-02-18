"""Defines mixins for API schema classes(Pydantic models)."""

from datetime import datetime
from typing import Annotated

from pydantic import Field
from pydantic.types import PositiveInt

from .base import BaseSchema


class TimestampMixin(BaseSchema):
    """Mixin for timestamp fields (created_at and updated_at)."""

    created_at: Annotated[
        datetime,
        Field(
            ...,
            description="The modification time of the object.",
        ),
    ]
    updated_at: Annotated[
        datetime | None,
        Field(
            description="The modification time of the object.",
        ),
    ] = None


class AuditMixin(BaseSchema):
    """Mixin for audit fields (created_by and updated_by)."""

    created_by: Annotated[
        str,
        Field(
            ...,
            description="ID of the user who created the object.",
        ),
    ]
    updated_by: Annotated[
        str | None,
        Field(
            description="ID of the user who modified the object.",
        ),
    ] = None


class IdMixin(BaseSchema):
    """Mixin for ID field (id)."""

    id: PositiveInt = Field(..., description="The unique identifier of the object.")


class CommonMixins(IdMixin, TimestampMixin):
    """Combines common mixins: IdMixin and TimestampMixin."""
