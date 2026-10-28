"""merge dimension scaling and upstream migrations

Revision ID: 19afd47c9e25
Revises: 8f4c2a1d9b70, a9f823e9e441
Create Date: 2026-10-27 22:31:01.377316

"""

# revision identifiers, used by Alembic.
revision = "19afd47c9e25"
down_revision: tuple[str, str] = ("8f4c2a1d9b70", "a9f823e9e441")
branch_labels: str | tuple[str, ...] | None = None
depends_on: str | tuple[str, ...] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
