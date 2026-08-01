"""Add template_count column to categories

Revision ID: [will be auto-generated]
Revises: d06268db54ba
Create Date: [will be auto-generated]

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '56237a6b04b8'  # ← This will be generated
down_revision = 'd06268db54ba'
branch_labels = None
depends_on = None


def upgrade():
    # Only add the column, don't touch anything else
    op.add_column('categories', sa.Column('template_count', sa.Integer(), nullable=True, server_default='0'))


def downgrade():
    op.drop_column('categories', 'template_count')