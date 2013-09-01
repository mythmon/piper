"""
Add budget date ranges

Revision ID: 10e51200afdb
Revises: b39487773fe
Create Date: 2013-09-01 10:58:22.066759
"""

from alembic import op
import sqlalchemy as sa


revision = '10e51200afdb'
down_revision = 'b39487773fe'


def upgrade():
    op.add_column('budget', sa.Column('start', sa.DateTime(), nullable=True))
    op.add_column('budget', sa.Column('end', sa.DateTime(), nullable=True))


def downgrade():
    op.drop_column('budget', 'start')
    op.drop_column('budget', 'end')
