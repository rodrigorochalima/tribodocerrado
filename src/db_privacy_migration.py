import os
import sys
import logging
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.db import db
from src.models.user import User

def run_migration():
    try:
        # Verificar se as colunas de privacidade já existem
        inspector = db.inspect(db.engine)
        existing_columns = inspector.get_columns('users')
        existing_column_names = [col['name'] for col in existing_columns]
        
        # Lista de novas colunas de privacidade
        privacy_columns = [
            'is_public_profile',
            'is_public_full_name',
            'is_public_birth_date',
            'is_public_blood_type',
            'is_public_address',
            'is_public_health_info',
            'is_public_collection_date',
            'is_public_join_date'
        ]
        
        # Adicionar colunas que não existem
        with db.engine.connect() as conn:
            for column in privacy_columns:
                if column not in existing_column_names:
                    logging.info(f"Adicionando coluna {column} à tabela users")
                    conn.execute(f"ALTER TABLE users ADD COLUMN {column} BOOLEAN DEFAULT FALSE")
            
            # Definir is_public_join_date como TRUE por padrão
            if 'is_public_join_date' in privacy_columns:
                conn.execute("UPDATE users SET is_public_join_date = TRUE WHERE is_public_join_date IS NULL")
            
            conn.commit()
        
        logging.info("Migração concluída com sucesso!")
        return True
    except Exception as e:
        logging.error(f"Erro durante a migração: {str(e)}")
        return False

if __name__ == "__main__":
    from src.main import app
    with app.app_context():
        run_migration()
