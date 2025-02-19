"""Module provides classes for pagination helper for SQLAlchemy queries."""

from typing import Any

from sqlalchemy.orm import Query


class PageNumberPagination:
    """Pagination helper class for SQLAlchemy queries."""

    @staticmethod
    def paginate(query: Query[Any], page: int, page_size: int) -> Query[Any]:
        """
        Apply pagination to a SQLAlchemy query.

        Parameters
        ----------
        query : sqlalchemy.orm.query.Query
            The SQLAlchemy query to paginate.
        page : int
            The current page number (1-indexed).
        page_size : int
            The number of items per page.

        Returns
        -------
        sqlalchemy.orm.query.Query
            The paginated SQLAlchemy query.
        """
        return query.offset((page - 1) * page_size).limit(page_size)
