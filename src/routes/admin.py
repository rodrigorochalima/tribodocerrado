from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..models.user import User
from ..models.db import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('member.profile'))
    
    # Buscar todos os usuários
    users = User.query.all()
    
    return render_template('admin/dashboard.html', users=users)

@admin_bp.route('/usuarios', methods=['GET'])
@login_required
def users():
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('member.profile'))
    
    # Buscar todos os usuários
    users = User.query.all()
    
    return render_template('admin/users.html', users=users)

@admin_bp.route('/usuario/<int:user_id>', methods=['GET'])
@login_required
def user_detail(user_id):
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('member.profile'))
    
    # Buscar o usuário pelo ID
    user = User.query.get_or_404(user_id)
    
    return render_template('admin/user_detail.html', user=user)

@admin_bp.route('/usuario/<int:user_id>/aprovar', methods=['POST'])
@login_required
def approve_user(user_id):
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('member.profile'))
    
    # Buscar o usuário pelo ID
    user = User.query.get_or_404(user_id)
    
    # Aprovar o usuário
    user.is_approved = True
    db.session.commit()
    
    flash(f'Usuário {user.username} aprovado com sucesso!', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/usuario/<int:user_id>/rejeitar', methods=['POST'])
@login_required
def reject_user(user_id):
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('member.profile'))
    
    # Buscar o usuário pelo ID
    user = User.query.get_or_404(user_id)
    
    # Rejeitar o usuário
    user.is_approved = False
    db.session.commit()
    
    flash(f'Usuário {user.username} rejeitado com sucesso!', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/usuario/<int:user_id>/excluir', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'danger')
        return redirect(url_for('member.profile'))
    
    # Buscar o usuário pelo ID
    user = User.query.get_or_404(user_id)
    
    # Não permitir excluir o próprio administrador
    if user.id == current_user.id:
        flash('Você não pode excluir seu próprio usuário!', 'danger')
        return redirect(url_for('admin.users'))
    
    # Excluir o usuário
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Usuário {user.username} excluído com sucesso!', 'success')
    return redirect(url_for('admin.users'))
