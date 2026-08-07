"""merge migration heads

Revision ID: c3a913a94452
Revises: 71db8140ab4c, dded8d369011
Create Date: 2026-08-08 00:59:29.500086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3a913a94452'
down_revision: Union[str, Sequence[str], None] = ('71db8140ab4c', 'dded8d369011')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
