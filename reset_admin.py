import os
import sys
sys.path.append('/home/ubuntu/tribo_cerrado')

from src.models.db import db
from src.models.user import User
from werkzeug.security import generate_password_hash
from flask import Flask

# Configurar a aplicação Flask mínima para acessar o banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/ubuntu/tribo_cerrado/instance/tribo_cerrado.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    # Criar todas as tabelas se não existirem
    db.create_all()
    
    # Verificar se o usuário admin já existe
    admin = User.query.filter_by(username='admin').first()
    
    if admin:
        # Atualizar a senha do admin existente
        admin.password = generate_password_hash('admin123')
        print(f"Senha do usuário admin resetada com sucesso!")
    else:
        # Criar um novo usuário admin
        new_admin = User(
            username='admin',
            email='admin@tribodocerrado.com.br',
            password=generate_password_hash('admin123'),
            full_name='Administrador',
            nickname='Admin',
            is_admin=True,
            is_approved=True
        )
        db.session.add(new_admin)
        print(f"Novo usuário admin criado com sucesso!")
    
    # Salvar as alterações no banco de dados
    db.session.commit()
    print("Operação concluída com sucesso!")
