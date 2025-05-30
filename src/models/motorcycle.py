from datetime import datetime
from src.models.db import db

class Motorcycle(db.Model):
    __tablename__ = 'motorcycles'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Informações básicas
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    manufacturing_year = db.Column(db.Integer, nullable=False)
    model_year = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(50))
    license_plate = db.Column(db.String(20))
    engine_capacity = db.Column(db.String(20))
    
    # Datas importantes
    purchase_date = db.Column(db.Date)
    ipva_due_date = db.Column(db.Date)
    insurance_due_date = db.Column(db.Date)
    
    # Seguro
    insurance_company = db.Column(db.String(100))
    
    # Manutenção
    last_maintenance = db.Column(db.Date)
    next_maintenance = db.Column(db.Date)
    maintenance_notes = db.Column(db.Text)
    
    # Imagem e observações
    image_url = db.Column(db.String(255))
    notes = db.Column(db.Text)
    
    # Metadados
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    user = db.relationship('User', backref=db.backref('motorcycles', lazy=True))
    
    def __repr__(self):
        return f'<Motorcycle {self.brand} {self.model} ({self.model_year})>'
