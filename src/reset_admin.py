import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from src.models.user import db, User
import logging
from werkzeug.security import generate_password_hash
from datetime import datetime

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
db.init_app(app)

def reset_admin_password():
    """Reseta a senha do administrador ou cria um novo se não existir"""
    with app.app_context():
        # Verificar se o banco de dados existe
        if not os.path.exists(DB_PATH):
            logger.info(f"Banco de dados não encontrado em {DB_PATH}. Criando tabelas...")
            db.create_all()
        
        # Verificar se existe um usuário admin
        admin = User.query.filter_by(username='admin').first()
        
        if admin:
            # Resetar a senha do admin existente
            admin.password = generate_password_hash('admin123')
            logger.info(f"Senha do usuário admin resetada para 'admin123'")
        else:
            # Criar um novo usuário admin
            new_admin = User(
                username='admin',
                email='admin@tribodocerrado.com.br',
                password=generate_password_hash('admin123'),
                full_name='Administrador',
                nickname='Admin',
                is_approved=True,
                is_admin=True,
                created_at=datetime.utcnow()
            )
            db.session.add(new_admin)
            logger.info(f"Novo usuário admin criado com senha 'admin123'")
        
        # Commit das alterações
        db.session.commit()
        
        # Verificar se a operação foi bem-sucedida
        admin = User.query.filter_by(username='admin').first()
        if admin:
            logger.info(f"Usuário admin verificado com sucesso: {admin.username}")
            logger.info(f"Admin ID: {admin.id}")
            logger.info(f"Admin é administrador: {admin.is_admin}")
            logger.info(f"Admin está aprovado: {admin.is_approved}")
        else:
            logger.error("Falha ao criar/resetar usuário admin")

if __name__ == '__main__':
    reset_admin_password()
    logger.info("Operação concluída com sucesso!")
