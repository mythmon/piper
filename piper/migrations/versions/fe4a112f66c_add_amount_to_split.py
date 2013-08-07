"""
Add amount to split

Revision ID: fe4a112f66c
Revises: 2241ef954d7f
Create Date: 2013-07-07 20:01:04.960412
"""

from alembic import op
import sqlalchemy as sa



revision = 'fe4a112f66c'
down_revision = '2241ef954d7f'


def upgrade():
    op.add_column(
        'split',
        sa.Column('amount', sa.Numeric(precision=15, scale=2), nullable=True))


def downgrade():
    op.drop_column('split', 'amount')