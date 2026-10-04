"""add recipe scale dimensions

Revision ID: 8f4c2a1d9b70
Revises: 27621d27c7e1
Create Date: 2026-10-03 22:00:00.000000

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "8f4c2a1d9b70"
down_revision: str | None = "27621d27c7e1"
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade():
    with op.batch_alter_table("recipes", schema=None) as batch_op:
        batch_op.add_column(sa.Column("recipe_scale_basis", sa.String(), nullable=False, server_default="servings"))
        batch_op.add_column(sa.Column("recipe_scale_unit", sa.String(), nullable=False, server_default="in"))
        batch_op.add_column(sa.Column("recipe_scale_base_length", sa.Float(), nullable=False, server_default="0"))
        batch_op.add_column(sa.Column("recipe_scale_base_width", sa.Float(), nullable=False, server_default="0"))


def downgrade():
    with op.batch_alter_table("recipes", schema=None) as batch_op:
        batch_op.drop_column("recipe_scale_base_width")
        batch_op.drop_column("recipe_scale_base_length")
        batch_op.drop_column("recipe_scale_unit")
        batch_op.drop_column("recipe_scale_basis")
