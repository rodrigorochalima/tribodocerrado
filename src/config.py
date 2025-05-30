import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env se existir
load_dotenv()

# Garantir que o diretório instance existe
instance_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
os.makedirs(instance_path, exist_ok=True)

# Variáveis globais para importação direta
DATABASE_URL = os.environ.get('DATABASE_URL', f'sqlite:///{instance_path}/tribo_cerrado.db')

# Se o DATABASE_URL começar com postgres://, substituir por postgresql://
# (necessário para o SQLAlchemy 1.4+)
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

SECRET_KEY = os.environ.get('SECRET_KEY', 'chave_secreta_padrao_para_desenvolvimento')
PORT = int(os.environ.get('PORT', 5000))
CUSTOM_DOMAIN = os.environ.get('CUSTOM_DOMAIN', None)

# Configurações de email
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ('true', 'yes', '1')
MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() in ('true', 'yes', '1')
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'tribodocerrado@gmail.com')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'tribodocerrado@gmail.com')

class Config:
    # Configuração básica
    SECRET_KEY = SECRET_KEY
    DEBUG = False
    TESTING = False
    
    # Configuração do banco de dados
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuração de upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    
    # Configuração de sessão
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutos
    
    # Configuração de domínio personalizado
    CUSTOM_DOMAIN = CUSTOM_DOMAIN
    
    # Configuração de email
    MAIL_SERVER = MAIL_SERVER
    MAIL_PORT = MAIL_PORT
    MAIL_USE_TLS = MAIL_USE_TLS
    MAIL_USE_SSL = MAIL_USE_SSL
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    MAIL_DEFAULT_SENDER = MAIL_DEFAULT_SENDER
    
    # Configuração de segurança
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'tribo-do-cerrado-salt-seguro')
    SECURITY_TOKEN_MAX_AGE = 86400  # 24 horas para confirmar o email

class DevelopmentConfig(Config):
    DEBUG = True
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
class ProductionConfig(Config):
    # Configurações específicas para produção
    pass

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Retorna a configuração baseada no ambiente"""
    env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, config['default'])
