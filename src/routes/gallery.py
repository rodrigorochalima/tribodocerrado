from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from src.models.gallery import db, Gallery, GalleryImage, GalleryAlbum, album_images
from src.utils.auth import login_required, admin_required
import logging
import os
from werkzeug.utils import secure_filename

gallery_bp = Blueprint('gallery', __name__, url_prefix='/gallery')
logger = logging.getLogger(__name__)

# Configurações para upload de imagens
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/images/gallery')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@gallery_bp.route('/', methods=['GET'])
def get_galleries():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    galleries = Gallery.query.order_by(Gallery.created_at.desc()).paginate(page=page, per_page=per_page)
    
    result = []
    for gallery in galleries.items:
        # Obter a imagem de capa (primeira imagem da galeria)
        cover_image = GalleryImage.query.filter_by(gallery_id=gallery.id).order_by(GalleryImage.order).first()
        
        result.append({
            'id': gallery.id,
            'title': gallery.title,
            'description': gallery.description,
            'event_date': gallery.event_date.strftime('%Y-%m-%d') if gallery.event_date else None,
            'created_at': gallery.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'image_count': GalleryImage.query.filter_by(gallery_id=gallery.id).count(),
            'cover_image': cover_image.image_url if cover_image else None
        })
    
    return jsonify({
        'galleries': result,
        'total': galleries.total,
        'pages': galleries.pages,
        'current_page': galleries.page
    }), 200

@gallery_bp.route('/<int:gallery_id>', methods=['GET'])
def get_gallery(gallery_id):
    gallery = Gallery.query.get(gallery_id)
    
    if not gallery:
        return jsonify({'message': 'Galeria não encontrada.'}), 404
    
    images = GalleryImage.query.filter_by(gallery_id=gallery_id).order_by(GalleryImage.order).all()
    
    images_list = []
    for image in images:
        images_list.append({
            'id': image.id,
            'image_url': image.image_url,
            'caption': image.caption,
            'order': image.order
        })
    
    result = {
        'id': gallery.id,
        'title': gallery.title,
        'description': gallery.description,
        'event_date': gallery.event_date.strftime('%Y-%m-%d') if gallery.event_date else None,
        'created_at': gallery.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'created_by': gallery.created_by.username,
        'images': images_list
    }
    
    return jsonify(result), 200

@gallery_bp.route('/', methods=['POST'])
@login_required
def create_gallery():
    data = request.get_json()
    
    if not data or not data.get('title'):
        return jsonify({'message': 'Título da galeria não fornecido.'}), 400
    
    new_gallery = Gallery(
        title=data['title'],
        description=data.get('description', ''),
        event_date=data.get('event_date'),
        created_by_id=session['user_id']
    )
    
    db.session.add(new_gallery)
    db.session.commit()
    logger.info(f"Nova galeria criada: {data['title']} por {session['username']}")
    
    return jsonify({
        'message': 'Galeria criada com sucesso!',
        'gallery_id': new_gallery.id
    }), 201

@gallery_bp.route('/<int:gallery_id>', methods=['PUT'])
@login_required
def update_gallery(gallery_id):
    gallery = Gallery.query.get(gallery_id)
    
    if not gallery:
        return jsonify({'message': 'Galeria não encontrada.'}), 404
    
    # Verificar permissão
    if gallery.created_by_id != session['user_id'] and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para editar esta galeria.'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Nenhum dado fornecido para atualização.'}), 400
    
    if 'title' in data:
        gallery.title = data['title']
    
    if 'description' in data:
        gallery.description = data['description']
    
    if 'event_date' in data:
        gallery.event_date = data['event_date']
    
    db.session.commit()
    logger.info(f"Galeria atualizada: {gallery.title} por {session['username']}")
    
    return jsonify({'message': 'Galeria atualizada com sucesso!'}), 200

@gallery_bp.route('/<int:gallery_id>', methods=['DELETE'])
@login_required
def delete_gallery(gallery_id):
    gallery = Gallery.query.get(gallery_id)
    
    if not gallery:
        return jsonify({'message': 'Galeria não encontrada.'}), 404
    
    # Verificar permissão
    if gallery.created_by_id != session['user_id'] and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para excluir esta galeria.'}), 403
    
    # Excluir todas as imagens da galeria
    images = GalleryImage.query.filter_by(gallery_id=gallery_id).all()
    for image in images:
        db.session.delete(image)
    
    db.session.delete(gallery)
    db.session.commit()
    logger.info(f"Galeria excluída: {gallery.title} por {session['username']}")
    
    return jsonify({'message': 'Galeria excluída com sucesso!'}), 200

