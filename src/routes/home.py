from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    """Rota para a página inicial pública do site"""
    return render_template('public/home.html')
