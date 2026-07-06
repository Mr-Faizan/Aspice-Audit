"""Refine auditquestion table and fix auditoption weight constraint

Revision ID: a2b3c4d5e6f7
Revises: f1a2b3c4d5e6
Create Date: 2026-06-29 00:01:00.000000

Changes:
- auditquestion: add base_practice_id, add is_active, drop criteria, drop identifies
- auditoption: fix weight check constraint from <= 5 to <= 4

"""
from alembic import op
import sqlalchemy as sa

revision = 'a2b3c4d5e6f7'
down_revision = 'f1a2b3c4d5e6'
branch_labels = None
depends_on = None


def upgrade():
    # --- auditquestion ---
    # Add base_practice_id (nullable first so existing rows are safe)
    op.add_column('auditquestion', sa.Column('base_practice_id', sa.String(length=50), nullable=True))
    op.execute("UPDATE auditquestion SET base_practice_id = '' WHERE base_practice_id IS NULL")
    op.alter_column('auditquestion', 'base_practice_id', nullable=False)

    # Add is_active with server default so existing rows get TRUE
    op.add_column('auditquestion', sa.Column(
        'is_active', sa.Boolean(), nullable=False, server_default=sa.true()
    ))

    # Drop the old columns that are consolidated into question_text
    op.drop_column('auditquestion', 'criteria')
    op.drop_column('auditquestion', 'identifies')

    # --- auditoption: clamp any weight=5 rows, then fix check constraint ---
    op.execute('UPDATE auditoption SET weight = 4 WHERE weight > 4')
    op.drop_constraint('ck_auditoption_weight_range', 'auditoption', type_='check')
    op.create_check_constraint(
        'ck_auditoption_weight_range',
        'auditoption',
        'weight >= 0 AND weight <= 4',
    )


def downgrade():
    # Restore auditoption constraint
    op.drop_constraint('ck_auditoption_weight_range', 'auditoption', type_='check')
    op.create_check_constraint(
        'ck_auditoption_weight_range',
        'auditoption',
        'weight >= 0 AND weight <= 5',
    )

    # Restore auditquestion columns
    op.add_column('auditquestion', sa.Column('criteria', sa.String(length=500), nullable=True))
    op.add_column('auditquestion', sa.Column('identifies', sa.String(length=500), nullable=True))
    op.drop_column('auditquestion', 'is_active')
    op.drop_column('auditquestion', 'base_practice_id')
