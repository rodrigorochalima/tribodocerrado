import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import sys
import logging
import sqlite3
from datetime import datetime
from flask import Flask

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho absoluto para o banco de dados
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'tribo_cerrado.db')
DB_URI = f'sqlite:///{DB_PATH}'

# Inicialização da aplicação Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Garantir que o diretório instance existe
os.makedirs(os.path.join(BASE_DIR, 'instance'), exist_ok=True)
logger.info(f"Diretório do banco de dados: {os.path.join(BASE_DIR, 'instance')}")
logger.info(f"Caminho do banco de dados: {DB_PATH}")

# Inicialização do banco de dados
from src.models.db import db
db.init_app(app)

def check_column_exists(table_name, column_name):
    """Verifica se uma coluna existe em uma tabela"""
    # Verifica se o arquivo do banco de dados existe
    if not os.path.exists(DB_PATH):
        logger.info(f"Banco de dados não encontrado em {DB_PATH}. Será criado.")
        return False
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Consulta para obter informações sobre as colunas da tabela
    try:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        # Verifica se a coluna existe
        for column in columns:
            if column[1] == column_name:
                return True
                
        return False
    except sqlite3.Error as e:
        logger.error(f"Erro ao verificar coluna {column_name}: {e}")
        return False
    finally:
        conn.close()

def add_column(table_name, column_name, column_type):
    """Adiciona uma coluna a uma tabela se ela não existir"""
    # Verifica se o arquivo do banco de dados existe
    if not os.path.exists(DB_PATH):
        logger.info(f"Banco de dados não encontrado em {DB_PATH}. Será criado durante a migração.")
        return
    
    if not check_column_exists(table_name, column_name):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
            conn.commit()
            logger.info(f"Coluna {column_name} adicionada à tabela {table_name}")
        except sqlite3.Error as e:
            logger.error(f"Erro ao adicionar coluna {column_name}: {e}")
        finally:
            conn.close()
    else:
        logger.info(f"Coluna {column_name} já existe na tabela {table_name}")

def migrate_database():
    """Executa a migração do banco de dados"""
    with app.app_context():
        # Importar modelos aqui para evitar problemas de importação circular
        from src.models.user import User
        from src.models.motorcycle import Motorcycle
        from src.models.family import FamilyMember
        
        # Verifica se as tabelas existem, se não, cria todas
        db.create_all()
        logger.info("Tabelas verificadas/criadas")
        
        # Adiciona colunas que podem estar faltando na tabela user
        add_column('users', 'nickname', 'VARCHAR(50)')
        add_column('users', 'birth_date', 'DATE')
        add_column('users', 'collection_date', 'DATE')
        add_column('users', 'blood_type', 'VARCHAR(10)')
        add_column('users', 'address_street', 'VARCHAR(100)')
        add_column('users', 'address_number', 'VARCHAR(20)')
        add_column('users', 'address_complement', 'VARCHAR(100)')
        add_column('users', 'address_district', 'VARCHAR(100)')
        add_column('users', 'address_city', 'VARCHAR(100)')
        add_column('users', 'address_state', 'VARCHAR(50)')
        add_column('users', 'address_zipcode', 'VARCHAR(20)')
        add_column('users', 'health_notes', 'TEXT')
        add_column('users', 'health_insurance', 'VARCHAR(100)')
        add_column('users', 'health_insurance_number', 'VARCHAR(50)')
        add_column('users', 'godfather_id', 'INTEGER')
        
        # Adiciona novas colunas de controle de privacidade
        add_column('users', 'full_name_public', 'BOOLEAN DEFAULT 0')
        add_column('users', 'birth_date_public', 'BOOLEAN DEFAULT 0')
        add_column('users', 'collection_date_public', 'BOOLEAN DEFAULT 0')
        add_column('users', 'blood_type_public', 'BOOLEAN DEFAULT 0')
        add_column('users', 'address_public', 'BOOLEAN DEFAULT 0')
        add_column('users', 'bio_public', 'BOOLEAN DEFAULT 0')
        add_column('users', 'health_info_public', 'BOOLEAN DEFAULT 0')
        
        # Verifica se existe pelo menos um usuário administrador
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
