#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Backend para Tribo do Cerrado - Versão Vercel
Conecta com PostgreSQL Neon e fornece endpoints para o frontend
"""

from flask import Flask, request, jsonify
import os
import hashlib
import json
from datetime import datetime

app = Flask(__name__)

# Configurações do banco de dados
DATABASE_URL = os.environ.get('DATABASE_URL', '')
MIGADU_API_KEY = os.environ.get('MIGADU_API_KEY', '')
MIGADU_DOMAIN = os.environ.get('MIGADU_DOMAIN', 'tribodocerrado.org')

# Dados simulados para funcionamento (enquanto conectamos com PostgreSQL)
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

def handler(request):
    """Handler principal para Vercel"""
    
    # Configurar CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Content-Type': 'application/json'
    }
    
    # Tratar OPTIONS (preflight)
    if request.method == 'OPTIONS':
        return ('', 200, headers)
    
    try:
        # Parse da URL
        path = request.path
        method = request.method
        
        # Obter dados JSON se POST
        data = {}
        if method == 'POST' and hasattr(request, 'get_json'):
            try:
                data = request.get_json() or {}
            except:
                data = {}
        
        # Roteamento
        if path == '/api/test' and method == 'GET':
            response = {
                "status": "success",
                "message": "API Tribo do Cerrado funcionando no Vercel!",
                "timestamp": datetime.now().isoformat(),
                "version": "2.0.0",
                "environment": "vercel"
            }
            
        elif path == '/api/login' and method == 'POST':
            email = data.get('email', '').lower().strip()
            senha = data.get('senha', '')
            
            if not email or not senha:
                response = {
                    "status": "error",
                    "message": "Email e senha são obrigatórios"
                }
                return (json.dumps(response), 400, headers)
            
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
                return (json.dumps(response), 401, headers)
            
            if usuario['status'] != 'ativo':
                response = {
                    "status": "error",
                    "message": "Usuário inativo"
                }
                return (json.dumps(response), 401, headers)
            
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
            
        elif path == '/api/usuarios' and method == 'GET':
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
            
        elif path == '/api/eventos' and method == 'GET':
            response = {
                "status": "success",
                "eventos": eventos_demo,
                "total": len(eventos_demo)
            }
            
        elif path == '/api/cadastro' and method == 'POST':
            # Validações básicas
            campos_obrigatorios = ['nome', 'email', 'senha']
            for campo in campos_obrigatorios:
                if not data.get(campo):
                    response = {
                        "status": "error",
                        "message": f"Campo {campo} é obrigatório"
                    }
                    return (json.dumps(response), 400, headers)
            
            email = data['email'].lower().strip()
            
            # Verificar se email já existe
            for u in usuarios_demo:
                if u['email'].lower() == email:
                    response = {
                        "status": "error",
                        "message": "Email já cadastrado"
                    }
                    return (json.dumps(response), 400, headers)
            
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
            
        elif path == '/api/email/send' and method == 'POST':
            # Simular envio de email
            response = {
                "status": "success",
                "message": "Email enviado com sucesso",
                "email_id": f"email_{datetime.now().timestamp()}"
            }
            
        elif path == '/api/status' and method == 'GET':
            response = {
                "status": "success",
                "sistema": {
                    "banco_dados": "Simulado",
                    "api_migadu": "Configurada" if MIGADU_API_KEY else "Não configurada",
                    "sistema_email": "Operacional",
                    "controle_usuarios": "Ativo",
                    "total_usuarios": len(usuarios_demo),
                    "total_eventos": len(eventos_demo),
                    "environment": "vercel"
                },
                "timestamp": datetime.now().isoformat()
            }
            
        else:
            response = {
                "status": "error",
                "message": f"Endpoint não encontrado: {method} {path}",
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
            return (json.dumps(response), 404, headers)
        
        return (json.dumps(response), 200, headers)
        
    except Exception as e:
        error_response = {
            "status": "error",
            "message": f"Erro interno do servidor: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }
        return (json.dumps(error_response), 500, headers)

# Para desenvolvimento local
if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, handler, use_debugger=True, use_reloader=True)

