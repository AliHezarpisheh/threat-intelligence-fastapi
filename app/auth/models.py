"""Module containing model definitions for user."""

from sqlalchemy import Index, sql
from sqlalchemy.orm import Mapped, mapped_column

from toolkit.database.annotations import str255
from toolkit.database.mixins import CommonMixin
from toolkit.database.orm import Base


class User(CommonMixin, Base):
    """Represents a user in the authentication system."""

    # Table Configurations
    __tablename__ = "auth__user"
    __table_args__ = (
        Index("ix_user_username", "username"),
        Index("ix_user_email", "email"),
    )

    # Columns
    username: Mapped[str255] = mapped_column(
        unique=True,
        nullable=False,
        comment="Unique username.",
    )
    email: Mapped[str255] = mapped_column(
        unique=True,
        nullable=False,
        comment="Unique email address.",
    )
    hashed_password: Mapped[str] = mapped_column(
        nullable=False, comment="Hashed password."
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=True,
        default=True,
        server_default=sql.false(),
        comment="Indicates if the user is active",
    )

    def __str__(self) -> str:
        """Return a string representation of the User object."""
        return (
            f"<User(username={self.username}, email={self.email}, "
            f"is_active={self.is_active})>"
        )

    def __repr__(self) -> str:
        """Return a human-readable string representation of the User object."""
        return (
            f"User(username={self.username}, email={self.email}, "
            f"is_active={self.is_active})"
        )
