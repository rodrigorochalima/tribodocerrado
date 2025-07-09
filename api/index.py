from http.server import BaseHTTPRequestHandler
import json
import hashlib
from datetime import datetime

# Dados simulados
usuarios = [
    {
        "id": 1,
        "nome": "Administrador",
        "email": "admin@tribodocerrado.org",
        "senha": hashlib.sha256("123456".encode()).hexdigest(),
        "tipo": "administrador"
    },
    {
        "id": 2,
        "nome": "Rocha Lima",
        "email": "rochalima@tribodocerrado.org",
        "senha": hashlib.sha256("MinhaSenh@123!".encode()).hexdigest(),
        "tipo": "usuario"
    }
]

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            "status": "success",
            "message": "API Tribo do Cerrado funcionando!",
            "timestamp": datetime.now().isoformat(),
            "path": self.path
        }
        
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8')) if post_data else {}
        except:
            data = {}
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        if self.path == '/api/login':
            email = data.get('email', '').lower()
            senha = data.get('senha', '')
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            
            usuario = None
            for u in usuarios:
                if u['email'].lower() == email and u['senha'] == senha_hash:
                    usuario = u
                    break
            
            if usuario:
                response = {
                    "status": "success",
                    "message": "Login realizado com sucesso",
                    "usuario": {
                        "id": usuario['id'],
                        "nome": usuario['nome'],
                        "email": usuario['email'],
                        "tipo": usuario['tipo']
                    }
                }
            else:
                response = {
                    "status": "error",
                    "message": "Email ou senha incorretos"
                }
        
        elif self.path == '/api/cadastro':
            response = {
                "status": "success",
                "message": "Usuário cadastrado com sucesso",
                "data": data
            }
        
        else:
            response = {
                "status": "success",
                "message": "API funcionando",
                "path": self.path,
                "data": data
            }
        
        self.wfile.write(json.dumps(response).encode())

