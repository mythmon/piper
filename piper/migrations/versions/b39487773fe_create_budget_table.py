"""
Create budget table

Revision ID: b39487773fe
Revises: fe4a112f66c
Create Date: 2013-08-03 16:27:00.201057
"""

from alembic import op
import sqlalchemy as sa

from piper.utils import DecimalString


revision = 'b39487773fe'
down_revision = 'fe4a112f66c'


def upgrade():
    op.create_table('budget',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(128), nullable=False),
        sa.Column('search', sa.String(length=10240), nullable=False),
        sa.Column('limit', sa.Numeric(precision=15, scale=2), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('budget')