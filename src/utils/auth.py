from functools import wraps
from flask import session, redirect, url_for, jsonify, request

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'message': 'Autenticação necessária.'}), 401
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'message': 'Autenticação necessária.'}), 401
            return redirect(url_for('auth.login', next=request.url))
        
        if not session.get('is_admin', False):
            if request.headers.get('Content-Type') == 'application/json':
                return jsonify({'message': 'Acesso restrito a administradores.'}), 403
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function
