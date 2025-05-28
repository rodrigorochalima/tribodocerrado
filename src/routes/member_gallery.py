from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from src.models.db import db
from src.models.user import User
from src.models.gallery import Gallery, GalleryImage
from src.utils.auth import login_required
import logging
import os
from werkzeug.utils import secure_filename
from datetime import datetime

# Configurações para upload de imagens
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'static', 'uploads', 'gallery')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

member_gallery_bp = Blueprint('member_gallery', __name__, url_prefix='/membro/galeria')
logger = logging.getLogger(__name__)

@member_gallery_bp.route('/upload', methods=['POST'])
@login_required
def upload_photo():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        flash('Usuário não encontrado.', 'error')
        return redirect(url_for('member.gallery'))
    
    # Verificar se há arquivo na requisição
    if 'photo' not in request.files:
        flash('Nenhum arquivo enviado.', 'error')
        return redirect(url_for('member.gallery'))
    
    photo = request.files['photo']
    
    # Verificar se o arquivo tem nome
    if photo.filename == '':
        flash('Nenhum arquivo selecionado.', 'error')
        return redirect(url_for('member.gallery'))
    
    # Verificar se o arquivo é permitido
    if not allowed_file(photo.filename):
        flash('Tipo de arquivo não permitido. Use PNG, JPG, JPEG, GIF ou WEBP.', 'error')
        return redirect(url_for('member.gallery'))
    
    # Criar diretório de uploads se não existir
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    # Gerar nome de arquivo seguro
    filename = secure_filename(f"{user_id}_{int(datetime.now().timestamp())}_{photo.filename}")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    # Salvar arquivo
    photo.save(filepath)
    
    # Obter dados do formulário (opcionais - não são mais obrigatórios)
    caption = request.form.get('caption', '')
    location = request.form.get('location', '')
    category = request.form.get('category', 'other')
    
    # Criar ou obter galeria padrão do usuário
    gallery = Gallery.query.filter_by(created_by_id=user_id, is_default=True).first()
    
    if not gallery:
        # Criar galeria padrão se não existir
        gallery = Gallery(
            title="Minha Galeria",
            description="Galeria pessoal",
            created_by_id=user_id,
            is_default=True
        )
        db.session.add(gallery)
        db.session.commit()
    
    # Obter a próxima ordem
    max_order = db.session.query(db.func.max(GalleryImage.order)).filter_by(gallery_id=gallery.id).scalar()
    next_order = 1 if max_order is None else max_order + 1
    
    # Criar nova imagem
    image_url = f"/static/uploads/gallery/{filename}"
    new_image = GalleryImage(
        gallery_id=gallery.id,
        image_url=image_url,
        caption=caption,
        location=location,
        category=category,
        order=next_order,
        created_at=datetime.now()  # Garantir que a data de criação seja definida
    )
    
    db.session.add(new_image)
    db.session.commit()
    
    logger.info(f"Foto enviada com sucesso pelo usuário {user.username}: {image_url}")
    flash('Foto enviada com sucesso!', 'success')
    return redirect(url_for('member.gallery'))
