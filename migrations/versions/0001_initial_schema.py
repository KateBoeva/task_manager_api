"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-11-08

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "status",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=30), nullable=False),
        if_not_exists=True,
    )
    op.create_table(
        "priority",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=30), nullable=False),
        if_not_exists=True,
    )
    op.create_table(
        "task",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("status_id", sa.Integer(), sa.ForeignKey("status.id"), nullable=False),
        sa.Column("priority_id", sa.Integer(), sa.ForeignKey("priority.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        if_not_exists=True,
    )


def downgrade() -> None:
    op.drop_table("task")
    op.drop_table("priority")
    op.drop_table("status")
