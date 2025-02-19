"""Tests for the Pagination class in toolkit.api.pagination module."""

from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Query

from toolkit.api.pagination import PageNumberPagination


@pytest.fixture
def mock_query() -> MagicMock:
    """Fixture to create a mock SQLAlchemy Query object."""
    return MagicMock(spec=Query)


@pytest.mark.parametrize(
    ["page", "page_size"],
    [(1, 10), (2, 10), (1, 20), (2, 20), (3, 20), (4, 20)],
)
def test_paginate(mock_query: MagicMock, page: int, page_size: int) -> None:
    """
    Fixture to create a mock SQLAlchemy Query object.

    Parameters
    ----------
    mock_query : MagicMock
        A mock SQLAlchemy Query object.
    page : int
        Page number.
    page_size : int
        Page size.
    """
    # Expected calls
    expected_offset = (page - 1) * page_size
    expected_limit = page_size

    # Mock the chainable methods
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query

    result = PageNumberPagination.paginate(mock_query, page, page_size)

    mock_query.offset.assert_called_once_with(expected_offset)
    mock_query.limit.assert_called_once_with(expected_limit)

    assert result == mock_query
