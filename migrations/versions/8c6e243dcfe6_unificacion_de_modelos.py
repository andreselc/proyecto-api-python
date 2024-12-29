"""Unificacion de modelos

Revision ID: 8c6e243dcfe6
Revises: 4cf2a98d0de1
Create Date: 2024-12-29 15:20:14.359931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 


# revision identifiers, used by Alembic.
revision: str = '8c6e243dcfe6'
down_revision: Union[str, None] = '4cf2a98d0de1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shoppincartmodel',
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.Column('inventory_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventorymodel.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id', 'inventory_id', 'user_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('shoppincartmodel')
    # ### end Alembic commands ###