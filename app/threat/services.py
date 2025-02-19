"""
Module for threat service operations.

This module provides a service class for handling various threat-related operations.
"""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.threat.dal import ThreatReportDataAccessLayer
from app.threat.helpers.messages import ThreatReportMessage
from app.threat.producer import ThreatReportProducer
from app.threat.schemas import ThreatReportInputSchema
from config.base import logger, rabbitmq_manager
from toolkit.api.enums import HTTPStatusDoc, Status


class ThreatReportService:
    """Service class for threat-report-related operations."""

    def __init__(self, db_session: async_scoped_session[AsyncSession]) -> None:
        """
        Initialize the `ThreatReportService`.

        Parameters
        ----------
        db_session : async_scoped_session[AsyncSession]
            The database session for asynchronous operations.
        """
        self.db_session = db_session
        self.threat_report_dal = ThreatReportDataAccessLayer(db_session=db_session)
        self.threat_report_producer = ThreatReportProducer(
            rabbitmq_manager=rabbitmq_manager
        )

    async def create_threat_and_notify_threat_report(
        self, threat_report_input: ThreatReportInputSchema
    ) -> dict[str, Any]:
        """
        Create a new threat report and notify via RabbitMQ.

        This method handles the creation of a new threat report in the database and
        sends a notification to RabbitMQ with the details of the new report.

        Parameters
        ----------
        threat_report_input : ThreatReportInputSchema
            The input data required for creating a new threat report.

        Returns
        -------
        dict[str, Any]
            A dictionary containing the status, message, created threat report data,
            and a documentation link.
        """
        created_threat_report = await self.threat_report_dal.create_threat_report(
            threat_report_input=threat_report_input
        )

        try:
            await self.threat_report_producer.produce_new_threat_report(
                threat_report=created_threat_report
            )
        except Exception:
            logger.error(
                "Failed to send new threat report to rabbitmq exchange. "
                "Threat report: %s",
                str(created_threat_report),
                exc_info=True,
            )

        return {
            "status": Status.CREATED,
            "message": ThreatReportMessage.SUCCESSFUL_CREATION.value,
            "data": created_threat_report,
            "documentationLink": HTTPStatusDoc.HTTP_STATUS_201,
        }

    async def get_threat_report(self, threat_report_id: int) -> dict[str, Any]:
        """
        Retrieve a threat report by its ID.

        This method fetches the threat report from the database based on the provided
        threat report ID.

        Parameters
        ----------
        threat_report_id : int
            The ID of the threat report to retrieve.

        Returns
        -------
        dict[str, Any]
            A dictionary containing the status, message, retrieved threat report data,
            and a documentation link.
        """
        retrieved_threat_report = await self.threat_report_dal.get_threat_report(
            threat_report_id=threat_report_id
        )
        return {
            "status": Status.SUCCESS,
            "message": ThreatReportMessage.SUCCESSFUL_RETRIEVAL,
            "data": retrieved_threat_report,
            "documentationLink": HTTPStatusDoc.HTTP_STATUS_200,
        }
