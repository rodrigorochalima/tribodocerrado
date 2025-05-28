import os
import sqlite3
from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime

# Função para criar e configurar a aplicação Flask
def create_app():
    app = Flask(__name__)
    
    # Configurações
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tribodocerrado_secret_key_2025')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///instance/tribo_cerrado.db')
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
        app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static', 'uploads')
    
    # Garantir que a pasta de uploads existe
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Inicializar o gerenciador de login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        from .models.user import User
        return User.query.get(int(user_id))
    
    # Registrar blueprints
    from .routes.home import home_bp
    app.register_blueprint(home_bp)
    
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from .routes.member import member_bp
    app.register_blueprint(member_bp, url_prefix='/membro')
    
    from .routes.member_gallery import member_gallery_bp
    app.register_blueprint(member_gallery_bp, url_prefix='/membro/galeria')
    
    from .routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from .routes.user import user_bp
    app.register_blueprint(user_bp, url_prefix='/usuario')
    
    # Inicializar o banco de dados
    from .models.db import db
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    
    return app

# Para execução direta
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
