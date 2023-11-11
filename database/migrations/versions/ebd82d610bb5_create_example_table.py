"""create example table

Revision ID: ebd82d610bb5
Revises:
Create Date: 2022-12-09 11:52:34.577158

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ebd82d610bb5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'examples', sa.Column('id', sa.BIGINT, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False), sa.Column('nick_name', sa.String),
        sa.Column('age', sa.INT),
        sa.Column('created_at', sa.TIMESTAMP, default=datetime.utcnow()),
        sa.Column('updated_at',
                  sa.TIMESTAMP,
                  default=datetime.utcnow(),
                  onupdate=datetime.utcnow()))
    pass


def downgrade() -> None:
    op.drop_table('examples')
