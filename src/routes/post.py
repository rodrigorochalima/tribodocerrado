from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from src.models.post import db, Post, Comment, Category, Tag, post_tags
from src.utils.auth import login_required, admin_required
import logging
from datetime import datetime

post_bp = Blueprint('post', __name__, url_prefix='/posts')
logger = logging.getLogger(__name__)

@post_bp.route('/', methods=['GET'])
def get_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category_id = request.args.get('category_id', type=int)
    tag_name = request.args.get('tag', type=str)
    
    # Construir query base
    query = Post.query.filter_by(is_published=True)
    
    # Filtrar por categoria, se especificado
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Filtrar por tag, se especificado
    if tag_name:
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag:
            query = query.filter(Post.id.in_(
                db.session.query(post_tags.c.post_id).filter(post_tags.c.tag_id == tag.id)
            ))
    
    # Paginar resultados
    posts = query.order_by(Post.created_at.desc()).paginate(page=page, per_page=per_page)
    
    # Formatar para resposta JSON
    result = []
    for post in posts.items:
        result.append({
            'id': post.id,
            'title': post.title,
            'summary': post.summary,
            'content': post.content[:200] + '...' if len(post.content) > 200 else post.content,
            'image_url': post.image_url,
            'author': post.author.username,
            'category': post.category.name if post.category else None,
            'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'comment_count': Comment.query.filter_by(post_id=post.id, is_approved=True).count()
        })
    
    return jsonify({
        'posts': result,
        'total': posts.total,
        'pages': posts.pages,
        'current_page': posts.page
    }), 200

@post_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)
    
    if not post or not post.is_published:
        return jsonify({'message': 'Post não encontrado.'}), 404
    
    # Buscar comentários aprovados
    comments = Comment.query.filter_by(post_id=post_id, is_approved=True).order_by(Comment.created_at).all()
    
    # Buscar tags
    tags = []
    for tag in post.tags:
        tags.append(tag.name)
    
    # Formatar para resposta JSON
    result = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'summary': post.summary,
        'image_url': post.image_url,
        'author': {
            'id': post.author.id,
            'username': post.author.username,
            'profile_image': post.author.profile_image
        },
        'category': {
            'id': post.category.id,
            'name': post.category.name
        } if post.category else None,
        'created_at': post.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': post.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        'tags': tags,
        'comments': [{
            'id': comment.id,
            'content': comment.content,
            'author': {
                'id': comment.author.id,
                'username': comment.author.username,
                'profile_image': comment.author.profile_image
            },
            'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for comment in comments]
    }
    
    return jsonify(result), 200

@post_bp.route('/', methods=['POST'])
@login_required
def create_post():
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('content'):
        return jsonify({'message': 'Dados incompletos. Por favor, forneça título e conteúdo.'}), 400
    
    # Verificar categoria
    category_id = data.get('category_id')
    category = None
    if category_id:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'message': 'Categoria não encontrada.'}), 404
    
    # Criar novo post
    new_post = Post(
        title=data['title'],
        content=data['content'],
        summary=data.get('summary', ''),
        image_url=data.get('image_url', ''),
        author_id=session['user_id'],
        category_id=category_id,
        is_published=data.get('is_published', True)
    )
    
    db.session.add(new_post)
    db.session.commit()
    
    # Adicionar tags, se fornecidas
    if 'tags' in data and isinstance(data['tags'], list):
        for tag_name in data['tags']:
            # Buscar tag existente ou criar nova
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.commit()
            
            # Adicionar relação entre post e tag
            stmt = post_tags.insert().values(post_id=new_post.id, tag_id=tag.id)
            db.session.execute(stmt)
        
        db.session.commit()
    
    logger.info(f"Novo post criado: {data['title']} por {session['username']}")
    
    return jsonify({
        'message': 'Post criado com sucesso!',
        'post_id': new_post.id
    }), 201

@post_bp.route('/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    post = Post.query.get(post_id)
    
    if not post:
        return jsonify({'message': 'Post não encontrado.'}), 404
    
    # Verificar permissão
    if post.author_id != session['user_id'] and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para editar este post.'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Nenhum dado fornecido para atualização.'}), 400
    
    # Atualizar campos
    if 'title' in data:
        post.title = data['title']
    
    if 'content' in data:
        post.content = data['content']
    
    if 'summary' in data:
        post.summary = data['summary']
    
    if 'image_url' in data:
        post.image_url = data['image_url']
    
    if 'category_id' in data:
        if data['category_id']:
            category = Category.query.get(data['category_id'])
            if not category:
                return jsonify({'message': 'Categoria não encontrada.'}), 404
            post.category_id = data['category_id']
        else:
            post.category_id = None
    
    if 'is_published' in data:
        post.is_published = data['is_published']
    
    post.updated_at = datetime.utcnow()
    
    # Atualizar tags, se fornecidas
    if 'tags' in data and isinstance(data['tags'], list):
        # Remover todas as tags existentes
        stmt = post_tags.delete().where(post_tags.c.post_id == post_id)
        db.session.execute(stmt)
        
        # Adicionar novas tags
        for tag_name in data['tags']:
            # Buscar tag existente ou criar nova
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.session.add(tag)
                db.session.commit()
            
            # Adicionar relação entre post e tag
            stmt = post_tags.insert().values(post_id=post.id, tag_id=tag.id)
            db.session.execute(stmt)
    
    db.session.commit()
    logger.info(f"Post {post_id} atualizado por {session['username']}")
    
    return jsonify({'message': 'Post atualizado com sucesso!'}), 200

