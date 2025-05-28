from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash, current_app
from src.models.db import db
from src.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import logging
from flask_login import login_user, logout_user, login_required, current_user

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
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
            flash('Dados de login inválidos', 'error')
            return redirect(url_for('auth.login'))
        
        username = data.get('username')
        password = data.get('password')
        remember = data.get('remember', False)
        
        if not username or not password:
            if is_ajax:
                return jsonify({'success': False, 'message': 'Por favor, forneça nome de usuário e senha'}), 400
            flash('Por favor, forneça nome de usuário e senha', 'error')
            return redirect(url_for('auth.login'))
        
        user = User.query.filter_by(username=username).first()
        
        if not user or not check_password_hash(user.password, password):
            if is_ajax:
                return jsonify({'success': False, 'message': 'Credenciais inválidas. Tente novamente.'}), 401
            flash('Credenciais inválidas. Tente novamente.', 'error')
            return redirect(url_for('auth.login'))
        
        # Atualizar último login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Usar Flask-Login para autenticação
        login_user(user, remember=remember)
        
        # Criar sessão (mantido para compatibilidade)
        session['user_id'] = user.id
        session['username'] = user.username
        session['is_admin'] = user.is_admin
        
        logger.info(f"Login bem-sucedido para o usuário: {username}")
        
        # Responder de acordo com o tipo de requisição
        if is_ajax:
            return jsonify({
                'success': True, 
                'message': 'Login bem-sucedido',
                'redirect': url_for('member.profile')
            }), 200
        
        # Redirecionar para a página de perfil do membro
        return redirect(url_for('member.profile'))

# Adicionar rota /api/auth/login para compatibilidade com o frontend
@auth_bp.route('/api/auth/login', methods=['POST'])
def api_login():
    # Verificar se a requisição é AJAX/JSON
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
    
    # Obter dados do formulário ou JSON
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    
    username = data.get('username')
    password = data.get('password')
    remember = data.get('remember', False)
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Por favor, forneça nome de usuário e senha'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': 'Credenciais inválidas. Tente novamente.'}), 401
    
    # Atualizar último login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Usar Flask-Login para autenticação
    login_user(user, remember=remember)
    
    # Criar sessão (mantido para compatibilidade)
    session['user_id'] = user.id
    session['username'] = user.username
    session['is_admin'] = user.is_admin
    
    logger.info(f"Login API bem-sucedido para o usuário: {username}")
    
    return jsonify({
        'success': True, 
        'message': 'Login bem-sucedido',
        'redirect': url_for('member.profile')
    }), 200

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    # Verificar se a requisição é AJAX/JSON
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
    
    # Usar Flask-Login para logout
    logout_user()
    
    # Limpar sessão (mantido para compatibilidade)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    
    logger.info("Logout realizado")
    
    if is_ajax:
        return jsonify({
            'success': True, 
            'message': 'Logout realizado com sucesso',
            'redirect': url_for('index')
        }), 200
    
    return redirect(url_for('index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
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
                return jsonify({'success': False, 'message': 'Dados de registro inválidos'}), 400
            flash('Dados de registro inválidos', 'error')
            return redirect(url_for('auth.register'))
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if not username or not email or not password or not confirm_password:
            if is_ajax:
                return jsonify({'success': False, 'message': 'Por favor, preencha todos os campos obrigatórios'}), 400
            flash('Por favor, preencha todos os campos obrigatórios', 'error')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            if is_ajax:
                return jsonify({'success': False, 'message': 'As senhas não coincidem'}), 400
            flash('As senhas não coincidem', 'error')
            return redirect(url_for('auth.register'))
        
        # Verificar se o usuário já existe
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            if is_ajax:
                return jsonify({'success': False, 'message': 'Nome de usuário já está em uso'}), 409
            flash('Nome de usuário já está em uso', 'error')
            return redirect(url_for('auth.register'))
        
        # Verificar se o email já existe
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            if is_ajax:
                return jsonify({'success': False, 'message': 'Email já está em uso'}), 409
            flash('Email já está em uso', 'error')
            return redirect(url_for('auth.register'))
        
        # Criar novo usuário
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            full_name=data.get('full_name', ''),
            nickname=data.get('nickname', username),
            is_admin=False,
            is_approved=False  # Requer aprovação de administrador
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        logger.info(f"Novo usuário registrado: {username}")
        
        if is_ajax:
            return jsonify({
                'success': True, 
                'message': 'Registro realizado com sucesso! Aguarde aprovação do administrador.',
                'redirect': url_for('auth.login')
            }), 201
        
        flash('Registro realizado com sucesso! Aguarde aprovação do administrador.', 'success')
        return redirect(url_for('auth.login'))
