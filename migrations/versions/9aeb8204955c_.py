"""empty message

Revision ID: 9aeb8204955c
Revises: 207990557251
Create Date: 2021-03-16 01:15:32.223725

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9aeb8204955c'
down_revision = '207990557251'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_movie', sa.Column('video_duration', sa.Integer(), nullable=True))
    op.add_column('user_series', sa.Column('video_duration', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_series', 'video_duration')
    op.drop_column('user_movie', 'video_duration')
    # ### end Alembic commands ###
