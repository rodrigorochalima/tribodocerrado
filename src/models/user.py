from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from src.models.db import db

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
    is_active = db.Column(db.Boolean, default=True)
    
    # Campos de privacidade
    is_public_profile = db.Column(db.Boolean, default=False)
    is_public_full_name = db.Column(db.Boolean, default=False)
    is_public_birth_date = db.Column(db.Boolean, default=False)
    is_public_blood_type = db.Column(db.Boolean, default=False)
    is_public_address = db.Column(db.Boolean, default=False)
    is_public_health_info = db.Column(db.Boolean, default=False)
    is_public_collection_date = db.Column(db.Boolean, default=False)
    is_public_join_date = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
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

class Motorcycle(db.Model):
    __tablename__ = 'motorcycles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer)
    license_plate = db.Column(db.String(20))
    color = db.Column(db.String(30))
    chassis_number = db.Column(db.String(50))
    engine_number = db.Column(db.String(50))
    purchase_date = db.Column(db.Date)
    insurance_company = db.Column(db.String(100))
    insurance_policy = db.Column(db.String(50))
    insurance_expiry = db.Column(db.Date)
    ipva_due_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref=db.backref('motorcycles', lazy=True))
    
    def __repr__(self):
        return f'<Motorcycle {self.brand} {self.model}>'

class MotorcycleImage(db.Model):
    __tablename__ = 'motorcycle_images'
    
    id = db.Column(db.Integer, primary_key=True)
    motorcycle_id = db.Column(db.Integer, db.ForeignKey('motorcycles.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    motorcycle = db.relationship('Motorcycle', backref=db.backref('images', lazy=True))
    
    def __repr__(self):
        return f'<MotorcycleImage {self.id}>'
