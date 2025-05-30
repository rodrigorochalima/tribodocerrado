from flask import Blueprint, request, jsonify, current_app, session, render_template
from src.models.user import User, EmergencyContact, MotorcycleImage
from src.models.motorcycle import Motorcycle
from src.models.family import FamilyMember
from src.models.notification import Notification
from src.models.db import db
from src.utils.auth import login_required, admin_required
import os
from datetime import datetime, date
from werkzeug.utils import secure_filename
import logging

user_bp = Blueprint('user', __name__)
logger = logging.getLogger(__name__)

# Configurações para upload de imagens
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/images/profiles')
MOTORCYCLE_UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/images/motorcycles')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'API está funcionando corretamente!'
    }), 200

@user_bp.route('/setup-admin', methods=['POST'])
def setup_admin():
    # Verificar se já existe algum administrador
    admin_exists = User.query.filter_by(is_admin=True).first()
    
    if admin_exists:
        return jsonify({'message': 'Um administrador já existe no sistema.'}), 409
    
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Dados incompletos. Por favor, forneça nome de usuário, email e senha.'}), 400
    
    from werkzeug.security import generate_password_hash
    
    # Criar o primeiro administrador
    admin_user = User(
        username=data['username'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        full_name=data.get('full_name', 'Administrador'),
        nickname=data.get('nickname', data['username']),
        is_admin=True,
        is_approved=True
    )
    
    db.session.add(admin_user)
    db.session.commit()
    
    return jsonify({
        'message': 'Administrador inicial criado com sucesso!',
        'user_id': admin_user.id
    }), 201

@user_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado.'}), 404
    
    # Buscar informações relacionadas
    family_members = FamilyMember.query.filter_by(user_id=user_id).all()
    emergency_contacts = EmergencyContact.query.filter_by(user_id=user_id).all()
    motorcycles = Motorcycle.query.filter_by(user_id=user_id).all()
    
    # Formatar dados do padrinho, se existir
    godfather = None
    if user.godfather_id:
        godfather_user = User.query.get(user.godfather_id)
        if godfather_user:
            godfather = {
                'id': godfather_user.id,
                'username': godfather_user.username,
                'nickname': godfather_user.nickname
            }
    
    # Formatar dados de familiares
    family_data = []
    for member in family_members:
        family_data.append({
            'id': member.id,
            'name': member.name,
            'relationship_type': member.relationship_type,
            'birth_date': member.birth_date.strftime('%Y-%m-%d') if member.birth_date else None
        })
    
    # Formatar contatos de emergência
    emergency_data = []
    for contact in emergency_contacts:
        emergency_data.append({
            'id': contact.id,
            'name': contact.name,
            'phone': contact.phone,
            'relationship': contact.relationship
        })
    
    # Formatar dados das motos
    motorcycle_data = []
    for moto in motorcycles:
        # Buscar imagens da moto
        moto_images = MotorcycleImage.query.filter_by(motorcycle_id=moto.id).all()
        images = []
        for img in moto_images:
            images.append({
                'id': img.id,
                'image_url': img.image_url,
                'caption': img.caption
            })
        
        motorcycle_data.append({
            'id': moto.id,
            'brand': moto.brand,
            'model': moto.model,
            'manufacturing_year': moto.manufacturing_year,
            'model_year': moto.model_year,
            'chassis_number': moto.chassis_number,
            'engine_number': moto.engine_number,
            'license_plate': moto.license_plate,
            'ipva_due_date': moto.ipva_due_date.strftime('%Y-%m-%d') if moto.ipva_due_date else None,
            'images': images
        })
    
    # Montar resposta completa
    profile_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'full_name': user.full_name,
        'nickname': user.nickname,
        'profile_image': user.profile_image,
        'bio': user.bio,
        'birth_date': user.birth_date.strftime('%Y-%m-%d') if user.birth_date else None,
        'collection_date': user.collection_date.strftime('%Y-%m-%d') if user.collection_date else None,
        'blood_type': user.blood_type,
        'address': {
            'street': user.address_street,
            'number': user.address_number,
            'complement': user.address_complement,
            'district': user.address_district,
            'city': user.address_city,
            'state': user.address_state,
            'zipcode': user.address_zipcode
        },
        'health': {
            'notes': user.health_notes,
            'insurance': user.health_insurance,
            'insurance_number': user.health_insurance_number
        },
        'godfather': godfather,
        'family_members': family_data,
        'emergency_contacts': emergency_data,
        'motorcycles': motorcycle_data,
        'is_admin': user.is_admin,
        'is_approved': user.is_approved,
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return jsonify(profile_data), 200

@user_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado.'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Nenhum dado fornecido para atualização.'}), 400
    
    # Atualizar campos básicos
    if 'full_name' in data:
        user.full_name = data['full_name']
    
    if 'nickname' in data:
        user.nickname = data['nickname']
    
    if 'bio' in data:
        user.bio = data['bio']
    
    if 'birth_date' in data and data['birth_date']:
        try:
            user.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Formato de data inválido para data de nascimento.'}), 400
    
    if 'collection_date' in data and data['collection_date']:
        try:
            user.collection_date = datetime.strptime(data['collection_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Formato de data inválido para data de coletamento.'}), 400
    
    if 'blood_type' in data:
        user.blood_type = data['blood_type']
    
    # Atualizar endereço
    if 'address' in data:
        address = data['address']
        if 'street' in address:
            user.address_street = address['street']
        if 'number' in address:
            user.address_number = address['number']
        if 'complement' in address:
            user.address_complement = address['complement']
        if 'district' in address:
            user.address_district = address['district']
        if 'city' in address:
            user.address_city = address['city']
        if 'state' in address:
            user.address_state = address['state']
        if 'zipcode' in address:
            user.address_zipcode = address['zipcode']
    
    # Atualizar informações de saúde
    if 'health' in data:
        health = data['health']
        if 'notes' in health:
            user.health_notes = health['notes']
        if 'insurance' in health:
            user.health_insurance = health['insurance']
        if 'insurance_number' in health:
            user.health_insurance_number = health['insurance_number']
    
    # Atualizar padrinho
    if 'godfather_id' in data:
        # Verificar se o padrinho existe
        if data['godfather_id']:
            godfather = User.query.get(data['godfather_id'])
            if not godfather:
                return jsonify({'message': 'Padrinho não encontrado.'}), 404
            user.godfather_id = data['godfather_id']
        else:
            user.godfather_id = None
    
    db.session.commit()
    logger.info(f"Perfil atualizado para o usuário {user.username}")
    
    return jsonify({'message': 'Perfil atualizado com sucesso!'}), 200

