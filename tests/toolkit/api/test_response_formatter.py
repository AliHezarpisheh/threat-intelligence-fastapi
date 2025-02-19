"""Tests for the ResponseFormatter class in toolkit.api.response_formatter module."""

from typing import Optional, Union

import pytest
from pydantic import BaseModel

from toolkit.annotations import JSON
from toolkit.api.enums import Status
from toolkit.api.response_formatter import ResponseFormatter
from toolkit.api.schemas import Pagination


class MockPydanticModel(BaseModel):
    """Mock Pydantic model for testing."""

    status: Status
    message: str
    data: Union[BaseModel, JSON, list[BaseModel], list[JSON]]
    links: Optional[JSON]
    pagination: Optional[Pagination]


@pytest.fixture
def formatter() -> ResponseFormatter:
    """Fixture for creating a ResponseFormatter instance."""
    return ResponseFormatter()


def test_format_response(formatter: ResponseFormatter):
    """Test the format_response method of ResponseFormatter."""
    status = Status.SUCCESS
    message = "Test message"
    data = {"key": "value"}
    links = {"self": "http://example.com"}
    pagination = Pagination(total_items=100, total_pages=10, current_page=1)

    expected_response = MockPydanticModel(
        status=status,
        message=message,
        data=data,
        links=links,
        pagination=pagination,
    )
    actual_response = formatter.format_response(
        MockPydanticModel, status, message, data, links, pagination
    )

    assert actual_response.model_dump() == expected_response.model_dump()


def test_format_response_no_links_no_pagination(formatter: ResponseFormatter):
    """Test the format_response method with default links and no pagination."""
    status = Status.SUCCESS
    message = "Test message"
    data = {"key": "value"}

    expected_response = MockPydanticModel(
        status=status,
        message=message,
        data=data,
        links={},
        pagination=None,
    )
    actual_response = formatter.format_response(
        MockPydanticModel,
        status,
        message,
        data,
    )

    assert actual_response.model_dump() == expected_response.model_dump()


def test_format_pagination(formatter):
    """Test the format_pagination method of ResponseFormatter."""
    total_items = 100
    page = 2
    page_size = 10
    url = "http://example.com/items"

    expected_pagination = Pagination(
        total_items=total_items,
        total_pages=10,
        current_page=page,
    )
    expected_links = {
        "next_page": f"{url}?page={page + 1}?page_size={page_size}",
        "previous_page": f"{url}?page={page - 1}?page_size={page_size}",
    }

    result_pagination, result_links = formatter.format_pagination(
        total_items, page, page_size, url
    )

    assert result_pagination == expected_pagination
    assert result_links == expected_links


def test_format_pagination_first_page(formatter):
    """Test the format_pagination method on the first page."""
    total_items = 100
    page = 1
    page_size = 10
    endpoint = "http://example.com/items"

    expected_pagination = Pagination(
        total_items=total_items,
        total_pages=10,
        current_page=page,
    )
    expected_links = {
        "next_page": f"{endpoint}?page={page + 1}?page_size={page_size}",
        "previous_page": None,
    }
    actual_pagination, actual_links = formatter.format_pagination(
        total_items, page, page_size, endpoint
    )

    assert actual_pagination == expected_pagination
    assert actual_links == expected_links


def test_format_pagination_last_page(formatter):
    """Test the format_pagination method on the last page."""
    total_items = 100
    page = 10
    page_size = 10
    endpoint = "http://example.com/items"

    expected_pagination = Pagination(
        total_items=total_items,
        total_pages=10,
        current_page=page,
    )
    expected_links = {
        "next_page": None,
        "previous_page": f"{endpoint}?page={page - 1}?page_size={page_size}",
    }

    actual_pagination, result_links = formatter.format_pagination(
        total_items, page, page_size, endpoint
    )

    assert actual_pagination == expected_pagination
    assert result_links == expected_links
