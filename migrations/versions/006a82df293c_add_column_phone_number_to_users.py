"""Add column phone_number to users

Revision ID: 006a82df293c
Revises: 
Create Date: 2024-03-06 21:46:26.491630

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '006a82df293c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String(45), nullable=True))


def downgrade() -> None:
    pass
