from flask_login import UserMixin
from .db import db
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(200))
    nickname = db.Column(db.String(100))
    profile_image = db.Column(db.String(200))
    bio = db.Column(db.Text)
    birth_date = db.Column(db.Date)
    collection_date = db.Column(db.Date)
    blood_type = db.Column(db.String(10))
    address_street = db.Column(db.String(200))
    address_number = db.Column(db.String(20))
    address_complement = db.Column(db.String(100))
    address_district = db.Column(db.String(100))
    address_city = db.Column(db.String(100))
    address_state = db.Column(db.String(50))
    address_zipcode = db.Column(db.String(20))
    health_notes = db.Column(db.Text)
    health_insurance = db.Column(db.String(100))
    health_insurance_number = db.Column(db.String(100))
    godfather_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_admin = db.Column(db.Boolean, default=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<User {self.username}>'
