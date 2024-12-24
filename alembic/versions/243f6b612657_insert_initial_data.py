"""Insert initial data

Revision ID: 243f6b612657
Revises: 2b99e9fdd4d7
Create Date: 2024-12-22 22:06:56.555927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = '243f6b612657'
down_revision: Union[str, None] = '2b99e9fdd4d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    op.execute(
        f"""
        INSERT INTO productmodel (id, name, code, description, price, profit_margin, cost, status, created_at) 
        VALUES ('c3f73879-ff95-4a74-9826-3d495d8c7596', 'Smartphone NovaTech X50', 'PRD12', 'Smartphone NovaTech X50', 399.99, 12.5, 349.99, 'active', '{current_time}');
        """
    )
    op.execute(
        f"""
        INSERT INTO productmodel (id, name, code, description, price, profit_margin, cost, status, created_at) 
        VALUES ('cf8a19fa-f364-4974-8eeb-b92ad4d49086', 'Tablet NovaTech Tab 8 Pro', 'TAB87', 'Tablet NovaTech Tab 8 Pro', 259.34, 15.2, 219.95, 'active', '{current_time}');
        """
    )
    op.execute(
        f"""
        INSERT INTO productmodel (id, name, code, description, price, profit_margin, cost, status, created_at) 
        VALUES ('3b4f76d4-293f-48ad-bad2-6ef8c1660a1d', 'Auriculares inalámbricos NovaTech AirBuds Pro', 'EAR34', 'Auriculares inalámbricos NovaTech AirBuds Pro', 134.59, 10.8, 119.99, 'active', '{current_time}');
        """
    )
    op.execute(
        f"""
        INSERT INTO productmodel (id, name, code, description, price, profit_margin, cost, status, created_at) 
        VALUES ('58895338-c20f-4b24-8ee6-1fdc2f113f08', 'Smartwatch NovaTech Fit', 'WAT56', 'Smartwatch NovaTech Fit', 208.01, 13.7, 179.5, 'active', '{current_time}');
        """
    )
    op.execute(
        f"""
        INSERT INTO productmodel (id, name, code, description, price, profit_margin, cost, status, created_at) 
        VALUES ('bfb7d2c1-88dc-4ba3-8d0e-1c3c983ecdea', 'Laptop NovaTech Book Pro', 'LAP98', 'Laptop NovaTech Book Pro', 956.63, 11.2, 849.99, 'active', '{current_time}');
        """
    )
    op.execute(
        f"""
        INSERT INTO productmodel (id, name, code, description, price, profit_margin, cost, status, created_at) 
        VALUES ('50a53f0d-f84f-462d-96f0-c9fa90a4477f', 'Altavoz inteligente NovaTech Home', 'SPK21', 'Altavoz inteligente NovaTech Home', 104.73, 14.1, 89.99, 'active', '{current_time}');
        """
    )
    op.execute(
        f"""
        INSERT INTO productmodel (id, name, code, description, price, profit_margin, cost, status, created_at) 
        VALUES ('2a0ae0b2-06e2-41c8-8583-9021c515d68d', 'Cámara de seguridad NovaTech Eye', 'CAM43', 'Cámara de seguridad NovaTech Eye', 85.46, 12.3, 74.95, 'active', '{current_time}');
        """
    )
    op.execute(
        f"""
        INSERT INTO productmodel (id, name, code, description, price, profit_margin, cost, status, created_at) 
        VALUES ('a6442e6d-43f6-42f5-b133-8141afda24f6', 'Consola de videojuegos NovaTech Play', 'CON65', 'Consola de videojuegos NovaTech Play', 295.86, 15.5, 249.99, 'active', '{current_time}');
        """
    )
    op.execute(
        f"""
        INSERT INTO productmodel (id, name, code, description, price, profit_margin, cost, status, created_at) 
        VALUES ('69e8d26f-d5e1-4a10-baa3-5fcb01b93f71', 'Drone NovaTech Sky', 'DRN78', 'Drone NovaTech Sky', 449.49, 10.9, 399.99, 'active', '{current_time}');
        """
    )
    op.execute(
        f"""
        INSERT INTO productmodel (id, name, code, description, price, profit_margin, cost, status, created_at) 
        VALUES ('66c1b456-3258-4a26-8120-b64c6a3e868f', 'Smart TV NovaTech Vision 55', 'TV90', 'Smart TV NovaTech Vision 55', 574.87, 13.1, 499.95, 'active', '{current_time}');
        """
    )
    op.execute(
        f"""
        INSERT INTO productmodel (id, name, code, description, price, profit_margin, cost, status, created_at) 
        VALUES ('c2e0ea3e-6301-4c68-a409-76ba2457b678', 'Auriculares con cable NovaTech Classic', 'EAR11', 'Auriculares con cable NovaTech Classic', 39.49, 11.4, 34.99, 'active', '{current_time}');
        """
    )
    op.execute(
        f"""
        INSERT INTO productmodel (id, name, code, description, price, profit_margin, cost, status, created_at) 
        VALUES ('f6aa5478-cda7-406b-9cb2-11c55b2bda75', 'Batería externa NovaTech PowerBank', 'BAT23', 'Batería externa NovaTech PowerBank', 58.63, 14.8, 49.95, 'active', '{current_time}');
        """
    )
    op.execute(
        f"""
        INSERT INTO productmodel (id, name, code, description, price, profit_margin, cost, status, created_at) 
        VALUES ('7dc3a2b3-6e92-4f94-98b4-e82aa7a19f90', 'Teclado mecánico NovaTech Gamer', 'KEY34', 'Teclado mecánico NovaTech Gamer', 118.02, 15.3, 99.99, 'active', '{current_time}');
        """
    )
    op.execute(
        f"""
        INSERT INTO productmodel (id, name, code, description, price, profit_margin, cost, status, created_at) 
        VALUES ('39ac68a8-8c33-49a6-8c84-4fc053cf97c4', 'Auriculares VR NovaTech Reality', 'VR78', 'Auriculares VR NovaTech Reality', 335.71, 10.7, 299.99, 'active', '{current_time}');
        """
    )

def downgrade():
    op.execute(
        """
        DELETE FROM productmodel WHERE id IN (
            'c3f73879-ff95-4a74-9826-3d495d8c7596',
            'cf8a19fa-f364-4974-8eeb-b92ad4d49086',
            '3b4f76d4-293f-48ad-bad2-6ef8c1660a1d',
            '58895338-c20f-4b24-8ee6-1fdc2f113f08',
            'bfb7d2c1-88dc-4ba3-8d0e-1c3c983ecdea',
            '50a53f0d-f84f-462d-96f0-c9fa90a4477f',
            '2a0ae0b2-06e2-41c8-8583-9021c515d68d',
            'a6442e6d-43f6-42f5-b133-8141afda24f6',
            '69e8d26f-d5e1-4a10-baa3-5fcb01b93f71',
            '66c1b456-3258-4a26-8120-b64c6a3e868f',
            'c2e0ea3e-6301-4c68-a409-76ba2457b678',
            'f6aa5478-cda7-406b-9cb2-11c55b2bda75',
            '7dc3a2b3-6e92-4f94-98b4-e82aa7a19f90',
            '39ac68a8-8c33-49a6-8c84-4fc053cf97c4'
        );
        """
    )