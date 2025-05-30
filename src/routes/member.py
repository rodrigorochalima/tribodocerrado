from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import login_required, current_user
from src.models.user import User
from src.models.motorcycle import Motorcycle, MotorcycleImage
from src.models.db import db
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid
import base64
from PIL import Image
from io import BytesIO

member_bp = Blueprint('member', __name__)

# Decorator personalizado para verificar se o email foi confirmado
def email_confirmed_required(f):
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.email_confirmed:
            flash('Por favor, confirme seu email antes de acessar esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@member_bp.route('/profile')
@login_required
def profile():
    # Mesmo usuários não confirmados podem ver o perfil, mas não editar
    if not current_user.email_confirmed:
        flash('Por favor, confirme seu email para ativar todas as funcionalidades do seu perfil.', 'warning')
    
    return render_template('member_profile.html', user=current_user)

@member_bp.route('/edit-profile', methods=['GET', 'POST'])
@email_confirmed_required
def edit_profile():
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            full_name = request.form.get('full_name')
            nickname = request.form.get('nickname')
            birth_date = request.form.get('birth_date')
            blood_type = request.form.get('blood_type')
            
            # Endereço
            address_street = request.form.get('address_street')
            address_number = request.form.get('address_number')
            address_complement = request.form.get('address_complement')
            address_district = request.form.get('address_district')
            address_city = request.form.get('address_city')
            address_state = request.form.get('address_state')
            address_zipcode = request.form.get('address_zipcode')
            
            # Informações de saúde
            health_notes = request.form.get('health_notes')
            health_insurance = request.form.get('health_insurance')
            health_insurance_number = request.form.get('health_insurance_number')
            
            # Configurações de privacidade
            is_public_profile = 'is_public_profile' in request.form
            is_public_full_name = 'is_public_full_name' in request.form
            is_public_birth_date = 'is_public_birth_date' in request.form
            is_public_blood_type = 'is_public_blood_type' in request.form
            is_public_address = 'is_public_address' in request.form
            is_public_health_info = 'is_public_health_info' in request.form
            is_public_collection_date = 'is_public_collection_date' in request.form
            is_public_join_date = 'is_public_join_date' in request.form
            
            # Imagem de perfil
            cropped_image_data = request.form.get('cropped_image_data')
            
            # Atualizar usuário
            user = current_user
            
            # Dados básicos
            user.full_name = full_name
            user.nickname = nickname
            
            # Data de nascimento
            if birth_date:
                user.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
            
            user.blood_type = blood_type
            
            # Endereço
            user.address_street = address_street
            user.address_number = address_number
            user.address_complement = address_complement
            user.address_district = address_district
            user.address_city = address_city
            user.address_state = address_state
            user.address_zipcode = address_zipcode
            
            # Informações de saúde
            user.health_notes = health_notes
            user.health_insurance = health_insurance
            user.health_insurance_number = health_insurance_number
            
            # Configurações de privacidade
            user.is_public_profile = is_public_profile
            user.is_public_full_name = is_public_full_name
            user.is_public_birth_date = is_public_birth_date
            user.is_public_blood_type = is_public_blood_type
            user.is_public_address = is_public_address
            user.is_public_health_info = is_public_health_info
            user.is_public_collection_date = is_public_collection_date
            user.is_public_join_date = is_public_join_date
            
            # Processar imagem de perfil
            if cropped_image_data and cropped_image_data.startswith('data:image'):
                # Extrair dados da imagem base64
                format, imgstr = cropped_image_data.split(';base64,')
                ext = format.split('/')[-1]
                
                # Gerar nome de arquivo único
                filename = f"{uuid.uuid4()}.{ext}"
                
                # Caminho para salvar a imagem
                upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', 'uploads', 'profiles')
                os.makedirs(upload_folder, exist_ok=True)
                filepath = os.path.join(upload_folder, filename)
                
                # Salvar imagem
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(imgstr))
                
                # Atualizar caminho da imagem no usuário
                user.profile_image = f"uploads/profiles/{filename}"
            
            # Salvar alterações
            user.updated_at = datetime.utcnow()
            db.session.commit()
            
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('member.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar perfil: {str(e)}', 'danger')
            return redirect(url_for('member.edit_profile'))
    
    return render_template('member_edit_profile.html', user=current_user)

