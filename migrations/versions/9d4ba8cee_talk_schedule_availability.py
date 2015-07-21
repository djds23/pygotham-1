"""Talk schedule availability

Revision ID: 9d4ba8cee
Revises: 254d12951cf
Create Date: 2015-07-21 22:55:02.731945

"""

# revision identifiers, used by Alembic.
revision = '9d4ba8cee'
down_revision = '254d12951cf'

from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('talk_schedule_begins', sqlalchemy_utils.types.arrow.ArrowType(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', 'talk_schedule_begins')
    ### end Alembic commands ###
