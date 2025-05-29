import os
import sys
import logging
from flask import Flask
from sqlalchemy import text

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adicionar diretórios ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Inicialização da aplicação Flask
app = Flask(__name__)

# Importar configuração
from src.config import DATABASE_URL
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco de dados
from src.models.db import db
db.init_app(app)

def check_column_exists(engine, table_name, column_name):
    """Verifica se uma coluna existe em uma tabela no PostgreSQL"""
    if 'postgresql' in str(engine.url):
        query = text(f"""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}' 
            AND column_name = '{column_name}'
        """)
    else:
        # SQLite
        query = text(f"PRAGMA table_info({table_name})")
    
    with engine.connect() as conn:
        result = conn.execute(query)
        columns = result.fetchall()
        
        if 'postgresql' in str(engine.url):
            return len(columns) > 0
        else:
            # SQLite
            for column in columns:
                if column[1] == column_name:
                    return True
            return False

def add_column_if_not_exists(engine, table_name, column_name, column_type):
    """Adiciona uma coluna a uma tabela se ela não existir"""
    if not check_column_exists(engine, table_name, column_name):
        try:
            with engine.connect() as conn:
                if 'postgresql' in str(engine.url):
                    query = text(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} {column_type}")
                else:
                    # SQLite não suporta IF NOT EXISTS para colunas
                    query = text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
                
                conn.execute(query)
                conn.commit()
                logger.info(f"Coluna {column_name} adicionada à tabela {table_name}")
        except Exception as e:
            logger.error(f"Erro ao adicionar coluna {column_name}: {e}")
    else:
        logger.info(f"Coluna {column_name} já existe na tabela {table_name}")

def migrate_database():
    """Executa a migração do banco de dados"""
    with app.app_context():
        engine = db.engine
        
        # Verificar se as tabelas existem, se não, criar todas
        db.create_all()
        logger.info("Tabelas verificadas/criadas")
        
        # Adicionar colunas que podem estar faltando na tabela users
        # Coluna que estava causando o erro
        add_column_if_not_exists(engine, 'users', 'join_date', 'DATE')
        
        # Outras colunas que podem estar faltando
        add_column_if_not_exists(engine, 'users', 'nickname', 'VARCHAR(80)')
        add_column_if_not_exists(engine, 'users', 'birth_date', 'DATE')
        add_column_if_not_exists(engine, 'users', 'collection_date', 'DATE')
        add_column_if_not_exists(engine, 'users', 'blood_type', 'VARCHAR(10)')
        add_column_if_not_exists(engine, 'users', 'profile_image', 'VARCHAR(255)')
        add_column_if_not_exists(engine, 'users', 'address_street', 'VARCHAR(255)')
        add_column_if_not_exists(engine, 'users', 'address_number', 'VARCHAR(20)')
        add_column_if_not_exists(engine, 'users', 'address_complement', 'VARCHAR(255)')
        add_column_if_not_exists(engine, 'users', 'address_district', 'VARCHAR(255)')
        add_column_if_not_exists(engine, 'users', 'address_city', 'VARCHAR(255)')
        add_column_if_not_exists(engine, 'users', 'address_state', 'VARCHAR(2)')
        add_column_if_not_exists(engine, 'users', 'address_zipcode', 'VARCHAR(20)')
        add_column_if_not_exists(engine, 'users', 'health_notes', 'TEXT')
        add_column_if_not_exists(engine, 'users', 'health_insurance', 'VARCHAR(255)')
        add_column_if_not_exists(engine, 'users', 'health_insurance_number', 'VARCHAR(255)')
        add_column_if_not_exists(engine, 'users', 'last_login', 'TIMESTAMP')
        add_column_if_not_exists(engine, 'users', 'is_admin', 'BOOLEAN')
        add_column_if_not_exists(engine, 'users', 'is_active', 'BOOLEAN')
        add_column_if_not_exists(engine, 'users', 'bio', 'TEXT')
        add_column_if_not_exists(engine, 'users', 'godfather_id', 'INTEGER')
        add_column_if_not_exists(engine, 'users', 'is_approved', 'BOOLEAN')
        
        # Campos de privacidade
        add_column_if_not_exists(engine, 'users', 'is_public_profile', 'BOOLEAN')
        add_column_if_not_exists(engine, 'users', 'is_public_full_name', 'BOOLEAN')
        add_column_if_not_exists(engine, 'users', 'is_public_birth_date', 'BOOLEAN')
        add_column_if_not_exists(engine, 'users', 'is_public_blood_type', 'BOOLEAN')
        add_column_if_not_exists(engine, 'users', 'is_public_address', 'BOOLEAN')
        add_column_if_not_exists(engine, 'users', 'is_public_health_info', 'BOOLEAN')
        add_column_if_not_exists(engine, 'users', 'is_public_collection_date', 'BOOLEAN')
        add_column_if_not_exists(engine, 'users', 'is_public_join_date', 'BOOLEAN')
        
        # Verificar se existe pelo menos um usuário administrador
        from src.models.user import User
        admin = User.query.filter_by(is_admin=True).first()
        if not admin:
            logger.info("Criando usuário administrador padrão")
            from werkzeug.security import generate_password_hash
            
            admin_user = User(
                username="admin",
                email="admin@tribodocerrado.com.br",
                password=generate_password_hash("admin123"),
                full_name="Administrador",
                nickname="Admin",
                is_approved=True,
                is_admin=True
            )
            
            db.session.add(admin_user)
            db.session.commit()
            logger.info(f"Usuário administrador criado: {admin_user.username}")
        
        logger.info("Migração do banco de dados concluída com sucesso!")

if __name__ == '__main__':
    migrate_database()