@user_bp.route('/profile/image', methods=['POST'])
@login_required
def update_profile_image():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado.'}), 404
    
    if 'file' not in request.files:
        return jsonify({'message': 'Nenhum arquivo enviado.'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'Nenhum arquivo selecionado.'}), 400
    
    if file and allowed_file(file.filename):
        # Garantir que o diretório de upload exista
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Criar nome de arquivo único
        filename = secure_filename(f"{user.username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file.filename.rsplit('.', 1)[1].lower()}")
        
        # Salvar o arquivo
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Atualizar URL da imagem de perfil
        user.profile_image = f'/static/images/profiles/{filename}'
        db.session.commit()
        
        logger.info(f"Imagem de perfil atualizada para o usuário {user.username}")
        
        return jsonify({
            'message': 'Imagem de perfil atualizada com sucesso!',
            'profile_image': user.profile_image
        }), 200
    
    return jsonify({'message': 'Tipo de arquivo não permitido.'}), 400

@user_bp.route('/family', methods=['POST'])
@login_required
def add_family_member():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado.'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('relationship_type'):
        return jsonify({'message': 'Dados incompletos. Por favor, forneça nome e tipo de relacionamento.'}), 400
    
    # Validar tipo de relacionamento
    if data['relationship_type'] not in ['spouse', 'child']:
        return jsonify({'message': 'Tipo de relacionamento inválido. Use "spouse" ou "child".'}), 400
    
    # Converter data de nascimento, se fornecida
    birth_date = None
    if data.get('birth_date'):
        try:
            birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Formato de data inválido para data de nascimento.'}), 400
    
    # Criar novo membro da família
    new_family_member = FamilyMember(
        name=data['name'],
        relationship_type=data['relationship_type'],
        birth_date=birth_date,
        user_id=user_id
    )
    
    db.session.add(new_family_member)
    db.session.commit()
    
    logger.info(f"Novo membro da família adicionado para o usuário {user.username}")
    
    return jsonify({
        'message': 'Membro da família adicionado com sucesso!',
        'family_member_id': new_family_member.id
    }), 201

