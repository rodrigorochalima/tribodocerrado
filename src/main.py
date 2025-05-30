from flask import Flask, request, abort
from flask_login import LoginManager
from src.models.user import User
from src.models.db import db, init_db
from src.routes.home import home_bp
from src.routes.auth import auth_bp
from src.routes.member import member_bp
from src.routes.user import user_bp
from src.utils.email import init_mail
from src.config import get_config
import os
import time
import logging
from logging.handlers import RotatingFileHandler
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

# Configurar logging
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/tribodocerrado.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

# Criar aplicação Flask
def create_app(config_class=None):
    app = Flask(__name__, 
                static_folder='../static',
                template_folder='templates')
    
    # Configuração
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)
    
    # Configurar logging
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Inicializando aplicação Tribo do Cerrado')
    
    # Inicializar extensões
    db.init_app(app)
    
    # Inicializar Flask-Mail
    init_mail(app)
    
    # Inicializar CSRF Protection
    csrf = CSRFProtect(app)
    
    # Inicializar Flask-Limiter para proteção contra brute force
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://",
    )
    
    # Configurar limites específicos para rotas sensíveis
    @limiter.limit("5 per minute")
    @app.route("/login", methods=["POST"])
    def login_limit():
        return "Limite de tentativas excedido. Tente novamente mais tarde."
    
    @limiter.limit("3 per minute")
    @app.route("/register", methods=["POST"])
    def register_limit():
        return "Limite de tentativas excedido. Tente novamente mais tarde."
    
    # Configurar Login Manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor, faça login para acessar esta página.'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Registrar blueprints
    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(member_bp, url_prefix='/member')
    app.register_blueprint(user_bp, url_prefix='/user')
    
    # Middleware para proteção contra ataques
    @app.before_request
    def before_request():
        # Registrar início da requisição para detectar ataques de timing
        request.start_time = time.time()
        
        # Verificar User-Agent
        user_agent = request.headers.get('User-Agent', '')
        if not user_agent or len(user_agent) < 5:
            app.logger.warning(f"Requisição suspeita sem User-Agent: {request.remote_addr}")
            abort(403)  # Forbidden
        
        # Verificar se é um bot conhecido
        bot_signatures = ['bot', 'crawl', 'spider', 'scrape']
        if any(bot in user_agent.lower() for bot in bot_signatures):
            # Permitir bots legítimos como Googlebot, mas registrar
            legitimate_bots = ['Googlebot', 'Bingbot', 'Slurp', 'DuckDuckBot']
            if not any(bot in user_agent for bot in legitimate_bots):
                app.logger.warning(f"Bot detectado: {user_agent} de {request.remote_addr}")
        
        # Verificar métodos HTTP permitidos
        if request.method not in ['GET', 'POST', 'HEAD']:
            app.logger.warning(f"Método HTTP não permitido: {request.method} de {request.remote_addr}")
            abort(405)  # Method Not Allowed
    
    @app.after_request
    def after_request(response):
        # Adicionar headers de segurança
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        
        # Registrar tempo de resposta para detectar ataques de timing
        if hasattr(request, 'start_time'):
            elapsed = time.time() - request.start_time
            # Se a requisição for muito rápida, pode ser um bot
            if elapsed < 0.01 and request.path not in ['/static', '/favicon.ico']:
                app.logger.warning(f"Requisição suspeita (muito rápida): {request.path} de {request.remote_addr}")
            
            # Se a requisição for muito lenta, pode ser um ataque DoS
            if elapsed > 5.0:
                app.logger.warning(f"Requisição lenta: {request.path} de {request.remote_addr} ({elapsed:.2f}s)")
        
        return response
    
    # Criar tabelas do banco de dados
    with app.app_context():
        init_db()
    
    return app

# Criar instância da aplicação para o Gunicorn encontrar
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'])
