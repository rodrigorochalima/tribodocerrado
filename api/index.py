#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Backend para Tribo do Cerrado - Versão Vercel Serverless
"""

from http.server import BaseHTTPRequestHandler
import json
import hashlib
from datetime import datetime
import urllib.parse

# Dados simulados para funcionamento
usuarios_demo = [
    {
        "id": 1,
        "nome": "Administrador",
        "email": "admin@tribodocerrado.org",
        "senha": hashlib.sha256("123456".encode()).hexdigest(),
        "tipo": "administrador",
        "status": "ativo",
        "data_cadastro": "2025-01-01"
    },
    {
        "id": 2,
        "nome": "Rocha Lima",
        "email": "rochalima@tribodocerrado.org",
        "senha": hashlib.sha256("MinhaSenh@123!".encode()).hexdigest(),
        "tipo": "usuario",
        "status": "ativo",
        "data_cadastro": "2025-01-02"
    }
]

eventos_demo = [
    {
        "id": 1,
        "titulo": "Encontro Mensal - Janeiro",
        "data": "2025-01-15",
        "local": "Parque Vaca Brava",
        "descricao": "Encontro mensal da Tribo do Cerrado",
        "status": "ativo"
    },
    {
        "id": 2,
        "titulo": "Trilha do Cerrado",
        "data": "2025-01-22",
        "local": "Chapada dos Veadeiros",
        "descricao": "Trilha ecológica pela Chapada",
        "status": "ativo"
    },
    {
        "id": 3,
        "titulo": "Workshop de Mecânica",
        "data": "2025-01-29",
        "local": "Sede do Clube",
        "descricao": "Workshop sobre manutenção de motos",
        "status": "ativo"
    }
]

class handler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests"""
        try:
            path = self.path
            
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.end_headers()
            
            if path == '/api/test' or path == '/api/':
                response = {
                    "status": "success",
                    "message": "API Tribo do Cerrado funcionando no Vercel!",
                    "timestamp": datetime.now().isoformat(),
                    "version": "3.0.0",
                    "environment": "vercel-serverless"
                }
                
            elif path == '/api/usuarios':
                usuarios_safe = []
                for u in usuarios_demo:
                    usuarios_safe.append({
                        "id": u['id'],
                        "nome": u['nome'],
                        "email": u['email'],
                        "tipo": u['tipo'],
                        "status": u['status'],
                        "data_cadastro": u['data_cadastro']
                    })
                
                response = {
                    "status": "success",
                    "usuarios": usuarios_safe,
                    "total": len(usuarios_safe)
                }
                
            elif path == '/api/eventos':
                response = {
                    "status": "success",
                    "eventos": eventos_demo,
                    "total": len(eventos_demo)
                }
                
            elif path == '/api/status':
                response = {
                    "status": "success",
                    "sistema": {
                        "banco_dados": "Simulado",
                        "api_migadu": "Configurada",
                        "sistema_email": "Operacional",
                        "controle_usuarios": "Ativo",
                        "total_usuarios": len(usuarios_demo),
                        "total_eventos": len(eventos_demo),
                        "environment": "vercel-serverless"
                    },
                    "timestamp": datetime.now().isoformat()
                }
                
            else:
                response = {
                    "status": "error",
                    "message": f"Endpoint não encontrado: GET {path}",
                    "available_endpoints": [
                        "GET /api/test",
                        "POST /api/login",
                        "GET /api/usuarios",
                        "GET /api/eventos",
                        "POST /api/cadastro",
                        "GET /api/status"
                    ]
                }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                "status": "error",
                "message": f"Erro interno do servidor: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))

    def do_POST(self):
        """Handle POST requests"""
        try:
            path = self.path
            
            # Read request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8')) if post_data else {}
            except:
                data = {}
            
            # Set CORS headers
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
            self.end_headers()
            
            if path == '/api/login':
                email = data.get('email', '').lower().strip()
                senha = data.get('senha', '')
                
                if not email or not senha:
                    response = {
                        "status": "error",
                        "message": "Email e senha são obrigatórios"
                    }
                else:
                    # Hash da senha fornecida
                    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
                    
                    # Buscar usuário
                    usuario = None
                    for u in usuarios_demo:
                        if u['email'].lower() == email and u['senha'] == senha_hash:
                            usuario = u
                            break
                    
                    if not usuario:
                        response = {
                            "status": "error",
                            "message": "Email ou senha incorretos"
                        }
                    elif usuario['status'] != 'ativo':
                        response = {
                            "status": "error",
                            "message": "Usuário inativo"
                        }
                    else:
                        # Login bem-sucedido
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
                        
            elif path == '/api/cadastro':
                # Validações básicas
                campos_obrigatorios = ['nome', 'email', 'senha']
                for campo in campos_obrigatorios:
                    if not data.get(campo):
                        response = {
                            "status": "error",
                            "message": f"Campo {campo} é obrigatório"
                        }
                        break
                else:
                    email = data['email'].lower().strip()
                    
                    # Verificar se email já existe
                    email_existe = False
                    for u in usuarios_demo:
                        if u['email'].lower() == email:
                            email_existe = True
                            break
                    
                    if email_existe:
                        response = {
                            "status": "error",
                            "message": "Email já cadastrado"
                        }
                    else:
                        # Criar novo usuário
                        novo_usuario = {
                            "id": len(usuarios_demo) + 1,
                            "nome": data['nome'],
                            "email": email,
                            "senha": hashlib.sha256(data['senha'].encode()).hexdigest(),
                            "tipo": "usuario",
                            "status": "ativo",
                            "data_cadastro": datetime.now().strftime("%Y-%m-%d")
                        }
                        
                        usuarios_demo.append(novo_usuario)
                        
                        response = {
                            "status": "success",
                            "message": "Usuário cadastrado com sucesso",
                            "usuario": {
                                "id": novo_usuario['id'],
                                "nome": novo_usuario['nome'],
                                "email": novo_usuario['email'],
                                "tipo": novo_usuario['tipo']
                            }
                        }
                        
            elif path == '/api/email/send':
                # Simular envio de email
                response = {
                    "status": "success",
                    "message": "Email enviado com sucesso",
                    "email_id": f"email_{datetime.now().timestamp()}"
                }
                
            else:
                response = {
                    "status": "error",
                    "message": f"Endpoint não encontrado: POST {path}",
                    "available_endpoints": [
                        "GET /api/test",
                        "POST /api/login",
                        "GET /api/usuarios",
                        "GET /api/eventos",
                        "POST /api/cadastro",
                        "POST /api/email/send",
                        "GET /api/status"
                    ]
                }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                "status": "error",
                "message": f"Erro interno do servidor: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
            self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))

