from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask import current_app, url_for
import threading

mail = Mail()

def init_mail(app):
    """Inicializa a extensão Flask-Mail"""
    mail.init_app(app)

def generate_confirmation_token(email):
    """Gera um token seguro para confirmação de email"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration=86400):
    """Confirma um token de confirmação de email"""
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
        return email
    except:
        return False

def send_email(to, subject, template):
    """Envia um email usando Flask-Mail"""
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    
    # Enviar email em uma thread separada para não bloquear a resposta
    def send_async_email(app, msg):
        with app.app_context():
            mail.send(msg)
    
    threading.Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg)
    ).start()

def send_confirmation_email(user):
    """Envia um email de confirmação para o usuário"""
    token = user.generate_confirmation_token()
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    
    # Criar template HTML para o email
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #c00000; color: white; padding: 10px 20px; text-align: center; }}
            .content {{ padding: 20px; border: 1px solid #ddd; }}
            .button {{ display: inline-block; background-color: #c00000; color: white; padding: 10px 20px; 
                      text-decoration: none; border-radius: 5px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #777; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2>Tribo do Cerrado - Confirmação de Cadastro</h2>
            </div>
            <div class="content">
                <h3>Olá {user.full_name or user.username},</h3>
                <p>Obrigado por se cadastrar no site da Tribo do Cerrado!</p>
                <p>Para confirmar seu email e ativar sua conta, por favor clique no botão abaixo:</p>
                <p style="text-align: center;">
                    <a href="{confirm_url}" class="button">Confirmar Email</a>
                </p>
                <p>Ou copie e cole o seguinte link no seu navegador:</p>
                <p>{confirm_url}</p>
                <p>Este link expirará em 24 horas.</p>
                <p>Se você não solicitou este cadastro, por favor ignore este email.</p>
            </div>
            <div class="footer">
                <p>&copy; 2025 Tribo do Cerrado Motoclube - Goiânia, GO</p>
                <p>Este é um email automático, por favor não responda.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    send_email(user.email, "Confirmação de Cadastro - Tribo do Cerrado", html)
    return token
