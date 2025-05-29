from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

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
