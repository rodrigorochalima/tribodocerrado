from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid
import logging
import base64
import re
from PIL import Image
from io import BytesIO
from src.models.db import db

member_bp = Blueprint('member', __name__, url_prefix='/membro')

@member_bp.route('/perfil')
@login_required
def profile():
    # Garantir que a imagem padrão existe
    default_image_path = os.path.join(current_app.static_folder, 'images', 'profiles', 'default.jpg')
    if not os.path.exists(default_image_path):
        os.makedirs(os.path.dirname(default_image_path), exist_ok=True)
        try:
            # Criar uma imagem padrão simples
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (200, 200), color=(73, 109, 137))
            d = ImageDraw.Draw(img)
            d.text((20, 70), "Tribo do Cerrado", fill=(255, 255, 0))
            d.text((20, 120), "Perfil", fill=(255, 255, 0))
            img.save(default_image_path)
        except Exception as e:
            logging.error(f"Erro ao criar imagem padrão: {str(e)}")
    
    return render_template('member_profile.html', user=current_user)

@member_bp.route('/editar-perfil', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            full_name = request.form.get('full_name')
            nickname = request.form.get('nickname')
            birth_date = request.form.get('birth_date')
            blood_type = request.form.get('blood_type')
            address_street = request.form.get('address_street')
            address_number = request.form.get('address_number')
            address_complement = request.form.get('address_complement')
            address_district = request.form.get('address_district')
            address_city = request.form.get('address_city', 'Goiânia')
            address_state = request.form.get('address_state', 'GO')
            address_zipcode = request.form.get('address_zipcode')
            health_notes = request.form.get('health_notes')
            health_insurance = request.form.get('health_insurance')
            health_insurance_number = request.form.get('health_insurance_number')
            
            # Obter configurações de privacidade
            is_public_profile = 'is_public_profile' in request.form
            is_public_full_name = 'is_public_full_name' in request.form
            is_public_birth_date = 'is_public_birth_date' in request.form
            is_public_blood_type = 'is_public_blood_type' in request.form
            is_public_address = 'is_public_address' in request.form
            is_public_health_info = 'is_public_health_info' in request.form
            is_public_collection_date = 'is_public_collection_date' in request.form
            is_public_join_date = 'is_public_join_date' in request.form
            
            # Salvar o valor atual da imagem de perfil para preservá-lo caso não seja enviada uma nova imagem
            current_profile_image = current_user.profile_image
            
            # Processar imagem recortada se disponível
            cropped_image_data = request.form.get('cropped_image_data')
            if cropped_image_data and cropped_image_data.startswith('data:image'):
                # Criar diretórios se não existirem
                upload_folder = os.path.join(current_app.static_folder, 'uploads', 'profile')
                os.makedirs(upload_folder, exist_ok=True)
                
                # Extrair dados da imagem base64
                image_data = re.sub('^data:image/.+;base64,', '', cropped_image_data)
                
                # Importar Image aqui para garantir que está disponível no escopo correto
                from PIL import Image
                image = Image.open(BytesIO(base64.b64decode(image_data)))
                
                # Gerar nome de arquivo único
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"{current_user.id}_{int(datetime.now().timestamp())}_{timestamp}.jpg"
                
                # Salvar arquivo
                file_path = os.path.join(upload_folder, filename)
                image.save(file_path, 'JPEG')
                
                # Atualizar caminho da imagem no banco de dados
                current_user.profile_image = f"/static/uploads/profile/{filename}"
            
            # Processar upload de imagem tradicional (fallback)
            elif 'profile_image' in request.files and request.files['profile_image'].filename:
                profile_image = request.files['profile_image']
                
                # Criar diretórios se não existirem
                upload_folder = os.path.join(current_app.static_folder, 'uploads', 'profile')
                os.makedirs(upload_folder, exist_ok=True)
                
                # Gerar nome de arquivo único
                filename = secure_filename(profile_image.filename)
                timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
                filename = f"{current_user.id}_{int(datetime.now().timestamp())}_{filename}"
                
                # Salvar arquivo
                file_path = os.path.join(upload_folder, filename)
                profile_image.save(file_path)
                
                # Atualizar caminho da imagem no banco de dados
                current_user.profile_image = f"/static/uploads/profile/{filename}"
            else:
                # Se nenhuma nova imagem foi enviada, preservar a imagem atual
                current_user.profile_image = current_profile_image
            
            # Atualizar dados do usuário
            current_user.full_name = full_name
            current_user.nickname = nickname
            
            # Converter data de nascimento para objeto Date se não for vazio
            if birth_date:
                try:
                    current_user.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
                except ValueError:
                    pass
            
            current_user.blood_type = blood_type
            current_user.address_street = address_street
            current_user.address_number = address_number
            current_user.address_complement = address_complement
            current_user.address_district = address_district
            current_user.address_city = address_city
            current_user.address_state = address_state
            current_user.address_zipcode = address_zipcode
            current_user.health_notes = health_notes
            current_user.health_insurance = health_insurance
            current_user.health_insurance_number = health_insurance_number
            
            # Atualizar configurações de privacidade
            current_user.is_public_profile = is_public_profile
            current_user.is_public_full_name = is_public_full_name
            current_user.is_public_birth_date = is_public_birth_date
            current_user.is_public_blood_type = is_public_blood_type
            current_user.is_public_address = is_public_address
            current_user.is_public_health_info = is_public_health_info
            current_user.is_public_collection_date = is_public_collection_date
            current_user.is_public_join_date = is_public_join_date
            
            # Salvar alterações no banco de dados
            db.session.commit()
            
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('member.profile'))
            
        except Exception as e:
            logging.error(f"Erro ao atualizar perfil: {str(e)}")
            flash(f'Erro ao atualizar perfil. Por favor, tente novamente.', 'danger')
    
    # Garantir que a imagem padrão existe
    default_image_path = os.path.join(current_app.static_folder, 'images', 'profiles', 'default.jpg')
    if not os.path.exists(default_image_path):
        os.makedirs(os.path.dirname(default_image_path), exist_ok=True)
        try:
            # Criar uma imagem padrão simples
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (200, 200), color=(73, 109, 137))
            d = ImageDraw.Draw(img)
            d.text((20, 70), "Tribo do Cerrado", fill=(255, 255, 0))
            d.text((20, 120), "Perfil", fill=(255, 255, 0))
            img.save(default_image_path)
        except Exception as e:
            logging.error(f"Erro ao criar imagem padrão: {str(e)}")
    
    return render_template('member_edit_profile.html', user=current_user)

@member_bp.route('/minhas-motos')
@login_required
def my_motorcycles():
    return render_template('member_motorcycles.html')

@member_bp.route('/minha-familia')
@login_required
def my_family():
    return render_template('member_family.html')

@member_bp.route('/minha-galeria')
@login_required
def my_gallery():
    return render_template('member_gallery.html')

@member_bp.route('/configuracoes')
@login_required
def settings():
    return render_template('member_settings.html')

@member_bp.route('/alterar-senha')
@login_required
def change_password():
    return render_template('member_change_password.html')
