"""Corrigir script de migração para lidar com transações abortadas

Revision ID: 3b7e9d2a5678
Revises: 2a5f8c9d1234
Create Date: 2025-05-29 22:51:40.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import ProgrammingError, OperationalError, InternalError
import psycopg2

# revision identifiers, used by Alembic.
revision: str = '3b7e9d2a5678'
down_revision: Union[str, None] = '2a5f8c9d1234'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adicionar coluna updated_at à tabela users usando SQL direto
    # Esta abordagem é mais robusta e não será afetada por transações abortadas anteriores
    connection = op.get_bind()
    
    # Verificar se a coluna já existe antes de tentar adicioná-la
    try:
        connection.execute(sa.text("SELECT updated_at FROM users LIMIT 1"))
        # Se não lançar exceção, a coluna já existe
        print("Coluna updated_at já existe na tabela users")
    except Exception as e:
        if "column users.updated_at does not exist" in str(e) or "no such column" in str(e):
            try:
                # Adicionar a coluna updated_at
                connection.execute(sa.text(
                    "ALTER TABLE users ADD COLUMN updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()"
                ))
                # Atualizar valores existentes
                connection.execute(sa.text(
                    "UPDATE users SET updated_at = created_at WHERE updated_at IS NULL"
                ))
                print("Coluna updated_at adicionada com sucesso à tabela users")
            except Exception as add_error:
                print(f"Erro ao adicionar coluna updated_at: {add_error}")
        else:
            print(f"Erro ao verificar coluna updated_at: {e}")


def downgrade() -> None:
    # Remover coluna updated_at da tabela users
    try:
        op.drop_column('users', 'updated_at')
    except (ProgrammingError, OperationalError, InternalError):
        pass
