from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user
from src.models.user import User
from datetime import datetime
from src.models.db import db

auth_bp = Blueprint('auth', __name__)

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
        
        # Buscar usuário por nome de usuário ou email
        user = User.query.filter_by(username=username).first()
        if not user:
            # Tentar buscar por email
            user = User.query.filter_by(email=username).first()
        
        if user and check_password_hash(user.password, password):
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
            if is_ajax:
                return jsonify({'success': False, 'message': 'Nome de usuário ou senha inválidos'}), 401
            flash('Nome de usuário ou senha inválidos', 'error')
            return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Você saiu com sucesso', 'info')
    return redirect(url_for('home.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    # Lógica de registro aqui
    return redirect(url_for('auth.login'))
