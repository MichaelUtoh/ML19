"""added business table

Revision ID: 690087bff275
Revises: 943d8d38edd3
Create Date: 2023-05-01 00:30:16.379131

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '690087bff275'
down_revision = '943d8d38edd3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('state', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('capital', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('business',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('logo', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('open_days', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('location_id', sa.Integer(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('business')
    op.drop_table('location')
    # ### end Alembic commands ###