@user_bp.route('/family/<int:member_id>', methods=['PUT'])
@login_required
def update_family_member(member_id):
    user_id = session.get('user_id')
    
    # Buscar membro da família
    family_member = FamilyMember.query.get(member_id)
    
    if not family_member:
        return jsonify({'message': 'Membro da família não encontrado.'}), 404
    
    # Verificar permissão
    if family_member.user_id != user_id and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para editar este membro da família.'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Nenhum dado fornecido para atualização.'}), 400
    
    # Atualizar campos
    if 'name' in data:
        family_member.name = data['name']
    
    if 'relationship_type' in data:
        if data['relationship_type'] not in ['spouse', 'child']:
            return jsonify({'message': 'Tipo de relacionamento inválido. Use "spouse" ou "child".'}), 400
        family_member.relationship_type = data['relationship_type']
    
    if 'birth_date' in data:
        if data['birth_date']:
            try:
                family_member.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'message': 'Formato de data inválido para data de nascimento.'}), 400
        else:
            family_member.birth_date = None
    
    db.session.commit()
    logger.info(f"Membro da família {member_id} atualizado")
    
    return jsonify({'message': 'Membro da família atualizado com sucesso!'}), 200

@user_bp.route('/family/<int:member_id>', methods=['DELETE'])
@login_required
def delete_family_member(member_id):
    user_id = session.get('user_id')
    
    # Buscar membro da família
    family_member = FamilyMember.query.get(member_id)
    
    if not family_member:
        return jsonify({'message': 'Membro da família não encontrado.'}), 404
    
    # Verificar permissão
    if family_member.user_id != user_id and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para excluir este membro da família.'}), 403
    
    db.session.delete(family_member)
    db.session.commit()
    logger.info(f"Membro da família {member_id} excluído")
    
    return jsonify({'message': 'Membro da família excluído com sucesso!'}), 200

@user_bp.route('/emergency-contact', methods=['POST'])
@login_required
def add_emergency_contact():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado.'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('phone') or not data.get('relationship'):
        return jsonify({'message': 'Dados incompletos. Por favor, forneça nome, telefone e relacionamento.'}), 400
    
    # Criar novo contato de emergência
    new_contact = EmergencyContact(
        name=data['name'],
        phone=data['phone'],
        relationship=data['relationship'],
        user_id=user_id
    )
    
    db.session.add(new_contact)
    db.session.commit()
    
    logger.info(f"Novo contato de emergência adicionado para o usuário {user.username}")
    
    return jsonify({
        'message': 'Contato de emergência adicionado com sucesso!',
        'contact_id': new_contact.id
    }), 201

@user_bp.route('/emergency-contact/<int:contact_id>', methods=['PUT'])
@login_required
def update_emergency_contact(contact_id):
    user_id = session.get('user_id')
    
    # Buscar contato de emergência
    contact = EmergencyContact.query.get(contact_id)
    
    if not contact:
        return jsonify({'message': 'Contato de emergência não encontrado.'}), 404
    
    # Verificar permissão
    if contact.user_id != user_id and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para editar este contato de emergência.'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Nenhum dado fornecido para atualização.'}), 400
    
    # Atualizar campos
    if 'name' in data:
        contact.name = data['name']
    
    if 'phone' in data:
        contact.phone = data['phone']
    
    if 'relationship' in data:
        contact.relationship = data['relationship']
    
    db.session.commit()
    logger.info(f"Contato de emergência {contact_id} atualizado")
    
    return jsonify({'message': 'Contato de emergência atualizado com sucesso!'}), 200

@user_bp.route('/emergency-contact/<int:contact_id>', methods=['DELETE'])
@login_required
def delete_emergency_contact(contact_id):
    user_id = session.get('user_id')
    
    # Buscar contato de emergência
    contact = EmergencyContact.query.get(contact_id)
    
    if not contact:
        return jsonify({'message': 'Contato de emergência não encontrado.'}), 404
    
    # Verificar permissão
    if contact.user_id != user_id and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para excluir este contato de emergência.'}), 403
    
    db.session.delete(contact)
    db.session.commit()
    logger.info(f"Contato de emergência {contact_id} excluído")
    
    return jsonify({'message': 'Contato de emergência excluído com sucesso!'}), 200

