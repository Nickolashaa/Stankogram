"""u_attachments_files

Revision ID: a7d3f1c80e52
Revises: c4e1a9f2b730
Create Date: 2026-10-24 00:30:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a7d3f1c80e52"
down_revision: Union[str, Sequence[str], None] = "c4e1a9f2b730"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("ALTER TYPE attachmentkind ADD VALUE IF NOT EXISTS 'FILE'")
    op.alter_column(
        "attachments",
        "thumbnail_key",
        existing_type=sa.String(),
        nullable=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("DELETE FROM attachments WHERE kind = 'FILE'")
    op.alter_column(
        "attachments",
        "thumbnail_key",
        existing_type=sa.String(),
        nullable=False,
    )
    op.execute("ALTER TYPE attachmentkind RENAME TO attachmentkind_old")
    op.execute("CREATE TYPE attachmentkind AS ENUM ('IMAGE', 'VIDEO')")
    op.execute(
        "ALTER TABLE attachments ALTER COLUMN kind TYPE attachmentkind "
        "USING kind::text::attachmentkind"
    )
    op.execute("DROP TYPE attachmentkind_old")
