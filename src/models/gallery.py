from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.db import db

class Gallery(db.Model):
    __tablename__ = 'galleries'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_date = db.Column(db.Date, nullable=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    created_by = db.relationship('User', backref=db.backref('galleries', lazy=True))
    
    def __repr__(self):
        return f'<Gallery {self.title}>'

class GalleryImage(db.Model):
    __tablename__ = 'gallery_images'
    
    id = db.Column(db.Integer, primary_key=True)
    gallery_id = db.Column(db.Integer, db.ForeignKey('galleries.id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255), nullable=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    gallery = db.relationship('Gallery', backref=db.backref('images', lazy=True))
    
    def __repr__(self):
        return f'<GalleryImage {self.id}>'

class GalleryAlbum(db.Model):
    __tablename__ = 'gallery_albums'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cover_image_id = db.Column(db.Integer, db.ForeignKey('gallery_images.id'), nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    creator = db.relationship('User', backref=db.backref('gallery_albums', lazy=True))
    cover_image = db.relationship('GalleryImage')
    
    def __repr__(self):
        return f'<GalleryAlbum {self.title}>'

# Tabela de associação entre álbuns e imagens (muitos para muitos)
album_images = db.Table('album_images',
    db.Column('album_id', db.Integer, db.ForeignKey('gallery_albums.id'), primary_key=True),
    db.Column('image_id', db.Integer, db.ForeignKey('gallery_images.id'), primary_key=True)
)
