from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from src.models.db import db
from src.models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import logging

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
        
        # Criar sessão
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
    
    if not data:
        return jsonify({'success': False, 'message': 'Dados de login inválidos'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'success': False, 'message': 'Por favor, forneça nome de usuário e senha'}), 400
    
    user = User.query.filter_by(username=username).first()
    
    if not user or not check_password_hash(user.password, password):
        return jsonify({'success': False, 'message': 'Credenciais inválidas. Tente novamente.'}), 401
    
    # Atualizar último login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Criar sessão
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
    
    # Limpar sessão
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
                'message': 'Registro realizado com sucesso! Aguarde a aprovação de um administrador.',
                'redirect': url_for('auth.login')
            }), 201
        
        flash('Registro realizado com sucesso! Aguarde a aprovação de um administrador.', 'success')
        return redirect(url_for('auth.login'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')
    
    if request.method == 'POST':
        # Verificar se a requisição é AJAX/JSON
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
        
        # Obter dados do formulário ou JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        if not data or not data.get('email'):
            if is_ajax:
                return jsonify({'success': False, 'message': 'Por favor, forneça seu email'}), 400
            flash('Por favor, forneça seu email', 'error')
            return redirect(url_for('auth.forgot_password'))
        
        email = data.get('email')
        user = User.query.filter_by(email=email).first()
        
        if not user:
            if is_ajax:
                return jsonify({'success': False, 'message': 'Email não encontrado'}), 404
            flash('Email não encontrado', 'error')
            return redirect(url_for('auth.forgot_password'))
        
        # Aqui seria implementado o envio de email com link para redefinição de senha
        # Por simplicidade, vamos apenas redirecionar para uma página de confirmação
        
        logger.info(f"Solicitação de redefinição de senha para: {email}")
        
        if is_ajax:
            return jsonify({
                'success': True, 
                'message': 'Instruções para redefinição de senha foram enviadas para seu email',
                'redirect': url_for('auth.login')
            }), 200
        
        flash('Instruções para redefinição de senha foram enviadas para seu email', 'success')
        return redirect(url_for('auth.login'))

@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # Verificar se a requisição é AJAX/JSON
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
    
    # Aqui seria implementada a validação do token e redefinição de senha
    # Por simplicidade, vamos apenas redirecionar para a página de login
    
    if is_ajax:
        return jsonify({
            'success': True, 
            'message': 'Sua senha foi redefinida com sucesso!',
            'redirect': url_for('auth.login')
        }), 200
    
    flash('Sua senha foi redefinida com sucesso!', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/change-password', methods=['GET', 'POST'])
def change_password():
    # Verificar se a requisição é AJAX/JSON
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
    
    if 'user_id' not in session:
        if is_ajax:
            return jsonify({'success': False, 'message': 'Usuário não autenticado', 'redirect': url_for('auth.login')}), 401
        return redirect(url_for('auth.login'))
    
    if request.method == 'GET':
        return render_template('change_password.html')
    
    if request.method == 'POST':
        # Obter dados do formulário ou JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        if not data:
            if is_ajax:
                return jsonify({'success': False, 'message': 'Dados inválidos'}), 400
            flash('Dados inválidos', 'error')
            return redirect(url_for('auth.change_password'))
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        
        if not current_password or not new_password or not confirm_password:
            if is_ajax:
                return jsonify({'success': False, 'message': 'Por favor, preencha todos os campos'}), 400
            flash('Por favor, preencha todos os campos', 'error')
            return redirect(url_for('auth.change_password'))
        
        if new_password != confirm_password:
            if is_ajax:
                return jsonify({'success': False, 'message': 'As senhas não coincidem'}), 400
            flash('As senhas não coincidem', 'error')
            return redirect(url_for('auth.change_password'))
        
        user = User.query.get(session['user_id'])
        
        if not user or not check_password_hash(user.password, current_password):
            if is_ajax:
                return jsonify({'success': False, 'message': 'Senha atual incorreta'}), 401
            flash('Senha atual incorreta', 'error')
            return redirect(url_for('auth.change_password'))
        
        # Atualizar senha
        user.password = generate_password_hash(new_password)
        db.session.commit()
        
        logger.info(f"Senha alterada para o usuário: {user.username}")
        
        if is_ajax:
            return jsonify({
                'success': True, 
                'message': 'Senha alterada com sucesso!',
                'redirect': url_for('member.profile')
            }), 200
        
        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('member.profile'))

@auth_bp.route('/api/setup-admin', methods=['GET', 'POST'])
def setup_admin():
    if request.method == 'GET':
        # Verificar se já existe algum administrador
        admin_exists = User.query.filter_by(is_admin=True).first()
        
        if admin_exists:
            flash('Um administrador já existe no sistema.', 'error')
            return redirect(url_for('index'))
        
        return render_template('setup_admin.html')
    
    if request.method == 'POST':
        # Verificar se a requisição é AJAX/JSON
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json
        
        # Obter dados do formulário ou JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            if is_ajax:
                return jsonify({'success': False, 'message': 'Dados incompletos. Por favor, forneça nome de usuário, email e senha.'}), 400
            flash('Dados incompletos. Por favor, forneça nome de usuário, email e senha.', 'error')
            return redirect(url_for('auth.setup_admin'))
        
        # Verificar se já existe algum administrador
        admin_exists = User.query.filter_by(is_admin=True).first()
        
        if admin_exists:
            if is_ajax:
                return jsonify({'success': False, 'message': 'Um administrador já existe no sistema.', 'redirect': url_for('index')}), 409
            flash('Um administrador já existe no sistema.', 'error')
            return redirect(url_for('index'))
        
        # Criar o primeiro administrador
        admin_user = User(
            username=data.get('username'),
            email=data.get('email'),
            password=generate_password_hash(data.get('password')),
            full_name=data.get('full_name', 'Administrador'),
            nickname=data.get('nickname', data.get('username')),
            is_admin=True,
            is_approved=True
        )
        
        db.session.add(admin_user)
        db.session.commit()
        
        logger.info(f"Administrador inicial criado: {data.get('username')}")
        
        if is_ajax:
            return jsonify({
                'success': True, 
                'message': 'Administrador inicial criado com sucesso!',
                'redirect': url_for('auth.login')
            }), 201
        
        flash('Administrador inicial criado com sucesso!', 'success')
        return redirect(url_for('auth.login'))

# Endpoint para verificar status de autenticação
@auth_bp.route('/api/auth/status', methods=['GET'])
def auth_status():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return jsonify({
                'authenticated': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_admin': user.is_admin,
                    'nickname': user.nickname
                }
            }), 200
    
    return jsonify({'authenticated': False}), 200

# Endpoint para verificar sessão
@auth_bp.route('/api/auth/check-session', methods=['GET'])
def check_session():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            return jsonify({
                'authenticated': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'is_admin': user.is_admin,
                    'nickname': user.nickname
                }
            }), 200
    
    return jsonify({'authenticated': False}), 200
