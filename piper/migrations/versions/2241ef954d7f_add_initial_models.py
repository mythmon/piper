"""Add initial models

Revision ID: 2241ef954d7f
Revises: None
Create Date: 2013-07-06 19:02:12.980884

"""

revision = '2241ef954d7f'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
        'category',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['parent_id'], ['category.id']),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'transaction',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('merchant', sa.String(length=128), nullable=True),
        sa.Column('purchase_date', sa.DateTime(), nullable=False),
        sa.Column('created', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'split',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('note', sa.String(length=512), nullable=True),
        sa.Column('transaction_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['transaction_id'], ['transaction.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'association',
        sa.Column('split_id', sa.Integer(), nullable=False),
        sa.Column('category_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
        sa.ForeignKeyConstraint(['split_id'], ['split.id'], ),
        sa.PrimaryKeyConstraint()
    )


def downgrade():
    op.drop_table('association')
    op.drop_table('split')
    op.drop_table('transaction')
    op.drop_table('category')
