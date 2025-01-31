"""Change created_at and updated_at to string

Revision ID: 2b99e9fdd4d7
Revises: 44f2310f378d
Create Date: 2024-12-19 22:54:50.636125

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2b99e9fdd4d7'
down_revision: Union[str, None] = '44f2310f378d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('productmodel',
    sa.Column('id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('code', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('status', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('profit_margin', sa.Float(), nullable=False),
    sa.Column('cost', sa.Float(), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('created_at', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('updated_at', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('product')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('code', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('status', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('profit_margin', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('cost', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('price', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='product_pkey')
    )
    op.drop_table('productmodel')
    # ### end Alembic commands ###
