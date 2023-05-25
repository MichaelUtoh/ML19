"""Add reviews to user model

Revision ID: b4d49e33f07c
Revises: 4d08252fb575
Create Date: 2023-05-25 22:06:02.583289

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'b4d49e33f07c'
down_revision = '4d08252fb575'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('review', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('review_author_id_fkey', 'review', type_='foreignkey')
    op.create_foreign_key(None, 'review', 'user', ['user_id'], ['id'])
    op.drop_column('review', 'author_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('review', sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'review', type_='foreignkey')
    op.create_foreign_key('review_author_id_fkey', 'review', 'user', ['author_id'], ['id'])
    op.drop_column('review', 'user_id')
    # ### end Alembic commands ###