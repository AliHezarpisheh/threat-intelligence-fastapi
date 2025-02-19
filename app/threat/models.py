"""Module containing model definitions for threat reports."""

import json
from typing import Any

from sqlalchemy import Index
from sqlalchemy.orm import Mapped, mapped_column

from app.threat.helpers.enums import ThreatType
from toolkit.database.annotations import str63, str255, text
from toolkit.database.mixins import CommonMixin
from toolkit.database.orm import Base


class ThreatReport(CommonMixin, Base):
    """Represent a threat report in the system."""

    # Table Configuration
    __tablename__ = "threat__threat_report"
    __table_args__ = (
        Index("idx_threat_report_created_at", "created_at"),
        Index("idx_threat_report_modified_at", "modified_at"),
    )

    # Columns
    indicator_type: Mapped[ThreatType] = mapped_column(
        nullable=False,
        comment="Threat indicator type",
    )
    indicator_address: Mapped[str255] = mapped_column(
        nullable=False,
        comment="Threat indicator address",
    )
    full_name: Mapped[str255] = mapped_column(
        nullable=False,
        comment="Full name of the user submitting the report",
    )
    email: Mapped[str255] = mapped_column(
        nullable=False,
        comment="Email of the user submitting the report",
    )
    threat_actor: Mapped[str255] = mapped_column(
        nullable=True,
        comment="The threat actor",
    )
    industry: Mapped[str255] = mapped_column(
        nullable=True,
        comment="The industry",
    )
    tactic: Mapped[str63] = mapped_column(
        nullable=True,
        comment="The threat tactic",
    )
    technique: Mapped[str63] = mapped_column(
        nullable=True,
        comment="The threat technique",
    )
    credibility: Mapped[int] = mapped_column(
        nullable=False,
        comment="The threat credibility",
    )
    attack_logs: Mapped[text] = mapped_column(
        nullable=True,
        comment="The threat attack logs",
    )

    def to_bytes(self) -> bytes:
        """Convert the ThreatReport instance to a JSON bytes object."""

        def serializer(obj: Any) -> str:
            if isinstance(obj, ThreatType):
                return obj.value
            return str(obj)

        threat_dict = self.__dict__
        threat_dict.pop("_sa_instance_state", None)
        json_str = json.dumps(threat_dict, default=serializer)
        return json_str.encode("utf-8")

    def __str__(self) -> str:
        """Return a string representation of the `ThreatReport` object."""
        return (
            f"<ThreatReport(id={self.id}, indicator_type={self.indicator_type}, "
            f"indicator_address={self.indicator_address}, full_name={self.full_name})>"
        )

    def __repr__(self) -> str:
        """Return a human-readable string representation of the `ThreatReport` obj."""
        return (
            f"ThreatReport(id={self.id}, indicator_type={self.indicator_type}, "
            f"indicator_address={self.indicator_address}, full_name={self.full_name})"
        )
