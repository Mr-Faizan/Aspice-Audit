"""Create auditsession, auditresponse, weaknessresult, banditarmstate tables

Revision ID: b3c4d5e6f7a8
Revises: a2b3c4d5e6f7
Create Date: 2026-06-29 00:02:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'b3c4d5e6f7a8'
down_revision = 'a2b3c4d5e6f7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'auditsession',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='in_progress'),
        sa.Column('questions_asked', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('max_questions', sa.Integer(), nullable=False, server_default='12'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'auditresponse',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('session_id', sa.UUID(), nullable=False),
        sa.Column('question_id', sa.UUID(), nullable=False),
        sa.Column('option_id', sa.UUID(), nullable=False),
        sa.Column('answered_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['auditsession.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['question_id'], ['auditquestion.id']),
        sa.ForeignKeyConstraint(['option_id'], ['auditoption.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'weaknessresult',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('session_id', sa.UUID(), nullable=False),
        sa.Column('scores', sa.JSON(), nullable=False, server_default='{}'),
        sa.Column('top_weaknesses', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('computed_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['auditsession.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_id', name='uq_weaknessresult_session_id'),
    )

    op.create_table(
        'banditarmstate',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('question_id', sa.UUID(), nullable=False),
        sa.Column('A_matrix', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('b_vector', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('pull_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('total_reward', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['question_id'], ['auditquestion.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('question_id', name='uq_banditarmstate_question_id'),
    )


def downgrade():
    op.drop_table('banditarmstate')
    op.drop_table('weaknessresult')
    op.drop_table('auditresponse')
    op.drop_table('auditsession')
