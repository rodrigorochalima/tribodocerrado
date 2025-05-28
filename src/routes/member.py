from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from src.models.user import User
from src.utils.auth import login_required
import os
import logging
from werkzeug.utils import secure_filename
from datetime import datetime

member_bp = Blueprint('member', __name__, url_prefix='/membro')
logger = logging.getLogger(__name__)

# Configurações para upload de imagens
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', 'uploads', 'profile')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@member_bp.route('/perfil', methods=['GET'])
@login_required
def profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return redirect(url_for('auth.login'))
    
    return render_template('member_profile.html', user=user)

@member_bp.route('/editar-perfil', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        # Processar upload de foto
        if 'profile_image' in request.files:
            photo = request.files['profile_image']
            if photo.filename != '' and allowed_file(photo.filename):
                # Criar diretório de uploads se não existir
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                
                # Gerar nome de arquivo seguro
                filename = secure_filename(f"{user_id}_{int(datetime.now().timestamp())}_{photo.filename}")
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                
                # Salvar arquivo
                photo.save(filepath)
                
                # Atualizar caminho da foto no banco de dados
                user.profile_image = f"/static/uploads/profile/{filename}"
                
                # Commit das alterações
                from src.models.db import db
                db.session.commit()
                
                flash('Foto de perfil atualizada com sucesso!', 'success')
        
        # Atualizar outros campos do perfil
        user.full_name = request.form.get('full_name', user.full_name)
        user.nickname = request.form.get('nickname', user.nickname)
        # Não permitir alteração de email
        user.birth_date = request.form.get('birth_date', user.birth_date)
        user.blood_type = request.form.get('blood_type', user.blood_type)
        user.join_date = request.form.get('join_date', user.join_date)
        user.bio = request.form.get('bio', user.bio)
        
        # Endereço
        user.address_street = request.form.get('address_street', user.address_street)
        user.address_number = request.form.get('address_number', user.address_number)
        user.address_complement = request.form.get('address_complement', user.address_complement)
        user.address_district = request.form.get('address_district', user.address_district)
        user.address_city = request.form.get('address_city', user.address_city)
        user.address_state = request.form.get('address_state', user.address_state)
        user.address_zipcode = request.form.get('address_zipcode', user.address_zipcode)
        
        # Saúde
        user.health_insurance = request.form.get('health_insurance', user.health_insurance)
        user.health_insurance_number = request.form.get('health_insurance_number', user.health_insurance_number)
        user.health_notes = request.form.get('health_notes', user.health_notes)
        
        # Commit das alterações
        from src.models.db import db
        db.session.commit()
        
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('member.profile'))
    
    return render_template('member_edit_profile.html', user=user)

@member_bp.route('/motos', methods=['GET'])
@login_required
def motorcycles():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return redirect(url_for('auth.login'))
    
    # Buscar motos do usuário
    from src.models.motorcycle import Motorcycle
    motorcycles = Motorcycle.query.filter_by(user_id=user_id).all()
    
    return render_template('member_motorcycles.html', 
                          user=user, 
                          motorcycles=motorcycles)

@member_bp.route('/motos/adicionar', methods=['GET', 'POST'])
@login_required
def add_motorcycle():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        # Processar o formulário para adicionar moto
        from src.models.db import db
        from src.models.motorcycle import Motorcycle
        
        # Obter dados do formulário
        brand = request.form.get('brand')
        model = request.form.get('model')
        manufacturing_year = request.form.get('manufacturing_year')
        model_year = request.form.get('model_year')
        color = request.form.get('color', '')
        license_plate = request.form.get('license_plate', '')
        engine_capacity = request.form.get('engine_capacity', '')
        
        # Criar nova moto
        new_motorcycle = Motorcycle(
            user_id=user_id,
            brand=brand,
            model=model,
            manufacturing_year=manufacturing_year,
            model_year=model_year,
            color=color,
            license_plate=license_plate,
            engine_capacity=engine_capacity,
            purchase_date=request.form.get('purchase_date'),
            ipva_due_date=request.form.get('ipva_due_date'),
            insurance_company=request.form.get('insurance_company', ''),
            insurance_due_date=request.form.get('insurance_due_date'),
            last_maintenance=request.form.get('last_maintenance'),
            next_maintenance=request.form.get('next_maintenance'),
            maintenance_notes=request.form.get('maintenance_notes', ''),
            notes=request.form.get('notes', '')
        )
        
        db.session.add(new_motorcycle)
        db.session.commit()
        
        # Processar upload de foto se houver
        if 'motorcycle_image' in request.files:
            photo = request.files['motorcycle_image']
            if photo.filename != '' and allowed_file(photo.filename):
                # Criar diretório de uploads se não existir
                motorcycle_upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', 'uploads', 'motorcycles')
                os.makedirs(motorcycle_upload_folder, exist_ok=True)
                
                # Gerar nome de arquivo seguro
                filename = secure_filename(f"{user_id}_{new_motorcycle.id}_{int(datetime.now().timestamp())}_{photo.filename}")
                filepath = os.path.join(motorcycle_upload_folder, filename)
                
                # Salvar arquivo
                photo.save(filepath)
                
                # Atualizar caminho da foto no banco de dados
                new_motorcycle.image_url = f"/static/uploads/motorcycles/{filename}"
                db.session.commit()
        
        flash('Motocicleta adicionada com sucesso!', 'success')
        return redirect(url_for('member.motorcycles'))
    
    return render_template('member_add_motorcycle.html', user=user)

