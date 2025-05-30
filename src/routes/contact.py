from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from src.models.contact import db, ContactMessage, ContentSuggestion
from src.utils.auth import login_required, admin_required
import logging

contact_bp = Blueprint('contact', __name__)
logger = logging.getLogger(__name__)

@contact_bp.route('/message', methods=['POST'])
def send_message():
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email') or not data.get('message'):
        return jsonify({'message': 'Dados incompletos. Por favor, forneça nome, email e mensagem.'}), 400
    
    new_message = ContactMessage(
        name=data['name'],
        email=data['email'],
        subject=data.get('subject', ''),
        message=data['message'],
        phone=data.get('phone', '')
    )
    
    db.session.add(new_message)
    db.session.commit()
    logger.info(f"Nova mensagem de contato recebida de: {data['name']} ({data['email']})")
    
    return jsonify({'message': 'Mensagem enviada com sucesso! Entraremos em contato em breve.'}), 201

@contact_bp.route('/suggestion', methods=['POST'])
def send_suggestion():
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('email') or not data.get('content'):
        return jsonify({'message': 'Dados incompletos. Por favor, forneça nome, email e conteúdo sugerido.'}), 400
    
    new_suggestion = ContentSuggestion(
        name=data['name'],
        email=data['email'],
        title=data.get('title', ''),
        content=data['content'],
        content_type=data.get('content_type', 'article')
    )
    
    db.session.add(new_suggestion)
    db.session.commit()
    logger.info(f"Nova sugestão de conteúdo recebida de: {data['name']} ({data['email']})")
    
    return jsonify({'message': 'Sugestão enviada com sucesso! Agradecemos sua contribuição.'}), 201

@contact_bp.route('/messages', methods=['GET'])
@admin_required
def get_messages():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).paginate(page=page, per_page=per_page)
    
    result = []
    for message in messages.items:
        result.append({
            'id': message.id,
            'name': message.name,
            'email': message.email,
            'subject': message.subject,
            'message': message.message,
            'phone': message.phone,
            'is_read': message.is_read,
            'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({
        'messages': result,
        'total': messages.total,
        'pages': messages.pages,
        'current_page': messages.page
    }), 200

@contact_bp.route('/messages/<int:message_id>', methods=['GET'])
@admin_required
def get_message(message_id):
    message = ContactMessage.query.get(message_id)
    
    if not message:
        return jsonify({'message': 'Mensagem não encontrada.'}), 404
    
    # Marcar como lida
    if not message.is_read:
        message.is_read = True
        db.session.commit()
    
    result = {
        'id': message.id,
        'name': message.name,
        'email': message.email,
        'subject': message.subject,
        'message': message.message,
        'phone': message.phone,
        'is_read': message.is_read,
        'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return jsonify(result), 200

@contact_bp.route('/messages/<int:message_id>/mark-read', methods=['POST'])
@admin_required
def mark_message_read(message_id):
    message = ContactMessage.query.get(message_id)
    
    if not message:
        return jsonify({'message': 'Mensagem não encontrada.'}), 404
    
    message.is_read = True
    db.session.commit()
    logger.info(f"Mensagem {message_id} marcada como lida por {session['username']}")
    
    return jsonify({'message': 'Mensagem marcada como lida.'}), 200

@contact_bp.route('/messages/<int:message_id>', methods=['DELETE'])
@admin_required
def delete_message(message_id):
    message = ContactMessage.query.get(message_id)
    
    if not message:
        return jsonify({'message': 'Mensagem não encontrada.'}), 404
    
    db.session.delete(message)
    db.session.commit()
    logger.info(f"Mensagem {message_id} excluída por {session['username']}")
    
    return jsonify({'message': 'Mensagem excluída com sucesso!'}), 200

@contact_bp.route('/suggestions', methods=['GET'])
@admin_required
def get_suggestions():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    suggestions = ContentSuggestion.query.order_by(ContentSuggestion.created_at.desc()).paginate(page=page, per_page=per_page)
    
    result = []
    for suggestion in suggestions.items:
        result.append({
            'id': suggestion.id,
            'name': suggestion.name,
            'email': suggestion.email,
            'title': suggestion.title,
            'content': suggestion.content[:200] + '...' if len(suggestion.content) > 200 else suggestion.content,
            'content_type': suggestion.content_type,
            'is_reviewed': suggestion.is_reviewed,
            'is_approved': suggestion.is_approved,
            'created_at': suggestion.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({
        'suggestions': result,
        'total': suggestions.total,
        'pages': suggestions.pages,
        'current_page': suggestions.page
    }), 200

@contact_bp.route('/suggestions/<int:suggestion_id>', methods=['GET'])
@admin_required
def get_suggestion(suggestion_id):
    suggestion = ContentSuggestion.query.get(suggestion_id)
    
    if not suggestion:
        return jsonify({'message': 'Sugestão não encontrada.'}), 404
    
    # Marcar como revisada
    if not suggestion.is_reviewed:
        suggestion.is_reviewed = True
        db.session.commit()
    
    result = {
        'id': suggestion.id,
        'name': suggestion.name,
        'email': suggestion.email,
        'title': suggestion.title,
        'content': suggestion.content,
        'content_type': suggestion.content_type,
        'is_reviewed': suggestion.is_reviewed,
        'is_approved': suggestion.is_approved,
        'created_at': suggestion.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return jsonify(result), 200

@contact_bp.route('/suggestions/<int:suggestion_id>/approve', methods=['POST'])
@admin_required
def approve_suggestion(suggestion_id):
    suggestion = ContentSuggestion.query.get(suggestion_id)
    
    if not suggestion:
        return jsonify({'message': 'Sugestão não encontrada.'}), 404
    
    suggestion.is_reviewed = True
    suggestion.is_approved = True
    db.session.commit()
    logger.info(f"Sugestão {suggestion_id} aprovada por {session['username']}")
    
    return jsonify({'message': 'Sugestão aprovada com sucesso!'}), 200

@contact_bp.route('/suggestions/<int:suggestion_id>/reject', methods=['POST'])
@admin_required
def reject_suggestion(suggestion_id):
    suggestion = ContentSuggestion.query.get(suggestion_id)
    
    if not suggestion:
        return jsonify({'message': 'Sugestão não encontrada.'}), 404
    
    suggestion.is_reviewed = True
    suggestion.is_approved = False
    db.session.commit()
    logger.info(f"Sugestão {suggestion_id} rejeitada por {session['username']}")
    
    return jsonify({'message': 'Sugestão rejeitada.'}), 200

@contact_bp.route('/suggestions/<int:suggestion_id>', methods=['DELETE'])
@admin_required
def delete_suggestion(suggestion_id):
    suggestion = ContentSuggestion.query.get(suggestion_id)
    
    if not suggestion:
        return jsonify({'message': 'Sugestão não encontrada.'}), 404
    
    db.session.delete(suggestion)
    db.session.commit()
    logger.info(f"Sugestão {suggestion_id} excluída por {session['username']}")
    
    return jsonify({'message': 'Sugestão excluída com sucesso!'}), 200
