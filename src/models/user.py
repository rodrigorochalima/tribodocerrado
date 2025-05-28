from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.db import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    nickname = db.Column(db.String(50), nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    birth_date = db.Column(db.Date, nullable=True)
    collection_date = db.Column(db.Date, nullable=True)  # Data de coletamento (entrada no motoclube)
    blood_type = db.Column(db.String(10), nullable=True)
    
    # Endereço
    address_street = db.Column(db.String(255), nullable=True)
    address_number = db.Column(db.String(20), nullable=True)
    address_complement = db.Column(db.String(100), nullable=True)
    address_district = db.Column(db.String(100), nullable=True)
    address_city = db.Column(db.String(100), nullable=True)
    address_state = db.Column(db.String(50), nullable=True)
    address_zipcode = db.Column(db.String(20), nullable=True)
    
    # Informações de saúde
    health_notes = db.Column(db.Text, nullable=True)
    health_insurance = db.Column(db.String(100), nullable=True)
    health_insurance_number = db.Column(db.String(50), nullable=True)
    
    # Relacionamentos
    godfather_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    # Controle de acesso
    is_admin = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Controle de privacidade (quais campos são visíveis publicamente)
    full_name_public = db.Column(db.Boolean, default=False)
    birth_date_public = db.Column(db.Boolean, default=False)
    collection_date_public = db.Column(db.Boolean, default=False)
    blood_type_public = db.Column(db.Boolean, default=False)
    address_public = db.Column(db.Boolean, default=False)
    bio_public = db.Column(db.Boolean, default=False)
    health_info_public = db.Column(db.Boolean, default=False)
    
    def __repr__(self):
        return f'<User {self.username}>'
        
    # Métodos necessários para Flask-Login
    def is_authenticated(self):
        return True
        
    def is_active(self):
        return self.is_approved
        
    def is_anonymous(self):
        return False
        
    def get_id(self):
        return str(self.id)

class EmergencyContact(db.Model):
    __tablename__ = 'emergency_contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref=db.backref('emergency_contacts', lazy=True))
    
    def __repr__(self):
        return f'<EmergencyContact {self.name}>'

class MotorcycleImage(db.Model):
    __tablename__ = 'motorcycle_images'
    
    id = db.Column(db.Integer, primary_key=True)
    motorcycle_id = db.Column(db.Integer, db.ForeignKey('motorcycles.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    motorcycle = db.relationship('Motorcycle', backref=db.backref('images', lazy=True))
    
    def __repr__(self):
        return f'<MotorcycleImage {self.id}>'
