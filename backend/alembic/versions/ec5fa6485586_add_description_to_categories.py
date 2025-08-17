"""add_description_to_categories

Revision ID: ec5fa6485586
Revises: 16d8c51e89ae
Create Date: 2025-08-17 15:21:31.838211

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ec5fa6485586"
down_revision: Union[str, Sequence[str], None] = "16d8c51e89ae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add description column to categories table
    op.add_column("categories", sa.Column("description", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove description column from categories table
    op.drop_column("categories", "description")
