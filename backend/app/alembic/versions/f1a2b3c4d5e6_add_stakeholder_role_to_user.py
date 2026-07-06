"""Add stakeholder_role to user table

Revision ID: f1a2b3c4d5e6
Revises: c9e4f1b2d3a7
Create Date: 2026-06-29 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'f1a2b3c4d5e6'
down_revision = 'c9e4f1b2d3a7'
branch_labels = None
depends_on = None


def upgrade():
    # Add as nullable first so existing rows don't violate NOT NULL
    op.add_column('user', sa.Column(
        'stakeholder_role', sa.String(length=50), nullable=True
    ))
    op.execute("UPDATE \"user\" SET stakeholder_role = 'software_developer' WHERE stakeholder_role IS NULL")
    op.alter_column('user', 'stakeholder_role', nullable=False)


def downgrade():
    op.drop_column('user', 'stakeholder_role')
