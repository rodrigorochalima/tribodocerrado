from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from ..models.db import db
from ..models.user import User

member_bp = Blueprint('member', __name__)

@member_bp.route('/perfil', methods=['GET'])
@login_required
def profile():
    if current_user.is_admin:
        return redirect(url_for('admin.dashboard'))
    return render_template('member_profile.html', user=current_user)

@member_bp.route('/editar-perfil', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        # Atualizar informações do perfil
        current_user.full_name = request.form.get('full_name')
        current_user.nickname = request.form.get('nickname')
        current_user.email = request.form.get('email')
        current_user.bio = request.form.get('bio')
        
        # Processar data de nascimento
        birth_date_str = request.form.get('birth_date')
        if birth_date_str:
            try:
                current_user.birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de data inválido para data de nascimento.', 'danger')
        
        # Processar data de coleta
        collection_date_str = request.form.get('collection_date')
        if collection_date_str:
            try:
                current_user.collection_date = datetime.strptime(collection_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de data inválido para data de coleta.', 'danger')
        
        # Outros campos
        current_user.blood_type = request.form.get('blood_type')
        current_user.address_street = request.form.get('address_street')
        current_user.address_number = request.form.get('address_number')
        current_user.address_complement = request.form.get('address_complement')
        current_user.address_district = request.form.get('address_district')
        current_user.address_city = request.form.get('address_city')
        current_user.address_state = request.form.get('address_state')
        current_user.address_zipcode = request.form.get('address_zipcode')
        current_user.health_notes = request.form.get('health_notes')
        current_user.health_insurance = request.form.get('health_insurance')
        current_user.health_insurance_number = request.form.get('health_insurance_number')
        
        # Processar imagem de perfil
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename:
                filename = secure_filename(file.filename)
                # Criar nome único para o arquivo
                unique_filename = f"{current_user.id}_{int(datetime.now().timestamp())}_{filename}"
                # Garantir que o diretório existe
                profile_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'profile')
                os.makedirs(profile_dir, exist_ok=True)
                # Salvar o arquivo
                file_path = os.path.join(profile_dir, unique_filename)
                file.save(file_path)
                # Atualizar o caminho da imagem no banco de dados
                current_user.profile_image = f"uploads/profile/{unique_filename}"
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('member.profile'))
    
    return render_template('member_edit_profile.html', user=current_user)

@member_bp.route('/configuracoes', methods=['GET'])
@login_required
def settings():
    return render_template('member_settings.html', user=current_user)

@member_bp.route('/motos', methods=['GET'])
@login_required
def motorcycles():
    # Aqui você buscaria as motos do usuário no banco de dados
    motorcycles = []  # Substitua por uma consulta real
    return render_template('member_motorcycles.html', motorcycles=motorcycles)

@member_bp.route('/motos/adicionar', methods=['GET', 'POST'])
@login_required
def add_motorcycle():
    if request.method == 'POST':
        # Lógica para adicionar uma nova moto
        flash('Moto adicionada com sucesso!', 'success')
        return redirect(url_for('member.motorcycles'))
    
    return render_template('member_add_motorcycle.html')

@member_bp.route('/familia', methods=['GET'])
@login_required
def family():
    # Aqui você buscaria os familiares do usuário no banco de dados
    family_members = []  # Substitua por uma consulta real
    return render_template('member_family.html', family_members=family_members)

@member_bp.route('/familia/adicionar', methods=['GET', 'POST'])
@login_required
def add_family_member():
    if request.method == 'POST':
        # Lógica para adicionar um novo familiar
        flash('Familiar adicionado com sucesso!', 'success')
        return redirect(url_for('member.family'))
    
    return render_template('member_add_family.html')