@member_bp.route('/motorcycles')
@email_confirmed_required
def motorcycles():
    motorcycles = Motorcycle.query.filter_by(user_id=current_user.id).all()
    return render_template('member_motorcycles.html', motorcycles=motorcycles)

@member_bp.route('/add-motorcycle', methods=['GET', 'POST'])
@email_confirmed_required
def add_motorcycle():
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            brand = request.form.get('brand')
            model = request.form.get('model')
            year = request.form.get('year')
            license_plate = request.form.get('license_plate')
            color = request.form.get('color')
            nickname = request.form.get('nickname')
            description = request.form.get('description')
            
            # Validações básicas
            if not brand or not model or not year:
                flash('Marca, modelo e ano são campos obrigatórios', 'danger')
                return redirect(url_for('member.add_motorcycle'))
            
            # Criar nova moto
            new_motorcycle = Motorcycle(
                user_id=current_user.id,
                brand=brand,
                model=model,
                year=year,
                license_plate=license_plate,
                color=color,
                nickname=nickname,
                description=description,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.session.add(new_motorcycle)
            db.session.commit()
            
            # Processar imagens
            images = request.files.getlist('images')
            
            if images and images[0].filename:
                upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', 'uploads', 'motorcycles')
                os.makedirs(upload_folder, exist_ok=True)
                
                for image in images:
                    if image and image.filename:
                        filename = secure_filename(image.filename)
                        # Gerar nome único para evitar conflitos
                        unique_filename = f"{uuid.uuid4()}_{filename}"
                        filepath = os.path.join(upload_folder, unique_filename)
                        
                        # Salvar imagem
                        image.save(filepath)
                        
                        # Criar miniatura
                        img = Image.open(filepath)
                        img.thumbnail((300, 300))
                        thumb_filename = f"thumb_{unique_filename}"
                        thumb_path = os.path.join(upload_folder, thumb_filename)
                        img.save(thumb_path)
                        
                        # Adicionar imagem ao banco de dados
                        motorcycle_image = MotorcycleImage(
                            motorcycle_id=new_motorcycle.id,
                            image_path=f"uploads/motorcycles/{unique_filename}",
                            thumbnail_path=f"uploads/motorcycles/{thumb_filename}",
                            created_at=datetime.utcnow()
                        )
                        
                        db.session.add(motorcycle_image)
            
            db.session.commit()
            
            flash('Motocicleta adicionada com sucesso!', 'success')
            return redirect(url_for('member.motorcycles'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao adicionar motocicleta: {str(e)}', 'danger')
            return redirect(url_for('member.add_motorcycle'))
    
    return render_template('member_add_motorcycle.html')

@member_bp.route('/edit-motorcycle/<int:id>', methods=['GET', 'POST'])
@email_confirmed_required
def edit_motorcycle(id):
    motorcycle = Motorcycle.query.get_or_404(id)
    
    # Verificar se a moto pertence ao usuário atual
    if motorcycle.user_id != current_user.id:
        abort(403)
    
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            brand = request.form.get('brand')
            model = request.form.get('model')
            year = request.form.get('year')
            license_plate = request.form.get('license_plate')
            color = request.form.get('color')
            nickname = request.form.get('nickname')
            description = request.form.get('description')
            
            # Validações básicas
            if not brand or not model or not year:
                flash('Marca, modelo e ano são campos obrigatórios', 'danger')
                return redirect(url_for('member.edit_motorcycle', id=id))
            
            # Atualizar moto
            motorcycle.brand = brand
            motorcycle.model = model
            motorcycle.year = year
            motorcycle.license_plate = license_plate
            motorcycle.color = color
            motorcycle.nickname = nickname
            motorcycle.description = description
            motorcycle.updated_at = datetime.utcnow()
            
            # Processar imagens
            images = request.files.getlist('images')
            
            if images and images[0].filename:
                upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', 'uploads', 'motorcycles')
                os.makedirs(upload_folder, exist_ok=True)
                
                for image in images:
                    if image and image.filename:
                        filename = secure_filename(image.filename)
                        # Gerar nome único para evitar conflitos
                        unique_filename = f"{uuid.uuid4()}_{filename}"
                        filepath = os.path.join(upload_folder, unique_filename)
                        
                        # Salvar imagem
                        image.save(filepath)
                        
                        # Criar miniatura
                        img = Image.open(filepath)
                        img.thumbnail((300, 300))
                        thumb_filename = f"thumb_{unique_filename}"
                        thumb_path = os.path.join(upload_folder, thumb_filename)
                        img.save(thumb_path)
                        
                        # Adicionar imagem ao banco de dados
                        motorcycle_image = MotorcycleImage(
                            motorcycle_id=motorcycle.id,
                            image_path=f"uploads/motorcycles/{unique_filename}",
                            thumbnail_path=f"uploads/motorcycles/{thumb_filename}",
                            created_at=datetime.utcnow()
                        )
                        
                        db.session.add(motorcycle_image)
            
            db.session.commit()
            
            flash('Motocicleta atualizada com sucesso!', 'success')
            return redirect(url_for('member.motorcycles'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar motocicleta: {str(e)}', 'danger')
            return redirect(url_for('member.edit_motorcycle', id=id))
    
    return render_template('member_edit_motorcycle.html', motorcycle=motorcycle)

@member_bp.route('/delete-motorcycle/<int:id>', methods=['POST'])
@email_confirmed_required
def delete_motorcycle(id):
    motorcycle = Motorcycle.query.get_or_404(id)
    
    # Verificar se a moto pertence ao usuário atual
    if motorcycle.user_id != current_user.id:
        abort(403)
    
    try:
        # Excluir imagens associadas
        for image in motorcycle.images:
            # Remover arquivos físicos
            try:
                image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', image.image_path)
                thumb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', image.thumbnail_path)
                
                if os.path.exists(image_path):
                    os.remove(image_path)
                
                if os.path.exists(thumb_path):
                    os.remove(thumb_path)
            except:
                pass
            
            db.session.delete(image)
        
        # Excluir moto
        db.session.delete(motorcycle)
        db.session.commit()
        
        flash('Motocicleta excluída com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir motocicleta: {str(e)}', 'danger')
    
    return redirect(url_for('member.motorcycles'))

@member_bp.route('/delete-motorcycle-image/<int:id>', methods=['POST'])
@email_confirmed_required
def delete_motorcycle_image(id):
    image = MotorcycleImage.query.get_or_404(id)
    motorcycle = Motorcycle.query.get_or_404(image.motorcycle_id)
    
    # Verificar se a moto pertence ao usuário atual
    if motorcycle.user_id != current_user.id:
        abort(403)
    
    try:
        # Remover arquivos físicos
        try:
            image_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', image.image_path)
            thumb_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', image.thumbnail_path)
            
            if os.path.exists(image_path):
                os.remove(image_path)
            
            if os.path.exists(thumb_path):
                os.remove(thumb_path)
        except:
            pass
        
        # Excluir imagem do banco de dados
        db.session.delete(image)
        db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@member_bp.route('/settings', methods=['GET', 'POST'])
@email_confirmed_required
def settings():
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')
            
            # Validações
            if not current_password:
                flash('Senha atual é obrigatória', 'danger')
                return redirect(url_for('member.settings'))
            
            if not current_user.check_password(current_password):
                flash('Senha atual incorreta', 'danger')
                return redirect(url_for('member.settings'))
            
            if new_password:
                if new_password != confirm_password:
                    flash('As novas senhas não coincidem', 'danger')
                    return redirect(url_for('member.settings'))
                
                # Validar força da senha
                from src.routes.auth import validate_password_strength
                birth_date = current_user.birth_date.strftime('%Y-%m-%d') if current_user.birth_date else None
                
                if not validate_password_strength(new_password, birth_date):
                    flash('A nova senha não atende aos requisitos de segurança', 'danger')
                    return redirect(url_for('member.settings'))
                
                # Atualizar senha
                current_user.set_password(new_password)
                current_user.updated_at = datetime.utcnow()
                db.session.commit()
                
                flash('Senha atualizada com sucesso!', 'success')
            
            return redirect(url_for('member.profile'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar configurações: {str(e)}', 'danger')
            return redirect(url_for('member.settings'))
    
    return render_template('member_settings.html')

@member_bp.route('/family')
@email_confirmed_required
def family():
    # Implementação futura
    return render_template('member_family.html')

@member_bp.route('/add-family', methods=['GET', 'POST'])
@email_confirmed_required
def add_family():
    # Implementação futura
    return render_template('member_add_family.html')

@member_bp.route('/gallery')
@email_confirmed_required
def gallery():
    # Implementação futura
    return render_template('member_gallery.html')

@member_bp.route('/card')
@email_confirmed_required
def card():
    return render_template('member_card.html', user=current_user)