@post_bp.route('/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)
    
    if not post:
        return jsonify({'message': 'Post não encontrado.'}), 404
    
    # Verificar permissão
    if post.author_id != session['user_id'] and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para excluir este post.'}), 403
    
    # Excluir todos os comentários do post
    Comment.query.filter_by(post_id=post_id).delete()
    
    # Remover todas as relações com tags
    stmt = post_tags.delete().where(post_tags.c.post_id == post_id)
    db.session.execute(stmt)
    
    db.session.delete(post)
    db.session.commit()
    logger.info(f"Post {post_id} excluído por {session['username']}")
    
    return jsonify({'message': 'Post excluído com sucesso!'}), 200

@post_bp.route('/<int:post_id>/comment', methods=['POST'])
@login_required
def add_comment(post_id):
    post = Post.query.get(post_id)
    
    if not post:
        return jsonify({'message': 'Post não encontrado.'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('content'):
        return jsonify({'message': 'Conteúdo do comentário não fornecido.'}), 400
    
    # Criar novo comentário
    new_comment = Comment(
        content=data['content'],
        post_id=post_id,
        author_id=session['user_id'],
        is_approved=True  # Por padrão, comentários são aprovados automaticamente
    )
    
    db.session.add(new_comment)
    db.session.commit()
    logger.info(f"Novo comentário adicionado ao post {post_id} por {session['username']}")
    
    return jsonify({
        'message': 'Comentário adicionado com sucesso!',
        'comment_id': new_comment.id
    }), 201

@post_bp.route('/comment/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    
    if not comment:
        return jsonify({'message': 'Comentário não encontrado.'}), 404
    
    # Verificar permissão
    if comment.author_id != session['user_id'] and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para excluir este comentário.'}), 403
    
    db.session.delete(comment)
    db.session.commit()
    logger.info(f"Comentário {comment_id} excluído por {session['username']}")
    
    return jsonify({'message': 'Comentário excluído com sucesso!'}), 200

@post_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    
    result = []
    for category in categories:
        result.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'post_count': Post.query.filter_by(category_id=category.id, is_published=True).count()
        })
    
    return jsonify({'categories': result}), 200

@post_bp.route('/categories', methods=['POST'])
@admin_required
def create_category():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'message': 'Nome da categoria não fornecido.'}), 400
    
    # Verificar se a categoria já existe
    existing_category = Category.query.filter_by(name=data['name']).first()
    if existing_category:
        return jsonify({'message': 'Categoria com este nome já existe.'}), 409
    
    # Criar nova categoria
    new_category = Category(
        name=data['name'],
        description=data.get('description', '')
    )
    
    db.session.add(new_category)
    db.session.commit()
    logger.info(f"Nova categoria criada: {data['name']} por {session['username']}")
    
    return jsonify({
        'message': 'Categoria criada com sucesso!',
        'category_id': new_category.id
    }), 201

@post_bp.route('/categories/<int:category_id>', methods=['PUT'])
@admin_required
def update_category(category_id):
    category = Category.query.get(category_id)
    
    if not category:
        return jsonify({'message': 'Categoria não encontrada.'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Nenhum dado fornecido para atualização.'}), 400
    
    # Verificar se o novo nome já existe em outra categoria
    if 'name' in data and data['name'] != category.name:
        existing_category = Category.query.filter_by(name=data['name']).first()
        if existing_category:
            return jsonify({'message': 'Categoria com este nome já existe.'}), 409
        
        category.name = data['name']
    
    if 'description' in data:
        category.description = data['description']
    
    db.session.commit()
    logger.info(f"Categoria {category_id} atualizada por {session['username']}")
    
    return jsonify({'message': 'Categoria atualizada com sucesso!'}), 200

@post_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(category_id):
    category = Category.query.get(category_id)
    
    if not category:
        return jsonify({'message': 'Categoria não encontrada.'}), 404
    
    # Verificar se existem posts nesta categoria
    posts_count = Post.query.filter_by(category_id=category_id).count()
    if posts_count > 0:
        return jsonify({'message': f'Não é possível excluir esta categoria. Existem {posts_count} posts associados a ela.'}), 400
    
    db.session.delete(category)
    db.session.commit()
    logger.info(f"Categoria {category_id} excluída por {session['username']}")
    
    return jsonify({'message': 'Categoria excluída com sucesso!'}), 200

@post_bp.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    
    result = []
    for tag in tags:
        # Contar posts com esta tag
        post_count = db.session.query(post_tags).filter_by(tag_id=tag.id).count()
        
        result.append({
            'id': tag.id,
            'name': tag.name,
            'post_count': post_count
        })
    
    return jsonify({'tags': result}), 200
