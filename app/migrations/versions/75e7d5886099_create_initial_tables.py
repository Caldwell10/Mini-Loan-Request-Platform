"""create initial tables (empty stub restored)

Revision ID: 75e7d5886099
Revises:
Create Date: 2025-09-24 09:24:40.743795
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "75e7d5886099"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
