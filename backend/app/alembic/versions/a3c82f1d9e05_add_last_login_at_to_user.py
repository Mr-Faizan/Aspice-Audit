"""Add last_login_at to User

Revision ID: a3c82f1d9e05
Revises: fe56fa70289e
Create Date: 2026-05-26 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3c82f1d9e05'
down_revision = 'fe56fa70289e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    op.drop_column('user', 'last_login_at')
