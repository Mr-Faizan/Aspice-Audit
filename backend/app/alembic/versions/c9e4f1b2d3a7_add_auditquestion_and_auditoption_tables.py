"""Add auditquestion and auditoption tables

Revision ID: c9e4f1b2d3a7
Revises: a3c82f1d9e05
Create Date: 2026-05-26 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c9e4f1b2d3a7'
down_revision = 'a3c82f1d9e05'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'auditquestion',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('question_code', sa.String(length=50), nullable=False),
        sa.Column('process', sa.String(length=20), nullable=False),
        sa.Column('level', sa.String(length=5), nullable=False),
        sa.Column('criteria', sa.String(length=500), nullable=False),
        sa.Column('identifies', sa.String(length=500), nullable=False),
        sa.Column('stakeholders', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('question_text', sa.String(length=2048), nullable=False),
        sa.Column('recommendation_logic', sa.String(length=2048), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('question_code'),
    )
    op.create_index('ix_auditquestion_question_code', 'auditquestion', ['question_code'])

    op.create_table(
        'auditoption',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('question_id', sa.UUID(), nullable=False),
        sa.Column('label', sa.String(length=5), nullable=False),
        sa.Column('option_text', sa.String(length=1000), nullable=False),
        sa.Column('weight', sa.Integer(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['question_id'], ['auditquestion.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('weight >= 0 AND weight <= 5', name='ck_auditoption_weight_range'),
    )


def downgrade():
    op.drop_table('auditoption')
    op.drop_index('ix_auditquestion_question_code', table_name='auditquestion')
    op.drop_table('auditquestion')
