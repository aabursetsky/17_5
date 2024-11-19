"""empty message

Revision ID: f01e576256cd
Revises: b9584e5b70f1
Create Date: 2024-11-19 13:21:21.100507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f01e576256cd'
down_revision: Union[str, None] = 'b9584e5b70f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
