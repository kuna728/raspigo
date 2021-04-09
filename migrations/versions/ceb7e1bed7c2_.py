"""empty message

Revision ID: ceb7e1bed7c2
Revises: 7098b8533cbf
Create Date: 2021-03-13 20:56:32.768354

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ceb7e1bed7c2'
down_revision = '7098b8533cbf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_seasons', sa.Column('episode', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_seasons', 'episode')
    # ### end Alembic commands ###