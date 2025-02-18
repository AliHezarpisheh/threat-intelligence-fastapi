"""Pagination utility for API responses."""

from typing import Annotated

from pydantic import Field

from .base import BaseSchema


class Pagination(BaseSchema):
    """Model representing pagination details."""

    total_items: Annotated[
        int, Field(..., ge=0, description="Total number of items available.")
    ]
    total_pages: Annotated[
        int,
        Field(
            ...,
            ge=1,
            description="Total number of pages available based on items per page.",
        ),
    ]
    current_page: Annotated[
        int, Field(..., ge=1, description="The current page number being viewed.")
    ]
    next_page: Annotated[
        str | None, Field(description="Endpoint or the Url for the next page.")
    ] = None
    previous_page: Annotated[
        str | None, Field(description="Endpoint or the Url for the previous page.")
    ] = None
