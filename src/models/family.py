from datetime import datetime
from src.models.db import db

class FamilyMember(db.Model):
    __tablename__ = 'family_members'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Informações básicas
    full_name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date)
    phone = db.Column(db.String(20))
    
    # Informações de saúde
    blood_type = db.Column(db.String(10))
    health_insurance = db.Column(db.String(100))
    health_notes = db.Column(db.Text)
    
    # Imagem e observações
    image_url = db.Column(db.String(255))
    notes = db.Column(db.Text)
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref=db.backref('family_members', lazy=True))
    
    def __repr__(self):
        return f'<FamilyMember {self.full_name} ({self.relationship})>'
