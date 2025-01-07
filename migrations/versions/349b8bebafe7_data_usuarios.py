"""Data Usuarios

Revision ID: 349b8bebafe7
Revises: 16c86aff9186
Create Date: 2025-01-05 18:18:33.775010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 
from app.users.auth.utils import get_password_hash
from datetime import datetime

# revision identifiers, used by Alembic.
revision: str = '349b8bebafe7'
down_revision: Union[str, None] = '16c86aff9186'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hashed_password = get_password_hash("12345")

    op.execute(
        f"""
        INSERT INTO "User" (id, name, email, username, password, role, created_at) 
        VALUES ('d3b88d9a-bd82-4f8d-9e7e-4a1e1e69e9e0','Andrés','andreslopez@gmail.com','andresL','{hashed_password}','manager','{current_time}');
        """
    )

    op.execute(
        f"""
        INSERT INTO "User" (id, name, email, username, password, role, created_at) 
        VALUES ('6e2c8b3e-0c69-4f5a-9f8e-9b9c2fc2e9f3', 'Samuel','samuelponce@gmail.com','samuelP','{hashed_password}','customer','{current_time}');
        """
    )



def downgrade() -> None:
    op.execute(
        """
        DELETE FROM "User" WHERE id IN (
            'd3b88d9a-bd82-4f8d-9e7e-4a1e1e69e9e0',
            '6e2c8b3e-0c69-4f5a-9f8e-9b9c2fc2e9f3',
        );
        """
    )
