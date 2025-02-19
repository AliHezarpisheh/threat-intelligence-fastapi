"""
Module serves the FastAPI instance for the backend application.

It initializes the FastAPI application, configures middleware, setting lifespan context
manager, and defines routes for handling various HTTP requests.
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from config.base import settings
from config.settings.openapi import responses
from toolkit.api.exceptions import (
    CustomHTTPException,
    DoesNotExistError,
    DuplicateResourceError,
    UnauthorizedError,
)

from .exception_handlers import (
    custom_http_exception_handler,
    does_not_exist_exception_handler,
    duplicate_resource_error_handler,
    internal_exception_handler,
    request_validation_exception_handler,
    unauthorized_exception_handler,
)
from .healthcheck import router as health_check_router
from .threat.routers import router as threat_router

# Setup FastAPI instance
app = FastAPI(
    title=settings.openapi.title,
    version=settings.openapi.version,
    description=settings.openapi.description,
    contact=settings.openapi.contact.model_dump(),
    license_info=settings.openapi.license.model_dump(),
    openapi_tags=[tag.model_dump() for tag in settings.openapi.tags],
    responses=responses,
    default_response_class=ORJSONResponse,
    redoc_url=None,
)

# Register custom exception handlers
app.add_exception_handler(
    Exception,
    internal_exception_handler,
)
app.add_exception_handler(
    CustomHTTPException,
    custom_http_exception_handler,  # type: ignore
)
app.add_exception_handler(
    RequestValidationError,
    request_validation_exception_handler,  # type: ignore
)
app.add_exception_handler(
    DoesNotExistError,
    does_not_exist_exception_handler,  # type: ignore
)
app.add_exception_handler(
    DuplicateResourceError,
    duplicate_resource_error_handler,  # type: ignore
)
app.add_exception_handler(
    UnauthorizedError,
    unauthorized_exception_handler,  # type: ignore
)

# Include routers
app.include_router(health_check_router)
app.include_router(threat_router)
