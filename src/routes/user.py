from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from ..models.user import User
from ..models.db import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/registrar', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('member.profile'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        full_name = request.form.get('full_name')
        
        # Validações básicas
        if not username or not email or not password or not confirm_password or not full_name:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return render_template('register.html')
        
        # Verificar se o usuário já existe
        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash('Nome de usuário já está em uso.', 'danger')
            return render_template('register.html')
        
        # Verificar se o email já existe
        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash('Email já está em uso.', 'danger')
            return render_template('register.html')
        
        # Criar novo usuário
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            full_name=full_name,
            is_admin=False,
            is_approved=False  # Usuário precisa ser aprovado por um administrador
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registro realizado com sucesso! Aguarde a aprovação de um administrador.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@user_bp.route('/alterar-senha', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Validações básicas
        if not current_password or not new_password or not confirm_password:
            flash('Todos os campos são obrigatórios.', 'danger')
            return render_template('change_password.html')
        
        if new_password != confirm_password:
            flash('As senhas não coincidem.', 'danger')
            return render_template('change_password.html')
        
        # Verificar se a senha atual está correta
        if not check_password_hash(current_user.password, current_password):
            flash('Senha atual incorreta.', 'danger')
            return render_template('change_password.html')
        
        # Atualizar a senha
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        
        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('member.profile'))
    
    return render_template('change_password.html')
