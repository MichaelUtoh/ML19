"""Add fk field to business uuid

Revision ID: 34cfd7f05733
Revises: 49cdd47bcb7a
Create Date: 2023-05-12 12:58:56.131638

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = "34cfd7f05733"
down_revision = "49cdd47bcb7a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("business", "id", existing_type=sa.INTEGER(), nullable=True)
    op.alter_column("business", "uuid", existing_type=sa.VARCHAR(), nullable=False)
    op.drop_constraint("product_business_id_fkey", "product", type_="foreignkey")
    op.create_foreign_key(None, "product", "business", ["business_id"], ["uuid"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "product", type_="foreignkey")
    op.create_foreign_key(
        "product_business_id_fkey", "product", "business", ["business_id"], ["id"]
    )
    op.alter_column("business", "uuid", existing_type=sa.VARCHAR(), nullable=True)
    op.alter_column("business", "id", existing_type=sa.INTEGER(), nullable=False)
    # ### end Alembic commands ###
