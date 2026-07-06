"""Use integer PKs for user, auditquestion, auditoption tables

Revision ID: d5e6f7a8b9c0
Revises: c4d5e6f7a8b9
Create Date: 2026-06-29 00:04:00.000000

Replaces UUID PKs with auto-increment integers on the three master-data tables.
All dependent tables are dropped and recreated with the updated FK types.
NOTE: all existing data in these tables is lost — re-seed after this migration.

"""
from alembic import op
import sqlalchemy as sa

revision = 'd5e6f7a8b9c0'
down_revision = 'c4d5e6f7a8b9'
branch_labels = None
depends_on = None


def upgrade():
    # ---- Drop everything that references the three tables (leaf → root) ----
    op.drop_table('banditarmstate')
    op.drop_table('weaknessresult')
    op.drop_table('auditresponse')
    op.drop_table('auditsession')
    op.drop_table('auditoption')
    op.drop_table('auditquestion')
    op.drop_table('item')
    op.drop_table('user')

    # ---- Recreate user with SERIAL PK ----
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column('full_name', sa.String(length=255), nullable=True),
        sa.Column('stakeholder_role', sa.String(length=50), nullable=False, server_default='software_developer'),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_login_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)

    # ---- Recreate item with integer FK to user ----
    op.create_table(
        'item',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    # ---- Recreate auditquestion with SERIAL PK ----
    op.create_table(
        'auditquestion',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('question_code', sa.String(length=50), nullable=False),
        sa.Column('base_practice_id', sa.String(length=50), nullable=False),
        sa.Column('process', sa.String(length=20), nullable=False),
        sa.Column('level', sa.String(length=5), nullable=False),
        sa.Column('stakeholders', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('question_text', sa.String(length=2048), nullable=False),
        sa.Column('recommendation_logic', sa.String(length=2048), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('question_code'),
    )
    op.create_index('ix_auditquestion_question_code', 'auditquestion', ['question_code'])

    # ---- Recreate auditoption with integer PK and FK ----
    op.create_table(
        'auditoption',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('label', sa.String(length=5), nullable=False),
        sa.Column('option_text', sa.String(length=1000), nullable=False),
        sa.Column('weight', sa.Integer(), nullable=False, server_default='0'),
        sa.ForeignKeyConstraint(['question_id'], ['auditquestion.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('weight >= 0 AND weight <= 4', name='ck_auditoption_weight_range'),
    )

    # ---- Recreate auditsession with integer FK to user ----
    op.create_table(
        'auditsession',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='in_progress'),
        sa.Column('questions_asked', sa.JSON(), nullable=False, server_default='[]'),
        sa.Column('max_questions', sa.Integer(), nullable=False, server_default='12'),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    # ---- Recreate auditresponse with integer FKs to question/option ----
    op.create_table(
        'auditresponse',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('session_id', sa.UUID(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('option_id', sa.Integer(), nullable=False),
        sa.Column('answered_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['session_id'], ['auditsession.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['question_id'], ['auditquestion.id']),
        sa.ForeignKeyConstraint(['option_id'], ['auditoption.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    # ---- Recreate weaknessresult (no FK type changes) ----
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

    # ---- Recreate banditarmstate with integer FK to auditquestion ----
    op.create_table(
        'banditarmstate',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
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
    # Reverting to UUID PKs is complex; not supported.
    # To go back, restore from backup or rerun migrations from scratch.
    pass
