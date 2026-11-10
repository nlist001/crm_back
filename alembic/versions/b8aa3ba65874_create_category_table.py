"""create-category-table

Revision ID: b8aa3ba65874
Revises: 2392137ab85c
Create Date: 2026-07-08 11:40:29.166476

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8aa3ba65874'
down_revision: Union[str, Sequence[str], None] = '2392137ab85c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('category',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(150), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('category')
