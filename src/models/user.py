from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.db import db
import uuid

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    nickname = db.Column(db.String(80))
    birth_date = db.Column(db.Date)
    blood_type = db.Column(db.String(10))
    profile_image = db.Column(db.String(255))
    address_street = db.Column(db.String(255))
    address_number = db.Column(db.String(20))
    address_complement = db.Column(db.String(255))
    address_district = db.Column(db.String(255))
    address_city = db.Column(db.String(255))
    address_state = db.Column(db.String(2))
    address_zipcode = db.Column(db.String(20))
    health_notes = db.Column(db.Text)
    health_insurance = db.Column(db.String(255))
    health_insurance_number = db.Column(db.String(255))
    collection_date = db.Column(db.Date)
    join_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)  # Alterado para False por padrão (até confirmação de email)
    
    # Campos de privacidade
    is_public_profile = db.Column(db.Boolean, default=False)
    is_public_full_name = db.Column(db.Boolean, default=False)
    is_public_birth_date = db.Column(db.Boolean, default=False)
    is_public_blood_type = db.Column(db.Boolean, default=False)
    is_public_address = db.Column(db.Boolean, default=False)
    is_public_health_info = db.Column(db.Boolean, default=False)
    is_public_collection_date = db.Column(db.Boolean, default=False)
    is_public_join_date = db.Column(db.Boolean, default=True)
    
    # Campos para confirmação de email
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmation_token = db.Column(db.String(100), unique=True)
    email_confirmation_sent_at = db.Column(db.DateTime)
    
    # Campos para segurança
    failed_login_attempts = db.Column(db.Integer, default=0)
    last_failed_login = db.Column(db.DateTime)
    account_locked_until = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def generate_confirmation_token(self):
        """Gera um token único para confirmação de email"""
        self.email_confirmation_token = str(uuid.uuid4())
        self.email_confirmation_sent_at = datetime.utcnow()
        return self.email_confirmation_token
    
    def confirm_email(self):
        """Confirma o email do usuário"""
        self.email_confirmed = True
        self.is_active = True
        self.email_confirmation_token = None
        
    def can_edit_profile(self):
        """Verifica se o usuário pode editar seu perfil"""
        return self.email_confirmed and self.is_active
    
    def increment_failed_login(self):
        """Incrementa o contador de tentativas de login falhas"""
        self.failed_login_attempts = (self.failed_login_attempts or 0) + 1
        self.last_failed_login = datetime.utcnow()
        
        # Se houver muitas tentativas falhas, bloqueia a conta temporariamente
        if self.failed_login_attempts >= 5:
            from datetime import timedelta
            self.account_locked_until = datetime.utcnow() + timedelta(minutes=30)
    
    def reset_failed_login(self):
        """Reseta o contador de tentativas de login falhas"""
        self.failed_login_attempts = 0
        self.last_failed_login = None
        self.account_locked_until = None
    
    def is_account_locked(self):
        """Verifica se a conta está bloqueada temporariamente"""
        if not self.account_locked_until:
            return False
        return datetime.utcnow() < self.account_locked_until
    
    def __repr__(self):
        return f'<User {self.username}>'

class EmergencyContact(db.Model):
    __tablename__ = 'emergency_contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    relationship = db.Column(db.String(50))
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    address = db.Column(db.String(255))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('emergency_contacts', lazy=True))
    
    def __repr__(self):
        return f'<EmergencyContact {self.name}>'
