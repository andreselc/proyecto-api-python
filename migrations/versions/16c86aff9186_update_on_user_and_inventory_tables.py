"""Update on User and Inventory tables

Revision ID: 16c86aff9186
Revises: 1a3eeb2ba93e
Create Date: 2025-01-03 22:24:10.146918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 


# revision identifiers, used by Alembic.
revision: str = '16c86aff9186'
down_revision: Union[str, None] = '1a3eeb2ba93e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###