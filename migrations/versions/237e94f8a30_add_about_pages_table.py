"""Add about_pages table

Revision ID: 237e94f8a30
Revises: 55a2c1bad7
Create Date: 2015-02-15 23:54:16.509430

"""

# revision identifiers, used by Alembic.
revision = '237e94f8a30'
down_revision = '55a2c1bad7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('about_pages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('slug', sa.String(length=255), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )


def downgrade():
    op.drop_table('about_pages')
