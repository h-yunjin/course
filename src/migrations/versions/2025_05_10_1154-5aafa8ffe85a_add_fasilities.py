"""add_fasilities

Revision ID: 5aafa8ffe85a
Revises: d52ab3e3101b
Create Date: 2025-05-10 11:54:50.514551

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "5aafa8ffe85a"
down_revision: Union[str, None] = "d52ab3e3101b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "servises",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "servises_rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("room_id", sa.Integer(), nullable=False),
        sa.Column("servise_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["room_id"],
            ["rooms.id"],
        ),
        sa.ForeignKeyConstraint(
            ["servise_id"],
            ["servises.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("servises_rooms")
    op.drop_table("servises")
