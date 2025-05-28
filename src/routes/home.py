from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    """Rota principal que exibe a homepage pública"""
    return render_template('public/home.html')
