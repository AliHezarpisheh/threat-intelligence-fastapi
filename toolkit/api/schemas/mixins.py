"""Defines mixins for API schema classes(Pydantic models)."""

from datetime import datetime
from typing import Annotated

from pydantic import Field
from pydantic.types import PositiveInt

from .base import BaseSchema


class TimestampMixin(BaseSchema):
    """Mixin for timestamp fields (created_at and modified_at)."""

    created_at: Annotated[
        datetime,
        Field(
            ...,
            description="The modification time of the object.",
        ),
    ]
    modified_at: Annotated[
        datetime | None,
        Field(
            description="The modification time of the object.",
        ),
    ] = None


class IdMixin(BaseSchema):
    """Mixin for ID field (id)."""

    id: PositiveInt = Field(..., description="The unique identifier of the object.")


class CommonMixins(IdMixin, TimestampMixin):
    """Combines common mixins: IdMixin and TimestampMixin."""
