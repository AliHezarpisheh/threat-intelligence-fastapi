"""Module containing custom exception handlers for FastAPI applications."""

import fastapi
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from config.base import logger
from toolkit.api.enums import HTTPStatusDoc, Messages, Status
from toolkit.api.exceptions import (
    CustomHTTPException,
    DoesNotExistError,
    DuplicateResourceError,
    UnauthorizedError,
)


async def custom_http_exception_handler(
    request: Request, exc: CustomHTTPException
) -> ORJSONResponse:
    """
    Handle CustomHTTPException raised within FastAPI routes.

    Parameters
    ----------
    request : Request
        The incoming request object.
    exc : CustomHTTPException
        The instance of CustomHTTPException raised.

    Returns
    -------
    ORJSONResponse
        JSON response containing error details, including status code,
        error message, details, and documentation link if available.
    """
    return ORJSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status.value,
            "message": exc.message,
            "details": exc.details,
            "documentation_link": exc.documentation_link.value,
        },
    )


async def internal_exception_handler(
    request: Request, exc: Exception
) -> ORJSONResponse:
    """
    Handle unexpected internal server errors by raising a CustomHTTPException.

    This function is an exception handler for any general Python exceptions
    that may arise within FastAPI routes. It catches unhandled exceptions and
    raises a CustomHTTPException with a status code of 500 (Internal Server Error),
    providing a generic error message and documentation link.

    Parameters
    ----------
    request : Request
        The incoming request object.
    exc : Exception
        The general Python exception instance raised.

    Raises
    ------
    CustomHTTPException
        Always raises a CustomHTTPException with a status code of 500
        (Internal Server Error).
    """
    logger.error("Handle general base python exception. Exception details: %s", exc)
    return ORJSONResponse(
        status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": Status.ERROR,
            "message": Messages.INTERNAL_SERVER_ERROR,
            "documentation_link": HTTPStatusDoc.HTTP_STATUS_500,
        },
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> None:
    """
    Handle RequestValidationError by raising a CustomHTTPException with details.

    This function is an exception handler specifically designed to handle
    RequestValidationError exceptions raised within FastAPI routes.
    It raises a CustomHTTPException with a status code of 422 (Unprocessable Entity)
    and includes details such as the error message, reason, affected field,
    and a documentation link.

    Parameters
    ----------
    request : Request
        The incoming request object.
    exc : RequestValidationError
        The instance of RequestValidationError raised.

    Raises
    ------
    CustomHTTPException
        Always raises a CustomHTTPException with a status code of 422
        (Unprocessable Entity).
    """
    exc_data = exc.errors()[0]
    message = exc.errors()[0]["msg"]
    reason = exc.errors()[0]["type"]
    field = exc_data["loc"][1] if len(exc_data["loc"]) >= 2 else "-"
    loc = exc_data["loc"][0]
    logger.error("Handle request validation exception. Exception details: %s", exc_data)
    raise CustomHTTPException(
        status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
        status=Status.VALIDATION_ERROR,
        message=message,
        field=f"{field}, in: {loc}",
        reason=reason,
        documentation_link=HTTPStatusDoc.HTTP_STATUS_422,
    ) from exc


async def unauthorized_exception_handler(
    request: Request, exc: UnauthorizedError
) -> None:
    """
    Handle UnauthorizedError by raising a CustomHTTPException with details.

    This function is an exception handler specifically designed to handle
    UnauthorizedError exceptions raised within FastAPI routes.
    It raises a CustomHTTPException with a status code of 401 (Unauthorized)
    and includes details such as the error message, reason, affected field,
    and a documentation link.

    Parameters
    ----------
    request : Request
        The incoming request object.
    exc : UnauthorizedError
        The instance of UnauthorizedError raised.

    Raises
    ------
    CustomHTTPException
        Always raises a CustomHTTPException with a status code of 401 (Unauthorized).
    """
    logger.error("Handled unauthorized error. Exception details: %s", exc)
    raise CustomHTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        status=Status.UNAUTHORIZED,
        message=str(exc),
        documentation_link=HTTPStatusDoc.HTTP_STATUS_401,
    ) from exc


async def does_not_exist_exception_handler(
    request: Request, exc: DoesNotExistError
) -> None:
    """
    Handle DoesNotExistError by raising a CustomHTTPException with details.

    This function is an exception handler specifically designed to handle
    DoesNotExistError exceptions and its children raised within FastAPI routes.
    It raises a CustomHTTPException with a status code of 404 (Not Found)
    and includes details such as the error message, reason, affected field,
    and a documentation link.

    Parameters
    ----------
    request : Request
        The incoming request object.
    exc : DoesNotExistError
        The instance of DoesNotExistError raised.

    Raises
    ------
    CustomHTTPException
        Always raises a CustomHTTPException with a status code of 404 (Not Found).
    """
    logger.error("Handled does not exist exception. Exception details: %s", exc)
    raise CustomHTTPException(
        status_code=fastapi.status.HTTP_404_NOT_FOUND,
        status=Status.NOT_FOUND,
        message=str(exc),
        documentation_link=HTTPStatusDoc.HTTP_STATUS_404,
    ) from exc


async def duplicate_resource_error_handler(
    request: Request, exc: DuplicateResourceError
) -> None:
    """
    Handle DuplicateResourceError by raising a CustomHTTPException with details.

    This function is an exception handler specifically designed to handle
    DuplicateResourceError exceptions raised within FastAPI routes.
    It raises a CustomHTTPException with a status code of 409 (Conflict)
    and includes details such as the error message, reason, affected field,
    and a documentation link.

    Parameters
    ----------
    request : Request
        The incoming request object.
    exc : DuplicateResourceError
        The instance of DuplicateResourceError raised.

    Raises
    ------
    CustomHTTPException
        Always raises a CustomHTTPException with a status code of 409 (Conflict).
    """
    logger.error("Handle duplicate resource exception. Exception details: %s", exc)
    raise CustomHTTPException(
        status_code=fastapi.status.HTTP_409_CONFLICT,
        status=Status.CONFLICT,
        message=str(exc),
        documentation_link=HTTPStatusDoc.HTTP_STATUS_409,
    ) from exc
