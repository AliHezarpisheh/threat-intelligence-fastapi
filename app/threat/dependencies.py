"""Module containing dependencies for the threat API."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.threat.services import ThreatReportService
from toolkit.api.database import get_async_db_session


async def get_threat_report_service(
    db_session: Annotated[
        async_scoped_session[AsyncSession], Depends(get_async_db_session)
    ],
) -> ThreatReportService:
    """Get `ThreatReportService` dependency, injecting db session."""
    return ThreatReportService(db_session=db_session)
