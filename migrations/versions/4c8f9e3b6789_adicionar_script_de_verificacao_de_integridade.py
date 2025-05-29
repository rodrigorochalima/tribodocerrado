"""Adicionar script de verificação de integridade do banco de dados

Revision ID: 4c8f9e3b6789
Revises: 3b7e9d2a5678
Create Date: 2025-05-29 22:53:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import ProgrammingError, OperationalError, InternalError
import psycopg2

# revision identifiers, used by Alembic.
revision: str = '4c8f9e3b6789'
down_revision: Union[str, None] = '3b7e9d2a5678'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Verificar e adicionar outras colunas que possam estar faltando
    connection = op.get_bind()
    
    # Lista de colunas a verificar e adicionar se necessário
    columns_to_check = [
        {
            'table': 'users',
            'column': 'last_login',
            'type': 'TIMESTAMP WITHOUT TIME ZONE',
            'default': 'NULL'
        },
        {
            'table': 'users',
            'column': 'is_public_profile',
            'type': 'BOOLEAN',
            'default': 'FALSE'
        },
        {
            'table': 'users',
            'column': 'is_public_full_name',
            'type': 'BOOLEAN',
            'default': 'FALSE'
        },
        {
            'table': 'users',
            'column': 'is_public_birth_date',
            'type': 'BOOLEAN',
            'default': 'FALSE'
        },
        {
            'table': 'users',
            'column': 'is_public_blood_type',
            'type': 'BOOLEAN',
            'default': 'FALSE'
        },
        {
            'table': 'users',
            'column': 'is_public_address',
            'type': 'BOOLEAN',
            'default': 'FALSE'
        },
        {
            'table': 'users',
            'column': 'is_public_health_info',
            'type': 'BOOLEAN',
            'default': 'FALSE'
        },
        {
            'table': 'users',
            'column': 'is_public_collection_date',
            'type': 'BOOLEAN',
            'default': 'FALSE'
        },
        {
            'table': 'users',
            'column': 'is_public_join_date',
            'type': 'BOOLEAN',
            'default': 'TRUE'
        }
    ]
    
    for column_info in columns_to_check:
        table = column_info['table']
        column = column_info['column']
        col_type = column_info['type']
        default = column_info['default']
        
        try:
            # Verificar se a coluna existe
            connection.execute(sa.text(f"SELECT {column} FROM {table} LIMIT 1"))
            print(f"Coluna {column} já existe na tabela {table}")
        except Exception as e:
            if "column" in str(e) and "does not exist" in str(e) or "no such column" in str(e):
                try:
                    # Adicionar a coluna
                    connection.execute(sa.text(
                        f"ALTER TABLE {table} ADD COLUMN {column} {col_type} DEFAULT {default}"
                    ))
                    print(f"Coluna {column} adicionada com sucesso à tabela {table}")
                except Exception as add_error:
                    print(f"Erro ao adicionar coluna {column} à tabela {table}: {add_error}")
            else:
                print(f"Erro ao verificar coluna {column} na tabela {table}: {e}")


def downgrade() -> None:
    # Não é necessário fazer nada no downgrade
    pass
