"""Module defines exceptions related to threat."""

from toolkit.api.exceptions import DoesNotExistError


class ThreatReportDoesNotExistsError(DoesNotExistError):
    """Exception raised when a requested threat report is not found."""
