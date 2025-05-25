"""add_users_unuque

Revision ID: a868fb886eef
Revises: a3ca40dd6e02
Create Date: 2025-04-29 15:04:54.894578

"""

from typing import Sequence, Union

from alembic import op


revision: str = "a868fb886eef"
down_revision: Union[str, None] = "a3ca40dd6e02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
