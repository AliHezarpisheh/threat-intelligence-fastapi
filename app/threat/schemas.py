"""Module defines schemas for threat-related objects."""

from typing import Annotated

from pydantic import EmailStr, Field

from app.threat.helpers.enums import ThreatType
from toolkit.api.enums import HTTPStatusDoc, Status
from toolkit.api.schemas.base import BaseSchema
from toolkit.api.schemas.mixins import CommonMixins


class ThreatReportInputSchema(BaseSchema):
    """Pydantic schema for threat report input validation."""

    indicator_type: Annotated[ThreatType, Field(description="Threat indicator type")]
    indicator_address: Annotated[
        str, Field(max_length=255, description="Threat indicator address")
    ]
    full_name: Annotated[
        str,
        Field(
            max_length=255, description="Full name of the user submitting the report"
        ),
    ]
    email: Annotated[
        EmailStr,
        Field(max_length=255, description="Email of the user submitting the report"),
    ]
    threat_actor: Annotated[
        str | None, Field(max_length=255, description="The threat actor")
    ] = None
    industry: Annotated[
        str | None, Field(max_length=255, description="The industry")
    ] = None
    tactic: Annotated[
        str | None, Field(max_length=63, description="The threat tactic")
    ] = None
    technique: Annotated[
        str | None,
        Field(max_length=63, description="The threat technique"),
    ] = None
    credibility: Annotated[int, Field(description="The threat credibility")]
    attack_logs: Annotated[str | None, Field(description="The threat attack logs")] = (
        None
    )


class ThreatReportData(CommonMixins, BaseSchema):
    """Pydantic schema for the threat report data in the response."""

    indicator_type: Annotated[ThreatType, Field(description="Threat indicator type")]
    indicator_address: Annotated[str, Field(description="Threat indicator address")]
    full_name: Annotated[
        str, Field(description="Full name of the user submitting the report")
    ]
    email: Annotated[str, Field(description="Email of the user submitting the report")]
    threat_actor: Annotated[str | None, Field(description="The threat actor")]
    industry: Annotated[str | None, Field(description="The industry")]
    tactic: Annotated[str | None, Field(description="The threat tactic")]
    technique: Annotated[str | None, Field(description="The threat technique")]
    credibility: Annotated[int, Field(description="The threat credibility")]
    attack_logs: Annotated[str | None, Field(description="The threat attack logs")]


class ThreatReportOutputSchema(BaseSchema):
    """Pydantic schema for the threat report API response."""

    status: Annotated[Status, Field(description="The status of the operation")]
    message: Annotated[
        str, Field(description="A message describing the result of the operation")
    ]
    data: Annotated[
        ThreatReportData, Field(description="The created threat report data")
    ]
    documentationLink: Annotated[
        HTTPStatusDoc, Field(description="Link to the relevant API documentation")
    ]
