"""staging_update

Revision ID: 148b41da137a
Revises: 663288548220
Create Date: 2022-02-23 17:41:09.020709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '148b41da137a'
down_revision = '663288548220'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('staging', sa.Column('rank', sa.String(), nullable=True))
    op.add_column('staging', sa.Column('subject', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('staging', 'subject')
    op.drop_column('staging', 'rank')
    # ### end Alembic commands ###