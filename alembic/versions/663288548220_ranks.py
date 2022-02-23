"""ranks

Revision ID: 663288548220
Revises: 5a4750e0441e
Create Date: 2022-02-23 15:49:48.869793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '663288548220'
down_revision = '5a4750e0441e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('rank', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'rank')
    # ### end Alembic commands ###
