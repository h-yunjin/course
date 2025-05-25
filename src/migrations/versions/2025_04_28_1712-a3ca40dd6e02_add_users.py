"""add_users

Revision ID: a3ca40dd6e02
Revises: dba36b049358
Create Date: 2025-04-28 17:12:40.869572

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a3ca40dd6e02"
down_revision: Union[str, None] = "dba36b049358"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
