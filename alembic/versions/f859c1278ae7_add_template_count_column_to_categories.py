"""Add template_count column to categories

Revision ID: f859c1278ae7
Revises: c4db868ea26f
Create Date: 2026-08-01 12:04:10.495533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f859c1278ae7'
down_revision: Union[str, Sequence[str], None] = 'c4db868ea26f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
