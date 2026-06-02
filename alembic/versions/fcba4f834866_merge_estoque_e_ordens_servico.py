"""merge estoque e ordens servico

Revision ID: fcba4f834866
Revises: 202605310001, abc50fa4e7ae
Create Date: 2026-06-01 21:44:35.854554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fcba4f834866'
down_revision: Union[str, Sequence[str], None] = ('202605310001', 'abc50fa4e7ae')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass