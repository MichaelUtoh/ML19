"""Tweak model to fix business id issue

Revision ID: 5791ed4822d5
Revises: 584a52d6a9d4
Create Date: 2023-05-12 00:11:30.623807

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "5791ed4822d5"
down_revision = "584a52d6a9d4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
