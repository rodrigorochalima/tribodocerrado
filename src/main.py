import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Importação da instância única do SQLAlchemy
from src.models.db import db
from src.config import DATABASE_URL, SECRET_KEY, PORT
from flask_login import LoginManager

def create_app():
    from flask import Flask, render_template
    
    app = Flask(__name__)
    
    # Garantir que o diretório instance existe
    instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    os.makedirs(instance_path, exist_ok=True)
    
    # Configuração do banco de dados com suporte a PostgreSQL para produção
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY
    
    # Inicialização do banco de dados com o app
    db.init_app(app)
    
    # Inicialização do Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Função para carregar usuário pelo ID
    @login_manager.user_loader
    def load_user(user_id):
        from src.models.user import User
        return User.query.get(int(user_id))
    
    # Registro de blueprints
    from src.routes.auth import auth_bp
    from src.routes.post import post_bp
    from src.routes.gallery import gallery_bp
    from src.routes.contact import contact_bp
    from src.routes.user import user_bp
    from src.routes.member import member_bp
    from src.routes.member_gallery import member_gallery_bp
    from src.routes.admin import admin_bp
    from src.routes.home import home_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(member_bp)
    app.register_blueprint(member_gallery_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(home_bp)
    
    # Criação das tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    # Rota principal - agora usa a homepage pública
    @app.route('/')
    def index():
        return render_template('public/home.html')
    
    # Filtros personalizados para templates
    @app.template_filter('date_format')
    def date_format(value):
        if value:
            from datetime import datetime
            return value.strftime('%d/%m/%Y')
        return ''
    
    @app.template_filter('days_until')
    def days_until(date):
        if date:
            from datetime import datetime
            delta = date - datetime.now().date()
            return delta.days
        return 0
    
    @app.template_filter('days_until_birthday')
    def days_until_birthday(birth_date):
        if birth_date:
            from datetime import datetime
            today = datetime.now().date()
            next_birthday = datetime(today.year, birth_date.month, birth_date.day).date()
            
            if next_birthday < today:
                next_birthday = datetime(today.year + 1, birth_date.month, birth_date.day).date()
            
            delta = next_birthday - today
            return delta.days
        return 0
    
    return app
# Importação aqui para evitar importação circular
from datetime import datetime
if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=PORT, debug=False)
