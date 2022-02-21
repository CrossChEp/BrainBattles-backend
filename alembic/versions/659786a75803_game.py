"""game

Revision ID: 659786a75803
Revises: b12bfc27d902
Create Date: 2022-02-21 21:24:49.744502

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '659786a75803'
down_revision = 'b12bfc27d902'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('opponent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('games')
    # ### end Alembic commands ###