@gallery_bp.route('/<int:gallery_id>/images', methods=['POST'])
@login_required
def add_image(gallery_id):
    gallery = Gallery.query.get(gallery_id)
    
    if not gallery:
        return jsonify({'message': 'Galeria não encontrada.'}), 404
    
    # Verificar permissão
    if gallery.created_by_id != session['user_id'] and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para adicionar imagens a esta galeria.'}), 403
    
    # Verificar se é um upload de arquivo ou uma URL
    if 'file' in request.files:
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'message': 'Nenhum arquivo selecionado.'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Garantir que o diretório de upload exista
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            # Salvar o arquivo
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            # URL relativa para o arquivo
            image_url = f'/static/images/gallery/{filename}'
        else:
            return jsonify({'message': 'Tipo de arquivo não permitido.'}), 400
    else:
        data = request.get_json()
        
        if not data or not data.get('image_url'):
            return jsonify({'message': 'URL da imagem não fornecida.'}), 400
        
        image_url = data['image_url']
    
    # Obter a próxima ordem
    max_order = db.session.query(db.func.max(GalleryImage.order)).filter_by(gallery_id=gallery_id).scalar()
    next_order = 1 if max_order is None else max_order + 1
    
    # Criar nova imagem
    new_image = GalleryImage(
        gallery_id=gallery_id,
        image_url=image_url,
        caption=request.form.get('caption', '') if 'file' in request.files else data.get('caption', ''),
        order=next_order
    )
    
    db.session.add(new_image)
    db.session.commit()
    logger.info(f"Nova imagem adicionada à galeria {gallery_id} por {session['username']}")
    
    return jsonify({
        'message': 'Imagem adicionada com sucesso!',
        'image_id': new_image.id,
        'image_url': new_image.image_url
    }), 201

@gallery_bp.route('/images/<int:image_id>', methods=['PUT'])
@login_required
def update_image(image_id):
    image = GalleryImage.query.get(image_id)
    
    if not image:
        return jsonify({'message': 'Imagem não encontrada.'}), 404
    
    gallery = Gallery.query.get(image.gallery_id)
    
    # Verificar permissão
    if gallery.created_by_id != session['user_id'] and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para editar esta imagem.'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Nenhum dado fornecido para atualização.'}), 400
    
    if 'caption' in data:
        image.caption = data['caption']
    
    if 'order' in data:
        image.order = data['order']
    
    db.session.commit()
    logger.info(f"Imagem {image_id} atualizada por {session['username']}")
    
    return jsonify({'message': 'Imagem atualizada com sucesso!'}), 200

@gallery_bp.route('/images/<int:image_id>', methods=['DELETE'])
@login_required
def delete_image(image_id):
    image = GalleryImage.query.get(image_id)
    
    if not image:
        return jsonify({'message': 'Imagem não encontrada.'}), 404
    
    gallery = Gallery.query.get(image.gallery_id)
    
    # Verificar permissão
    if gallery.created_by_id != session['user_id'] and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para excluir esta imagem.'}), 403
    
    db.session.delete(image)
    db.session.commit()
    logger.info(f"Imagem {image_id} excluída por {session['username']}")
    
    return jsonify({'message': 'Imagem excluída com sucesso!'}), 200

@gallery_bp.route('/images/reorder', methods=['POST'])
@login_required
def reorder_images():
    data = request.get_json()
    
    if not data or not data.get('images'):
        return jsonify({'message': 'Dados de reordenação não fornecidos.'}), 400
    
    # Verificar se todas as imagens pertencem à mesma galeria
    image_ids = [item['id'] for item in data['images']]
    images = GalleryImage.query.filter(GalleryImage.id.in_(image_ids)).all()
    
    if not images:
        return jsonify({'message': 'Nenhuma imagem encontrada.'}), 404
    
    gallery_id = images[0].gallery_id
    for image in images:
        if image.gallery_id != gallery_id:
            return jsonify({'message': 'Todas as imagens devem pertencer à mesma galeria.'}), 400
    
    # Verificar permissão
    gallery = Gallery.query.get(gallery_id)
    if gallery.created_by_id != session['user_id'] and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para reordenar estas imagens.'}), 403
    
    # Atualizar a ordem das imagens
    for item in data['images']:
        image = next((img for img in images if img.id == item['id']), None)
        if image:
            image.order = item['order']
    
    db.session.commit()
    logger.info(f"Imagens da galeria {gallery_id} reordenadas por {session['username']}")
    
    return jsonify({'message': 'Imagens reordenadas com sucesso!'}), 200
