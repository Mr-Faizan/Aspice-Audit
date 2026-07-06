"""Drop quiz, question, quizattempt tables

Revision ID: c4d5e6f7a8b9
Revises: b3c4d5e6f7a8
Create Date: 2026-06-29 00:03:00.000000

These tables were defined in models.py but never formally migrated.
The DROP uses IF EXISTS so the migration is safe either way.

"""
from alembic import op

revision = 'c4d5e6f7a8b9'
down_revision = 'b3c4d5e6f7a8'
branch_labels = None
depends_on = None


def upgrade():
    # Drop dependents before parents
    op.execute('DROP TABLE IF EXISTS quizattempt CASCADE')
    op.execute('DROP TABLE IF EXISTS question CASCADE')
    op.execute('DROP TABLE IF EXISTS quiz CASCADE')


def downgrade():
    # Quiz tables are intentionally removed — no restore on downgrade
    pass
