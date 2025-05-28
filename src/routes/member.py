from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from src.models.db import db
from src.models.user import User
from src.utils.auth import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
import logging

member_bp = Blueprint('member', __name__)
logger = logging.getLogger(__name__)

# Configuração para upload de arquivos
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Garantir que os diretórios de upload existam
def ensure_upload_dirs():
    dirs = [
        os.path.join(UPLOAD_FOLDER, 'profile'),
        os.path.join(UPLOAD_FOLDER, 'gallery'),
        os.path.join(UPLOAD_FOLDER, 'motorcycles'),
        os.path.join(UPLOAD_FOLDER, 'family')
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    # Criar diretório para imagens padrão
    img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'static', 'img')
    os.makedirs(img_dir, exist_ok=True)
    
    # Criar imagem de perfil padrão se não existir
    default_profile = os.path.join(img_dir, 'default-profile.png')
    if not os.path.exists(default_profile):
        # Criar uma imagem de perfil padrão simples
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (200, 200), color=(73, 109, 137))
            d = ImageDraw.Draw(img)
            d.ellipse((10, 10, 190, 190), fill=(255, 255, 255))
            d.ellipse((50, 50, 150, 150), fill=(73, 109, 137))
            img.save(default_profile)
            logger.info(f"Imagem de perfil padrão criada em {default_profile}")
        except Exception as e:
            logger.error(f"Erro ao criar imagem de perfil padrão: {e}")

# Chamar a função para garantir que os diretórios existam
ensure_upload_dirs()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@member_bp.route('/membro/perfil')
@login_required
def profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('auth.logout'))
    
    return render_template('member_profile.html', user=user)

@member_bp.route('/membro/editar-perfil', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('auth.logout'))
    
    if request.method == 'POST':
        try:
            # Atualizar informações básicas
            user.full_name = request.form.get('full_name', user.full_name)
            user.nickname = request.form.get('nickname', user.nickname)
            user.email = request.form.get('email', user.email)
            
            # Tratar campos que podem não existir no modelo User
            try:
                # Verificar se o atributo existe antes de tentar acessá-lo
                if hasattr(user, 'join_date'):
                    user.join_date = request.form.get('join_date', user.join_date)
                else:
                    # Ignorar este campo se não existir no modelo
                    logger.warning("Campo 'join_date' não existe no modelo User")
                
                # Tratar outros campos que podem não existir
                for field in ['birth_date', 'blood_type', 'address_street', 'address_number', 
                             'address_complement', 'address_district', 'address_city', 
                             'address_state', 'address_zipcode', 'health_notes', 
                             'health_insurance', 'health_insurance_number']:
                    if field in request.form and hasattr(user, field):
                        setattr(user, field, request.form.get(field))
            except Exception as e:
                logger.error(f"Erro ao processar campos do formulário: {e}")
            
            # Processar upload de foto de perfil
            if 'profile_photo' in request.files:
                file = request.files['profile_photo']
                if file and file.filename and allowed_file(file.filename):
                    try:
                        # Garantir que o diretório existe
                        ensure_upload_dirs()
                        
                        # Criar nome de arquivo seguro
                        filename = secure_filename(file.filename)
                        timestamp = int(datetime.now().timestamp())
                        safe_filename = f"{user_id}_{timestamp}_{filename}"
                        
                        # Salvar o arquivo
                        file_path = os.path.join(UPLOAD_FOLDER, 'profile', safe_filename)
                        file.save(file_path)
                        
                        # Atualizar o caminho da foto no banco de dados
                        if hasattr(user, 'profile_photo'):
                            user.profile_photo = f"/static/uploads/profile/{safe_filename}"
                        else:
                            logger.warning("Campo 'profile_photo' não existe no modelo User")
                        
                        logger.info(f"Foto de perfil salva: {file_path}")
                    except Exception as e:
                        logger.error(f"Erro ao salvar foto de perfil: {e}")
                        flash('Erro ao salvar foto de perfil', 'error')
            
            # Salvar alterações
            db.session.commit()
            flash('Perfil atualizado com sucesso!', 'success')
            return redirect(url_for('member.profile'))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Erro ao atualizar perfil: {e}")
            flash('Erro ao atualizar perfil', 'error')
    
    return render_template('member_edit_profile.html', user=user)

@member_bp.route('/membro/alterar-senha', methods=['GET', 'POST'])
@login_required
def change_password():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('auth.logout'))
    
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not current_password or not new_password or not confirm_password:
            flash('Por favor, preencha todos os campos', 'error')
            return redirect(url_for('member.change_password'))
        
        if new_password != confirm_password:
            flash('As senhas não coincidem', 'error')
            return redirect(url_for('member.change_password'))
        
        if not check_password_hash(user.password, current_password):
            flash('Senha atual incorreta', 'error')
            return redirect(url_for('member.change_password'))
        
        user.password = generate_password_hash(new_password)
        db.session.commit()
        
        flash('Senha alterada com sucesso!', 'success')
        return redirect(url_for('member.profile'))
    
    return render_template('member_change_password.html')

@member_bp.route('/membro/minhas-motos')
@login_required
def my_motorcycles():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('auth.logout'))
    
    # Aqui você buscaria as motos do usuário no banco de dados
    # Por enquanto, vamos retornar uma lista vazia
    motorcycles = []
    
    return render_template('member_motorcycles.html', motorcycles=motorcycles)

@member_bp.route('/membro/adicionar-moto', methods=['GET', 'POST'])
@login_required
def add_motorcycle():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('auth.logout'))
    
    if request.method == 'POST':
        # Aqui você processaria o formulário para adicionar uma nova moto
        flash('Moto adicionada com sucesso!', 'success')
        return redirect(url_for('member.my_motorcycles'))
    
    return render_template('member_add_motorcycle.html')

@member_bp.route('/membro/minha-familia')
@login_required
def my_family():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('auth.logout'))
    
    # Aqui você buscaria os familiares do usuário no banco de dados
    # Por enquanto, vamos retornar uma lista vazia
    family_members = []
    
    return render_template('member_family.html', family_members=family_members)

@member_bp.route('/membro/adicionar-familiar', methods=['GET', 'POST'])
@login_required
def add_family_member():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('auth.logout'))
    
    if request.method == 'POST':
        # Aqui você processaria o formulário para adicionar um novo familiar
        flash('Familiar adicionado com sucesso!', 'success')
        return redirect(url_for('member.my_family'))
    
    return render_template('member_add_family.html')

@member_bp.route('/membro/minha-galeria')
@login_required
def my_gallery():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('auth.logout'))
    
    # Aqui você buscaria as fotos do usuário no banco de dados
    # Por enquanto, vamos retornar uma lista vazia
    photos = []
    
    return render_template('member_gallery.html', photos=photos)

@member_bp.route('/membro/adicionar-foto', methods=['GET', 'POST'])
@login_required
def add_photo():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        flash('Usuário não encontrado', 'error')
        return redirect(url_for('auth.logout'))
    
    if request.method == 'POST':
        # Aqui você processaria o formulário para adicionar uma nova foto
        flash('Foto adicionada com sucesso!', 'success')
        return redirect(url_for('member.my_gallery'))
    
    return render_template('member_add_photo.html')

