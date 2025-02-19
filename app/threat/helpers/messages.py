"""Module defines enumeration classes for threat response messages."""

from enum import StrEnum


class ThreatReportMessage(StrEnum):
    """Enumeration class defining threat report messages."""

    SUCCESSFUL_CREATION = "Threat report have been created successfully"
    SUCCESSFUL_RETRIEVAL = "Threat report have been retrieved successfully"
