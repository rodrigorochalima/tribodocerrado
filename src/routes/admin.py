from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from src.models.db import db
from src.models.user import User
from src.utils.auth import login_required, admin_required
from datetime import datetime
import logging

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
logger = logging.getLogger(__name__)

@admin_bp.route('/dashboard', methods=['GET'])
@login_required
@admin_required
def dashboard():
    """Renderiza o painel de administração"""
    return render_template('admin/dashboard.html')

@admin_bp.route('/users', methods=['GET'])
@login_required
@admin_required
def list_users():
    """Lista todos os usuários do sistema"""
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>/approve', methods=['POST'])
@login_required
@admin_required
def approve_user(user_id):
    """Aprova um usuário pendente"""
    user = User.query.get(user_id)
    
    if not user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Usuário não encontrado'}), 404
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('admin.list_users'))
    
    user.is_approved = True
    db.session.commit()
    
    logger.info(f"Usuário {user.username} aprovado pelo administrador {session.get('username')}")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': f'Usuário {user.username} aprovado com sucesso'})
    
    flash(f'Usuário {user.username} aprovado com sucesso', 'success')
    return redirect(url_for('admin.list_users'))

@admin_bp.route('/users/<int:user_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_user(user_id):
    """Rejeita um usuário pendente"""
    user = User.query.get(user_id)
    
    if not user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Usuário não encontrado'}), 404
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('admin.list_users'))
    
    # Armazenar informações para log
    username = user.username
    admin_username = session.get('username')
    
    # Excluir o usuário
    db.session.delete(user)
    db.session.commit()
    
    logger.info(f"Usuário {username} rejeitado pelo administrador {admin_username}")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': f'Usuário {username} rejeitado com sucesso'})
    
    flash(f'Usuário {username} rejeitado com sucesso', 'success')
    return redirect(url_for('admin.list_users'))

@admin_bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    """Alterna o status de administrador de um usuário"""
    # Não permitir que um administrador remova seus próprios privilégios
    if user_id == session.get('user_id'):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Você não pode remover seus próprios privilégios de administrador'}), 403
        flash('Você não pode remover seus próprios privilégios de administrador', 'error')
        return redirect(url_for('admin.list_users'))
    
    user = User.query.get(user_id)
    
    if not user:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'message': 'Usuário não encontrado'}), 404
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('admin.list_users'))
    
    # Alternar status de administrador
    user.is_admin = not user.is_admin
    db.session.commit()
    
    action = "promovido a administrador" if user.is_admin else "removido de administrador"
    logger.info(f"Usuário {user.username} {action} pelo administrador {session.get('username')}")
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'message': f'Usuário {user.username} {action} com sucesso'})
    
    flash(f'Usuário {user.username} {action} com sucesso', 'success')
    return redirect(url_for('admin.list_users'))

@admin_bp.route('/pending-users', methods=['GET'])
@login_required
@admin_required
def pending_users():
    """Lista usuários pendentes de aprovação"""
    users = User.query.filter_by(is_approved=False).all()
    return render_template('admin/pending_users.html', users=users)

@admin_bp.route('/statistics', methods=['GET'])
@login_required
@admin_required
def statistics():
    """Exibe estatísticas do sistema"""
    total_users = User.query.count()
    approved_users = User.query.filter_by(is_approved=True).count()
    pending_users = User.query.filter_by(is_approved=False).count()
    admin_users = User.query.filter_by(is_admin=True).count()
    
    stats = {
        'total_users': total_users,
        'approved_users': approved_users,
        'pending_users': pending_users,
        'admin_users': admin_users
    }
    
    return render_template('admin/statistics.html', stats=stats)
