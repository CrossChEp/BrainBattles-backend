"""scores

Revision ID: 5a4750e0441e
Revises: 659786a75803
Create Date: 2022-02-22 14:27:05.876949

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5a4750e0441e'
down_revision = '659786a75803'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('scores', sa.Float(), nullable=True))
    op.add_column('users', sa.Column('scores', sa.Float(), nullable=True))
    op.add_column('games', sa.Column('task', sa.Integer(), nullable=True))
    sa.ForeignKeyConstraint(['task'], ['tasks.id'], ),
    sa.PrimaryKeyConstraint('id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'scores')
    op.drop_column('tasks', 'scores')
    # ### end Alembic commands ###
