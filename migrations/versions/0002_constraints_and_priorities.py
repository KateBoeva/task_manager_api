"""unique names, task indexes, default priorities

Revision ID: 0002
Revises: 0001
Create Date: 2026-11-08

"""
from typing import Sequence, Union

from alembic import op


revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint("uq_status_name", "status", ["name"])
    op.create_unique_constraint("uq_priority_name", "priority", ["name"])
    op.create_index("ix_task_status_id", "task", ["status_id"])
    op.create_index("ix_task_priority_id", "task", ["priority_id"])

    op.execute("INSERT INTO priority (name) VALUES ('Low'), ('Medium'), ('High') ON CONFLICT (name) DO NOTHING")


def downgrade() -> None:
    op.drop_index("ix_task_priority_id", table_name="task")
    op.drop_index("ix_task_status_id", table_name="task")
    op.drop_constraint("uq_priority_name", "priority", type_="unique")
    op.drop_constraint("uq_status_name", "status", type_="unique")
