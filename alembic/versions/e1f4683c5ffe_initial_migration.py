"""Initial migration

Revision ID: e1f4683c5ffe
Revises: 
Create Date: 2026-07-01 23:47:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSON

# revision identifiers, used by Alembic.
revision = 'e1f4683c5ffe'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=True),
        sa.Column('role', sa.String(length=20), server_default='user', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_id', 'users', ['id'])
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Categories table
    op.create_table('categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('icon', sa.String(length=50), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_categories_id', 'categories', ['id'])
    op.create_index('ix_categories_name', 'categories', ['name'], unique=True)

    # Templates table
    op.create_table('templates',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('content', JSON, nullable=False),
        sa.Column('version', sa.Integer(), server_default='1', nullable=True),
        sa.Column('is_public', sa.Boolean(), server_default='true', nullable=True),
        sa.Column('view_count', sa.Integer(), server_default='0', nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('share_token', sa.String(length=100), nullable=True),
        sa.Column('share_created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('share_views', sa.Integer(), server_default='0', nullable=True),
        sa.Column('share_expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_templates_id', 'templates', ['id'])
    op.create_index('ix_templates_title', 'templates', ['title'])
    op.create_index('ix_templates_category', 'templates', ['category'])
    op.create_index('ix_templates_share_token', 'templates', ['share_token'], unique=True)

    # Template versions table
    op.create_table('template_versions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('content', JSON, nullable=False),
        sa.Column('changes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('created_by', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['template_id'], ['templates.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_template_versions_id', 'template_versions', ['id'])

    # User activities table
    op.create_table('user_activities',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['template_id'], ['templates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_activities_id', 'user_activities', ['id'])

    # User favourites association table
    op.create_table('user_favourites',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('template_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['template_id'], ['templates.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'template_id')
    )

    # User preferences table
    op.create_table('user_preferences',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('theme', sa.String(length=20), server_default='light', nullable=True),
        sa.Column('language', sa.String(length=10), server_default='en', nullable=True),
        sa.Column('notifications_enabled', sa.Boolean(), server_default='true', nullable=True),
        sa.Column('email_frequency', sa.String(length=20), server_default='daily', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index('ix_user_preferences_id', 'user_preferences', ['id'])
    op.create_index('ix_user_preferences_user_id', 'user_preferences', ['user_id'], unique=True)

def downgrade():
    op.drop_index('ix_user_preferences_user_id', table_name='user_preferences')
    op.drop_index('ix_user_preferences_id', table_name='user_preferences')
    op.drop_table('user_preferences')
    op.drop_table('user_favourites')
    op.drop_index('ix_user_activities_id', table_name='user_activities')
    op.drop_table('user_activities')
    op.drop_index('ix_template_versions_id', table_name='template_versions')
    op.drop_table('template_versions')
    op.drop_index('ix_templates_share_token', table_name='templates')
    op.drop_index('ix_templates_category', table_name='templates')
    op.drop_index('ix_templates_title', table_name='templates')
    op.drop_index('ix_templates_id', table_name='templates')
    op.drop_table('templates')
    op.drop_index('ix_categories_name', table_name='categories')
    op.drop_index('ix_categories_id', table_name='categories')
    op.drop_table('categories')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_index('ix_users_id', table_name='users')
    op.drop_table('users')