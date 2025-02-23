"""Create user and threat_report

Revision ID: 4e54ac34647b
Revises:
Create Date: 2025-02-19 01:41:51.240760

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "4e54ac34647b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "auth__user",
        sa.Column(
            "username",
            sa.String(length=255),
            nullable=False,
            comment="Unique username.",
        ),
        sa.Column(
            "email",
            sa.String(length=255),
            nullable=False,
            comment="Unique email address.",
        ),
        sa.Column(
            "hashed_password", sa.String(), nullable=False, comment="Hashed password."
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("false"),
            nullable=True,
            comment="Indicates if the user is active",
        ),
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            comment="Auto-incrementing primary key",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Timestamp when the record was created",
        ),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            nullable=True,
            comment="Timestamp when the record was last modified",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("username"),
    )
    op.create_index("ix_user_email", "auth__user", ["email"], unique=False)
    op.create_index("ix_user_username", "auth__user", ["username"], unique=False)
    op.create_table(
        "threat__threat_report",
        sa.Column(
            "indicator_type",
            sa.Enum(
                "IP", "EMAIL", "DOMAIN", "FILE", "URL", "USER_AGENT", name="threattype"
            ),
            nullable=False,
            comment="Threat indicator type",
        ),
        sa.Column(
            "indicator_address",
            sa.String(length=255),
            nullable=False,
            comment="Threat indicator address",
        ),
        sa.Column(
            "full_name",
            sa.String(length=255),
            nullable=False,
            comment="Full name of the user submitting the report",
        ),
        sa.Column(
            "email",
            sa.String(length=255),
            nullable=False,
            comment="Email of the user submitting the report",
        ),
        sa.Column(
            "threat_actor",
            sa.String(length=255),
            nullable=True,
            comment="The threat actor",
        ),
        sa.Column(
            "industry", sa.String(length=255), nullable=True, comment="The industry"
        ),
        sa.Column(
            "tactic", sa.String(length=63), nullable=True, comment="The threat tactic"
        ),
        sa.Column(
            "technique",
            sa.String(length=63),
            nullable=True,
            comment="The threat technique",
        ),
        sa.Column(
            "credibility",
            sa.Integer(),
            nullable=False,
            comment="The threat credibility",
        ),
        sa.Column(
            "attack_logs", sa.Text(), nullable=True, comment="The threat attack logs"
        ),
        sa.Column(
            "id",
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            comment="Auto-incrementing primary key",
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
            comment="Timestamp when the record was created",
        ),
        sa.Column(
            "modified_at",
            sa.DateTime(),
            nullable=True,
            comment="Timestamp when the record was last modified",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "idx_threat_report_created_at",
        "threat__threat_report",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        "idx_threat_report_modified_at",
        "threat__threat_report",
        ["modified_at"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("idx_threat_report_modified_at", table_name="threat__threat_report")
    op.drop_index("idx_threat_report_created_at", table_name="threat__threat_report")
    op.drop_table("threat__threat_report")
    op.drop_index("ix_user_username", table_name="auth__user")
    op.drop_index("ix_user_email", table_name="auth__user")
    op.drop_table("auth__user")
    # ### end Alembic commands ###
