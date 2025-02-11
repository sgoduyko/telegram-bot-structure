"""empty message

Revision ID: 9fda3598a3ee
Revises:
Create Date: 2025-02-02 19:08:32.240220

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9fda3598a3ee"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("username", sa.String(length=15), nullable=False),
        sa.Column("pincode", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("username"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user")
    # ### end Alembic commands ###
