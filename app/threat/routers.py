"""Module defines routers related to threat."""

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Path, status

from app.auth.security import verify_token_dependency
from app.threat.dependencies import get_threat_report_service
from app.threat.schemas import ThreatReportInputSchema, ThreatReportOutputSchema
from app.threat.services import ThreatReportService
from toolkit.api.enums import OpenAPITags

router = APIRouter(
    prefix="/threats",
    tags=[OpenAPITags.THREAT_REPORTS],
    dependencies=[Depends(verify_token_dependency)],
)


@router.post(
    "/reports",
    status_code=status.HTTP_201_CREATED,
    response_model=ThreatReportOutputSchema,
)
async def create_threat_report(
    threat_report_input: ThreatReportInputSchema,
    threat_report_service: Annotated[
        ThreatReportService, Depends(get_threat_report_service)
    ],
) -> dict[str, Any]:
    """
    Create a new threat report based on the provided details.

    \f
    Parameters
    ----------
    threat_report_input : ThreatReportInputSchema
        A Pydantic schema containing the threat report details.
    threat_report_service : ThreatReportService
        A service dependency for handling threat report operations.

    Returns
    -------
    dict
        A dictionary containing the status, message, and created threat report data.

    Notes
    -----
    The system will process the threat report and notify relevant entities.
    """
    return await threat_report_service.create_threat_and_notify_threat_report(
        threat_report_input=threat_report_input
    )


@router.get(
    "/reports/{threat_report_id}",
    status_code=status.HTTP_200_OK,
    response_model=ThreatReportOutputSchema,
)
async def get_threat_report(
    threat_report_id: Annotated[int, Path()],
    threat_report_service: Annotated[
        ThreatReportService, Depends(get_threat_report_service)
    ],
) -> dict[str, Any]:
    """
    Retrieve a threat report by its unique identifier.

    This endpoint fetches details of a specific threat report using its ID.

    - **threat_report_id**: The unique identifier of the threat report.
    \f
    Parameters
    ----------
    threat_report_id : int
        The ID of the threat report to retrieve.
    threat_report_service : ThreatReportService
        A service dependency for handling threat report retrieval.

    Returns
    -------
    dict
        A dictionary containing the status, message, and threat report details.

    Notes
    -----
    Ensure the provided threat report ID exists before calling this endpoint.
    """
    return await threat_report_service.get_threat_report(
        threat_report_id=threat_report_id
    )
