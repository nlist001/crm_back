"""create-brands-table

Revision ID: 2392137ab85c
Revises: 
Create Date: 2026-07-08 11:13:32.151000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2392137ab85c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('brands',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(150), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('brands')
