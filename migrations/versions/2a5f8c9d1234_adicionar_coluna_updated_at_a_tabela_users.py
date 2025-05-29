"""Adicionar coluna updated_at à tabela users

Revision ID: 2a5f8c9d1234
Revises: c9f84a5a4568
Create Date: 2025-05-29 20:47:20.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.exc import ProgrammingError, OperationalError


# revision identifiers, used by Alembic.
revision: str = '2a5f8c9d1234'
down_revision: Union[str, None] = 'c9f84a5a4568'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Adicionar coluna updated_at à tabela users
    try:
        op.add_column('users', sa.Column('updated_at', sa.DateTime(), nullable=True, server_default=sa.text('NOW()')))
        # Atualizar valores existentes para usar o mesmo valor de created_at
        op.execute("UPDATE users SET updated_at = created_at WHERE updated_at IS NULL")
    except (ProgrammingError, OperationalError) as e:
        # Se a coluna já existir, ignorar o erro
        if 'already exists' not in str(e):
            raise


def downgrade() -> None:
    # Remover coluna updated_at da tabela users
    try:
        op.drop_column('users', 'updated_at')
    except (ProgrammingError, OperationalError):
        pass
