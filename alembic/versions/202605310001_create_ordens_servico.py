"""create ordens servico

Revision ID: 202605310001
Revises: 202605260002
Create Date: 2026-05-31 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "202605310001"
down_revision: str | None = "202605260002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "ordens_servico",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("numero", sa.String(length=20), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column(
            "status",
            sa.Enum("aberta", "em_andamento", "concluida", "cancelada", name="osstatus"),
            nullable=False,
        ),
        sa.Column(
            "priority",
            sa.Enum("baixa", "media", "alta", "urgente", name="ospriority"),
            nullable=False,
        ),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("technician_id", sa.Integer(), nullable=True),
        sa.Column("opened_by_id", sa.Integer(), nullable=False),
        sa.Column("cancellation_reason", sa.Text(), nullable=True),
        sa.Column("assigned_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("closed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"]),
        sa.ForeignKeyConstraint(["opened_by_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["technician_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ordens_servico_id"), "ordens_servico", ["id"], unique=False)
    op.create_index(op.f("ix_ordens_servico_numero"), "ordens_servico", ["numero"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_ordens_servico_numero"), table_name="ordens_servico")
    op.drop_index(op.f("ix_ordens_servico_id"), table_name="ordens_servico")
    op.drop_table("ordens_servico")
