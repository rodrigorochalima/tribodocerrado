from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from ..models.db import db

member_gallery_bp = Blueprint('member_gallery', __name__)

@member_gallery_bp.route('/', methods=['GET'])
@login_required
def gallery():
    # Aqui você buscaria as imagens da galeria do usuário no banco de dados
    gallery_images = []  # Substitua por uma consulta real
    return render_template('member_gallery.html', gallery_images=gallery_images)

@member_gallery_bp.route('/upload', methods=['POST'])
@login_required
def upload_image():
    if 'gallery_image' not in request.files:
        flash('Nenhum arquivo selecionado', 'danger')
        return redirect(url_for('member_gallery.gallery'))
    
    file = request.files['gallery_image']
    caption = request.form.get('caption', '')
    
    if file.filename == '':
        flash('Nenhum arquivo selecionado', 'danger')
        return redirect(url_for('member_gallery.gallery'))
    
    if file:
        filename = secure_filename(file.filename)
        # Criar nome único para o arquivo
        unique_filename = f"{current_user.id}_{int(datetime.now().timestamp())}_{filename}"
        # Garantir que o diretório existe
        gallery_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'gallery')
        os.makedirs(gallery_dir, exist_ok=True)
        # Salvar o arquivo
        file_path = os.path.join(gallery_dir, unique_filename)
        file.save(file_path)
        
        # Aqui você salvaria a informação no banco de dados
        # gallery_image = GalleryImage(user_id=current_user.id, image_url=f"uploads/gallery/{unique_filename}", caption=caption)
        # db.session.add(gallery_image)
        # db.session.commit()
        
        flash('Imagem enviada com sucesso!', 'success')
    
    return redirect(url_for('member_gallery.gallery'))

@member_gallery_bp.route('/delete/<int:image_id>', methods=['POST'])
@login_required
def delete_image(image_id):
    # Aqui você buscaria a imagem no banco de dados e verificaria se pertence ao usuário atual
    # Se sim, excluiria a imagem do sistema de arquivos e do banco de dados
    
    flash('Imagem excluída com sucesso!', 'success')
    return redirect(url_for('member_gallery.gallery'))
