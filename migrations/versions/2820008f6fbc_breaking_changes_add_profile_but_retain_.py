"""Breaking changes, add profile, but retain user table

Revision ID: 2820008f6fbc
Revises: b4d49e33f07c
Create Date: 2023-05-25 22:28:13.809258

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '2820008f6fbc'
down_revision = 'b4d49e33f07c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profile', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('profile', sa.Column('created_timestamp', sa.DateTime(), nullable=True))
    op.add_column('profile', sa.Column('updated_timestamp', sa.DateTime(), nullable=True))
    op.create_foreign_key(None, 'profile', 'user', ['user_id'], ['id'])
    op.drop_column('user', 'status')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'profile', type_='foreignkey')
    op.drop_column('profile', 'updated_timestamp')
    op.drop_column('profile', 'created_timestamp')
    op.drop_column('profile', 'user_id')
    # ### end Alembic commands ###