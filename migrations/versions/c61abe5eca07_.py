"""empty message

Revision ID: c61abe5eca07
Revises: cbc6a8cf23bd
Create Date: 2021-03-14 01:41:12.148170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c61abe5eca07'
down_revision = 'cbc6a8cf23bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_movie',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('watching_datetime', sa.DateTime(), nullable=True),
    sa.Column('watched_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'movie_id')
    )
    op.create_table('user_seasons',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('seasons_id', sa.Integer(), nullable=False),
    sa.Column('watching_datetime', sa.DateTime(), nullable=True),
    sa.Column('watched_time', sa.DateTime(), nullable=True),
    sa.Column('episode', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['seasons_id'], ['seasons.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'seasons_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_seasons')
    op.drop_table('user_movie')
    # ### end Alembic commands ###