@user_bp.route('/notifications', methods=['GET'])
@login_required
def get_notifications():
    user_id = session.get('user_id')
    
    # Buscar notificações não lidas
    notifications = Notification.query.filter_by(user_id=user_id, is_read=False).order_by(Notification.created_at.desc()).all()
    
    result = []
    for notification in notifications:
        result.append({
            'id': notification.id,
            'title': notification.title,
            'message': notification.message,
            'notification_type': notification.notification_type,
            'created_at': notification.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({'notifications': result}), 200

@user_bp.route('/notifications/<int:notification_id>/mark-read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    user_id = session.get('user_id')
    
    # Buscar notificação
    notification = Notification.query.get(notification_id)
    
    if not notification:
        return jsonify({'message': 'Notificação não encontrada.'}), 404
    
    # Verificar permissão
    if notification.user_id != user_id and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para marcar esta notificação como lida.'}), 403
    
    notification.is_read = True
    db.session.commit()
    
    return jsonify({'message': 'Notificação marcada como lida.'}), 200

@user_bp.route('/notifications/mark-all-read', methods=['POST'])
@login_required
def mark_all_notifications_read():
    user_id = session.get('user_id')
    
    # Buscar todas as notificações não lidas
    notifications = Notification.query.filter_by(user_id=user_id, is_read=False).all()
    
    for notification in notifications:
        notification.is_read = True
    
    db.session.commit()
    
    return jsonify({'message': 'Todas as notificações marcadas como lidas.'}), 200

@user_bp.route('/motorcycle', methods=['POST'])
@login_required
def add_motorcycle():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado.'}), 404
    
    data = request.get_json()
    
    if not data or not data.get('brand') or not data.get('model'):
        return jsonify({'message': 'Dados incompletos. Por favor, forneça marca e modelo.'}), 400
    
    # Converter data de vencimento do IPVA, se fornecida
    ipva_due_date = None
    if data.get('ipva_due_date'):
        try:
            ipva_due_date = datetime.strptime(data['ipva_due_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'message': 'Formato de data inválido para data de vencimento do IPVA.'}), 400
    
    # Criar nova motocicleta
    new_motorcycle = Motorcycle(
        brand=data['brand'],
        model=data['model'],
        manufacturing_year=data.get('manufacturing_year'),
        model_year=data.get('model_year'),
        chassis_number=data.get('chassis_number'),
        engine_number=data.get('engine_number'),
        license_plate=data.get('license_plate'),
        ipva_due_date=ipva_due_date,
        user_id=user_id
    )
    
    db.session.add(new_motorcycle)
    db.session.commit()
    
    logger.info(f"Nova motocicleta adicionada para o usuário {user.username}")
    
    return jsonify({
        'message': 'Motocicleta adicionada com sucesso!',
        'motorcycle_id': new_motorcycle.id
    }), 201

@user_bp.route('/motorcycle/<int:motorcycle_id>', methods=['PUT'])
@login_required
def update_motorcycle(motorcycle_id):
    user_id = session.get('user_id')
    
    # Buscar motocicleta
    motorcycle = Motorcycle.query.get(motorcycle_id)
    
    if not motorcycle:
        return jsonify({'message': 'Motocicleta não encontrada.'}), 404
    
    # Verificar permissão
    if motorcycle.user_id != user_id and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para editar esta motocicleta.'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Nenhum dado fornecido para atualização.'}), 400
    
    # Atualizar campos
    if 'brand' in data:
        motorcycle.brand = data['brand']
    
    if 'model' in data:
        motorcycle.model = data['model']
    
    if 'manufacturing_year' in data:
        motorcycle.manufacturing_year = data['manufacturing_year']
    
    if 'model_year' in data:
        motorcycle.model_year = data['model_year']
    
    if 'chassis_number' in data:
        motorcycle.chassis_number = data['chassis_number']
    
    if 'engine_number' in data:
        motorcycle.engine_number = data['engine_number']
    
    if 'license_plate' in data:
        motorcycle.license_plate = data['license_plate']
    
    if 'ipva_due_date' in data:
        if data['ipva_due_date']:
            try:
                motorcycle.ipva_due_date = datetime.strptime(data['ipva_due_date'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'message': 'Formato de data inválido para data de vencimento do IPVA.'}), 400
        else:
            motorcycle.ipva_due_date = None
    
    db.session.commit()
    logger.info(f"Motocicleta {motorcycle_id} atualizada")
    
    return jsonify({'message': 'Motocicleta atualizada com sucesso!'}), 200

@user_bp.route('/motorcycle/<int:motorcycle_id>', methods=['DELETE'])
@login_required
def delete_motorcycle(motorcycle_id):
    user_id = session.get('user_id')
    
    # Buscar motocicleta
    motorcycle = Motorcycle.query.get(motorcycle_id)
    
    if not motorcycle:
        return jsonify({'message': 'Motocicleta não encontrada.'}), 404
    
    # Verificar permissão
    if motorcycle.user_id != user_id and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para excluir esta motocicleta.'}), 403
    
    # Excluir imagens da motocicleta
    images = MotorcycleImage.query.filter_by(motorcycle_id=motorcycle_id).all()
    for image in images:
        db.session.delete(image)
    
    db.session.delete(motorcycle)
    db.session.commit()
    logger.info(f"Motocicleta {motorcycle_id} excluída")
    
    return jsonify({'message': 'Motocicleta excluída com sucesso!'}), 200

@user_bp.route('/motorcycle/<int:motorcycle_id>/image', methods=['POST'])
@login_required
def add_motorcycle_image(motorcycle_id):
    user_id = session.get('user_id')
    
    # Buscar motocicleta
    motorcycle = Motorcycle.query.get(motorcycle_id)
    
    if not motorcycle:
        return jsonify({'message': 'Motocicleta não encontrada.'}), 404
    
    # Verificar permissão
    if motorcycle.user_id != user_id and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para adicionar imagens a esta motocicleta.'}), 403
    
    if 'file' not in request.files:
        return jsonify({'message': 'Nenhum arquivo enviado.'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'Nenhum arquivo selecionado.'}), 400
    
    if file and allowed_file(file.filename):
        # Garantir que o diretório de upload exista
        os.makedirs(MOTORCYCLE_UPLOAD_FOLDER, exist_ok=True)
        
        # Criar nome de arquivo único
        filename = secure_filename(f"moto_{motorcycle_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file.filename.rsplit('.', 1)[1].lower()}")
        
        # Salvar o arquivo
        file_path = os.path.join(MOTORCYCLE_UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        # Criar nova imagem
        caption = request.form.get('caption', '')
        
        new_image = MotorcycleImage(
            motorcycle_id=motorcycle_id,
            image_url=f'/static/images/motorcycles/{filename}',
            caption=caption
        )
        
        db.session.add(new_image)
        db.session.commit()
        
        logger.info(f"Nova imagem adicionada à motocicleta {motorcycle_id}")
        
        return jsonify({
            'message': 'Imagem adicionada com sucesso!',
            'image_id': new_image.id,
            'image_url': new_image.image_url
        }), 201
    
    return jsonify({'message': 'Tipo de arquivo não permitido.'}), 400

@user_bp.route('/motorcycle/image/<int:image_id>', methods=['PUT'])
@login_required
def update_motorcycle_image(image_id):
    user_id = session.get('user_id')
    
    # Buscar imagem
    image = MotorcycleImage.query.get(image_id)
    
    if not image:
        return jsonify({'message': 'Imagem não encontrada.'}), 404
    
    # Buscar motocicleta
    motorcycle = Motorcycle.query.get(image.motorcycle_id)
    
    # Verificar permissão
    if motorcycle.user_id != user_id and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para editar esta imagem.'}), 403
    
    data = request.get_json()
    
    if not data:
        return jsonify({'message': 'Nenhum dado fornecido para atualização.'}), 400
    
    # Atualizar legenda
    if 'caption' in data:
        image.caption = data['caption']
        db.session.commit()
        logger.info(f"Legenda da imagem {image_id} atualizada")
    
    return jsonify({'message': 'Legenda da imagem atualizada com sucesso!'}), 200

@user_bp.route('/motorcycle/image/<int:image_id>', methods=['DELETE'])
@login_required
def delete_motorcycle_image(image_id):
    user_id = session.get('user_id')
    
    # Buscar imagem
    image = MotorcycleImage.query.get(image_id)
    
    if not image:
        return jsonify({'message': 'Imagem não encontrada.'}), 404
    
    # Buscar motocicleta
    motorcycle = Motorcycle.query.get(image.motorcycle_id)
    
    # Verificar permissão
    if motorcycle.user_id != user_id and not session.get('is_admin', False):
        return jsonify({'message': 'Você não tem permissão para excluir esta imagem.'}), 403
    
    db.session.delete(image)
    db.session.commit()
    logger.info(f"Imagem {image_id} excluída")
    
    return jsonify({'message': 'Imagem excluída com sucesso!'}), 200
