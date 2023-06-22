"""Breaking changes, add profile, but retain user table

Revision ID: 8b2d99fac8ab
Revises: 2820008f6fbc
Create Date: 2023-05-25 22:38:33.926984

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '8b2d99fac8ab'
down_revision = '2820008f6fbc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('business', sa.Column('profile_id', sa.Integer(), nullable=True))
    op.drop_constraint('business_user_id_fkey', 'business', type_='foreignkey')
    op.create_foreign_key(None, 'business', 'profile', ['profile_id'], ['id'])
    op.drop_column('business', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('business', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'business', type_='foreignkey')
    op.create_foreign_key('business_user_id_fkey', 'business', 'user', ['user_id'], ['id'])
    op.drop_column('business', 'profile_id')
    # ### end Alembic commands ###
