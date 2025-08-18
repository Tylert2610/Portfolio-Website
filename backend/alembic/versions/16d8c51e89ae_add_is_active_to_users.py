"""add_is_active_to_users

Revision ID: 16d8c51e89ae
Revises: b8e2ae3ac837
Create Date: 2025-08-17 15:19:12.919378

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "16d8c51e89ae"
down_revision: Union[str, Sequence[str], None] = "b8e2ae3ac837"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add is_active column to users table
    op.add_column(
        "users",
        sa.Column("is_active", sa.Boolean(), nullable=True, server_default="true"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove is_active column from users table
    op.drop_column("users", "is_active")
