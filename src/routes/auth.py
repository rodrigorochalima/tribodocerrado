from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from src.models.user import User
from datetime import datetime
from src.models.db import db
from src.utils.email import send_confirmation_email, confirm_token
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário já está autenticado, redireciona para o perfil
    if current_user.is_authenticated:
        return redirect(url_for('member.profile'))
        
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        # Verificar se a requisição é AJAX/JSON
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
        
        # Obter dados do formulário ou JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        if not data:
            if is_ajax:
                return jsonify({'success': False, 'message': 'Dados de login inválidos'}), 400
            flash('Dados de login inválidos', 'danger')
            return redirect(url_for('auth.login'))
        
        username = data.get('username')
        password = data.get('password')
        remember = data.get('remember', False)
        
        if not username or not password:
            if is_ajax:
                return jsonify({'success': False, 'message': 'Por favor, forneça nome de usuário e senha'}), 400
            flash('Por favor, forneça nome de usuário e senha', 'danger')
            return redirect(url_for('auth.login'))
        
        # Buscar usuário por nome de usuário ou email
        user = User.query.filter_by(username=username).first()
        if not user:
            # Tentar buscar por email
            user = User.query.filter_by(email=username).first()
        
        # Verificar se a conta está bloqueada por muitas tentativas de login
        if user and user.is_account_locked():
            if is_ajax:
                return jsonify({'success': False, 'message': 'Conta temporariamente bloqueada por muitas tentativas de login. Tente novamente mais tarde.'}), 401
            flash('Conta temporariamente bloqueada por muitas tentativas de login. Tente novamente mais tarde.', 'danger')
            return redirect(url_for('auth.login'))
        
        if user and check_password_hash(user.password, password):
            # Verificar se o email foi confirmado
            if not user.email_confirmed:
                if is_ajax:
                    return jsonify({'success': False, 'message': 'Por favor, confirme seu email antes de fazer login. Verifique sua caixa de entrada.'}), 401
                flash('Por favor, confirme seu email antes de fazer login. Verifique sua caixa de entrada.', 'warning')
                return redirect(url_for('auth.login'))
            
            # Resetar contador de tentativas de login falhas
            user.reset_failed_login()
            
            # Atualizar último login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Fazer login do usuário
            login_user(user, remember=bool(remember))
            
            if is_ajax:
                return jsonify({'success': True, 'redirect': url_for('member.profile')})
            
            # Redirecionar para a página de perfil após login bem-sucedido
            return redirect(url_for('member.profile'))
        else:
            # Incrementar contador de tentativas de login falhas
            if user:
                user.increment_failed_login()
                db.session.commit()
            
            if is_ajax:
                return jsonify({'success': False, 'message': 'Nome de usuário ou senha inválidos'}), 401
            flash('Nome de usuário ou senha inválidos', 'danger')
            return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Você saiu com sucesso', 'info')
    return redirect(url_for('home.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('member.profile'))
        
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        # Obter dados do formulário
        username = request.form.get('username')
        email = request.form.get('email')
        full_name = request.form.get('full_name')
        nickname = request.form.get('nickname')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        birth_date = request.form.get('birth_date')
        blood_type = request.form.get('blood_type')
        terms = request.form.get('terms')
        
        # Validações básicas
        if not username or not email or not full_name or not password or not confirm_password or not birth_date:
            flash('Todos os campos obrigatórios devem ser preenchidos', 'danger')
            return redirect(url_for('auth.register'))
        
        if not terms:
            flash('Você deve aceitar os termos e condições', 'danger')
            return redirect(url_for('auth.register'))
        
        # Verificar se o usuário já existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Nome de usuário já está em uso', 'danger')
            return redirect(url_for('auth.register'))
        
        # Verificar se o email já existe
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash('Email já está em uso', 'danger')
            return redirect(url_for('auth.register'))
        
        # Verificar se as senhas coincidem
        if password != confirm_password:
            flash('As senhas não coincidem', 'danger')
            return redirect(url_for('auth.register'))
        
        # Validar força da senha
        if not validate_password_strength(password, birth_date):
            flash('A senha não atende aos requisitos de segurança', 'danger')
            return redirect(url_for('auth.register'))
        
        try:
            # Converter data de nascimento
            birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date() if birth_date else None
            
            # Criar novo usuário
            new_user = User(
                username=username,
                email=email,
                full_name=full_name,
                nickname=nickname,
                birth_date=birth_date_obj,
                blood_type=blood_type,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                is_active=False,  # Usuário inativo até confirmar email
                email_confirmed=False  # Email não confirmado
            )
            
            # Definir senha com hash
            new_user.set_password(password)
            
            # Salvar no banco de dados
            db.session.add(new_user)
            db.session.commit()
            
            # Enviar email de confirmação
            send_confirmation_email(new_user)
            
            # Mensagem de sucesso
            flash('Cadastro realizado com sucesso! Por favor, verifique seu email para confirmar sua conta.', 'success')
            
            # Redirecionar para a página de login
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar usuário: {str(e)}', 'danger')
            return redirect(url_for('auth.register'))
    
    return render_template('register.html')

@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = confirm_token(token)
        
        if not email:
            flash('O link de confirmação é inválido ou expirou.', 'danger')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('Usuário não encontrado.', 'danger')
            return redirect(url_for('auth.login'))
        
        if user.email_confirmed:
            flash('Conta já confirmada. Por favor, faça login.', 'info')
            return redirect(url_for('auth.login'))
        
        # Confirmar email e ativar conta
        user.confirm_email()
        db.session.commit()
        
        flash('Seu email foi confirmado com sucesso! Agora você pode fazer login.', 'success')
        return redirect(url_for('auth.login'))
        
    except Exception as e:
        flash(f'Erro ao confirmar email: {str(e)}', 'danger')
        return redirect(url_for('auth.login'))

@auth_bp.route('/resend-confirmation')
def resend_confirmation():
    if current_user.is_authenticated:
        return redirect(url_for('member.profile'))
    
    return render_template('resend_confirmation.html')

@auth_bp.route('/resend-confirmation', methods=['POST'])
def resend_confirmation_post():
    email = request.form.get('email')
    
    if not email:
        flash('Por favor, forneça seu email.', 'danger')
        return redirect(url_for('auth.resend_confirmation'))
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        # Não informar que o usuário não existe por questões de segurança
        flash('Se o email estiver cadastrado, um novo link de confirmação será enviado.', 'info')
        return redirect(url_for('auth.login'))
    
    if user.email_confirmed:
        flash('Seu email já foi confirmado. Por favor, faça login.', 'info')
        return redirect(url_for('auth.login'))
    
    # Enviar novo email de confirmação
    send_confirmation_email(user)
    
    flash('Um novo link de confirmação foi enviado para seu email.', 'success')
    return redirect(url_for('auth.login'))

def validate_password_strength(password, birth_date):
    """
    Valida a força da senha de acordo com os requisitos:
    - Mínimo de 8 caracteres
    - Pelo menos 1 letra maiúscula
    - Pelo menos 1 letra minúscula
    - Pelo menos 1 número
    - Sem números sequenciais
    - Não pode conter a data de nascimento
    """
    # Verificar comprimento
    if len(password) < 8:
        return False
    
    # Verificar letra maiúscula
    if not re.search(r'[A-Z]', password):
        return False
    
    # Verificar letra minúscula
    if not re.search(r'[a-z]', password):
        return False
    
    # Verificar número
    if not re.search(r'[0-9]', password):
        return False
    
    # Verificar sequências numéricas
    sequences = ['123', '234', '345', '456', '567', '678', '789', '987', '876', '765', '654', '543', '432', '321']
    for seq in sequences:
        if seq in password:
            return False
    
    # Verificar data de nascimento
    if birth_date:
        try:
            birth_date_obj = datetime.strptime(birth_date, '%Y-%m-%d').date()
            day = birth_date_obj.day
            month = birth_date_obj.month
            year = birth_date_obj.year
            short_year = year % 100
            
            # Formatos de data para verificar
            date_formats = [
                f"{day:02d}{month:02d}",
                f"{month:02d}{day:02d}",
                f"{day:02d}{month:02d}{year}",
                f"{day:02d}{month:02d}{short_year:02d}",
                f"{year}",
                f"{short_year:02d}"
            ]
            
            for date_format in date_formats:
                if date_format in password:
                    return False
        except:
            # Se houver erro na conversão da data, ignorar esta validação
            pass
    
    return True
