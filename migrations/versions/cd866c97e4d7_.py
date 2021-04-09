"""empty message

Revision ID: cd866c97e4d7
Revises: a9f8593bb896
Create Date: 2021-03-06 22:34:47.325593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd866c97e4d7'
down_revision = 'a9f8593bb896'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('movies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('added', sa.DateTime(), nullable=False),
    sa.Column('img', sa.String(length=30), nullable=True),
    sa.Column('year', sa.String(length=11), nullable=True),
    sa.Column('description', sa.String(length=300), nullable=True),
    sa.Column('FWmark', sa.String(length=5), nullable=True),
    sa.Column('IMDBmark', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('series',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=80), nullable=False),
    sa.Column('added', sa.DateTime(), nullable=False),
    sa.Column('img', sa.String(length=30), nullable=True),
    sa.Column('year', sa.String(length=11), nullable=True),
    sa.Column('description', sa.String(length=300), nullable=True),
    sa.Column('FWmark', sa.String(length=5), nullable=True),
    sa.Column('IMDBmark', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('picture', sa.String(length=10), nullable=True),
    sa.Column('enabled', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('movie_category',
    sa.Column('movie_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['movie_id'], ['movies.id'], )
    )
    op.create_table('seasons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('series_id', sa.Integer(), nullable=True),
    sa.Column('season', sa.Integer(), nullable=True),
    sa.Column('episodes', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['series_id'], ['series.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('series_category',
    sa.Column('series_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ),
    sa.ForeignKeyConstraint(['series_id'], ['series.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('series_category')
    op.drop_table('seasons')
    op.drop_table('movie_category')
    op.drop_table('users')
    op.drop_table('series')
    op.drop_table('movies')
    op.drop_table('categories')
    # ### end Alembic commands ###
