"""add_hotel

Revision ID: 7a1a62a4208f
Revises:
Create Date: 2025-04-22 13:12:38.591364

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7a1a62a4208f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("hotels")
