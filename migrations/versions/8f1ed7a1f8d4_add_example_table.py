"""Add example table

Revision ID: 8f1ed7a1f8d4
Revises:
Create Date: 2023-04-02 12:04:24.659393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8f1ed7a1f8d4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "example",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("col1", sa.String(), nullable=False),
        sa.Column("col2", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_example")),
    )
    op.create_index(op.f("ix_example_col1"), "example", ["col1"], unique=True)
    op.create_index(op.f("ix_example_id"), "example", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_example_id"), table_name="example")
    op.drop_index(op.f("ix_example_col1"), table_name="example")
    op.drop_table("example")
    # ### end Alembic commands ###
