"""Add reviews to user model

Revision ID: 4d08252fb575
Revises: e535d611e2b0
Create Date: 2023-05-25 21:50:09.917717

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '4d08252fb575'
down_revision = 'e535d611e2b0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('review', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'review', 'user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'review', type_='foreignkey')
    op.drop_column('review', 'author_id')
    # ### end Alembic commands ###