"""v1.0.1

Revision ID: 9cca611b2e3c
Revises: db90f452c4f7
Create Date: 2024-03-26 17:09:10.860734

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cca611b2e3c'
down_revision = 'db90f452c4f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pbInterfaceInvokeLog', sa.Column('tStartTime', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('pbInterfaceInvokeLog', 'tStartTime')
    # ### end Alembic commands ###
