"""empty message

Revision ID: 53119f86c67
Revises: f34e9df528
Create Date: 2014-07-04 12:11:41.018911

"""

# revision identifiers, used by Alembic.
revision = '53119f86c67'
down_revision = 'f34e9df528'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('sponsor_levels', sa.Column('cost', sa.String(), nullable=True))
    op.add_column('sponsor_levels', sa.Column('limit', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('sponsor_levels', 'limit')
    op.drop_column('sponsor_levels', 'cost')
    ### end Alembic commands ###