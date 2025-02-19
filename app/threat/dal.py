"""
Module containing repository data access layer for threat related operations.

This module provides methods for interacting with the database to perform
CRUD operations on the threat report model.
"""

from sqlalchemy import insert, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.threat.helpers.exceptions import ThreatReportDoesNotExistsError
from app.threat.models import ThreatReport
from app.threat.schemas import ThreatReportInputSchema


class ThreatReportDataAccessLayer:
    """Data access layer for threat report related operations."""

    def __init__(self, db_session: async_scoped_session[AsyncSession]) -> None:
        """
        Initialize the `ThreatReportDataAccessLayer`.

        Parameters
        ----------
        db_session : async_scoped_session[AsyncSession]
            The database session for asynchronous operations.
        """
        self.db_session = db_session

    async def create_threat_report(
        self, threat_report_input: ThreatReportInputSchema
    ) -> ThreatReport:
        """
        Create a new threat report.

        Parameters
        ----------
        threat_report_input : ThreatReportInputSchema
            The input data for creating a new threat report.

        Returns
        -------
        ThreatReport
            The newly created threat report.
        """
        stmt = (
            insert(ThreatReport)
            .values(**threat_report_input.model_dump())
            .returning(ThreatReport)
        )

        async with self.db_session.begin():
            result = await self.db_session.execute(stmt)
            return result.scalar_one()

    async def get_threat_report(self, threat_report_id: int) -> ThreatReport:
        """
        Retrieve a threat report by its ID.

        Parameters
        ----------
        threat_report_id : int
            The ID of the threat report to retrieve.

        Returns
        -------
        ThreatReport
            The threat report.
        """
        stmt = select(ThreatReport).where(ThreatReport.id == threat_report_id)

        async with self.db_session.begin():
            result = await self.db_session.execute(stmt)
            try:
                return result.scalar_one()
            except NoResultFound:
                raise ThreatReportDoesNotExistsError("Threat report not found")
