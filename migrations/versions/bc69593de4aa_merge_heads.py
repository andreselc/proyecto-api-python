"""merge heads

Revision ID: bc69593de4aa
Revises: 243f6b612657, a8058471e22a
Create Date: 2024-12-26 21:00:45.869757

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 


# revision identifiers, used by Alembic.
revision: str = 'bc69593de4aa'
down_revision: Union[str, None] = ('243f6b612657', 'a8058471e22a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