@member_bp.route('/familia', methods=['GET'])
@login_required
def family():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return redirect(url_for('auth.login'))
    
    # Buscar familiares do usuário
    from src.models.family import FamilyMember
    family_members = FamilyMember.query.filter_by(user_id=user_id).all()
    
    return render_template('member_family.html', 
                          user=user, 
                          family_members=family_members)

@member_bp.route('/familia/adicionar', methods=['GET', 'POST'])
@login_required
def add_family_member():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        # Processar o formulário para adicionar familiar
        from src.models.db import db
        from src.models.family import FamilyMember
        
        # Obter dados do formulário
        full_name = request.form.get('full_name')
        relationship = request.form.get('relationship')
        birth_date = request.form.get('birth_date')
        phone = request.form.get('phone', '')
        
        # Criar novo familiar
        new_family_member = FamilyMember(
            user_id=user_id,
            full_name=full_name,
            relationship=relationship,
            birth_date=birth_date,
            phone=phone,
            blood_type=request.form.get('blood_type', ''),
            health_insurance=request.form.get('health_insurance', ''),
            health_notes=request.form.get('health_notes', ''),
            notes=request.form.get('notes', '')
        )
        
        db.session.add(new_family_member)
        db.session.commit()
        
        # Processar upload de foto se houver
        if 'family_image' in request.files:
            photo = request.files['family_image']
            if photo.filename != '' and allowed_file(photo.filename):
                # Criar diretório de uploads se não existir
                family_upload_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', 'uploads', 'family')
                os.makedirs(family_upload_folder, exist_ok=True)
                
                # Gerar nome de arquivo seguro
                filename = secure_filename(f"{user_id}_{new_family_member.id}_{int(datetime.now().timestamp())}_{photo.filename}")
                filepath = os.path.join(family_upload_folder, filename)
                
                # Salvar arquivo
                photo.save(filepath)
                
                # Atualizar caminho da foto no banco de dados
                new_family_member.image_url = f"/static/uploads/family/{filename}"
                db.session.commit()
        
        flash('Familiar adicionado com sucesso!', 'success')
        return redirect(url_for('member.family'))
    
    return render_template('member_add_family.html', user=user)

@member_bp.route('/galeria', methods=['GET'])
@login_required
def gallery():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return redirect(url_for('auth.login'))
    
    # Buscar imagens da galeria
    from src.models.gallery import Gallery, GalleryImage
    
    # Buscar galerias criadas pelo usuário
    galleries = Gallery.query.filter_by(created_by_id=user_id).all()
    
    # Buscar imagens para cada galeria
    for gallery in galleries:
        gallery.image_list = GalleryImage.query.filter_by(gallery_id=gallery.id).order_by(GalleryImage.order).all()
    
    return render_template('member_gallery.html', 
                          user=user, 
                          galleries=galleries)

@member_bp.route('/notificacoes', methods=['GET'])
@login_required
def notifications():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return redirect(url_for('auth.login'))
    
    # Buscar notificações
    from src.models.notification import Notification
    
    notifications = Notification.query.filter_by(user_id=user_id).order_by(Notification.created_at.desc()).all()
    
    return render_template('member_notifications.html', 
                          user=user, 
                          notifications=notifications)

@member_bp.route('/configuracoes', methods=['GET'])
@login_required
def settings():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return redirect(url_for('auth.login'))
    
    return render_template('member_settings.html', user=user)
