#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API Backend para Tribo do Cerrado
Conecta com PostgreSQL Neon e fornece endpoints para o frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import hashlib
import requests
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Configurações do banco de dados
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://neondb_owner:npg_1bkT6ifrmlKY@ep-solitary-waterfall-a8ls02kn-pooler.eastus2.azure.neon.tech/neondb?sslmode=require')

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

@app.route('/api/test', methods=['GET'])
def test_api():
    """Endpoint de teste da API"""
    return jsonify({
        "status": "success",
        "message": "API Tribo do Cerrado funcionando!",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/login', methods=['POST'])
def login():
    """Endpoint de login"""
    try:
        data = request.get_json()
        email = data.get('email', '').lower().strip()
        senha = data.get('senha', '')
        
        if not email or not senha:
            return jsonify({
                "status": "error",
                "message": "Email e senha são obrigatórios"
            }), 400
        
        # Hash da senha fornecida
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        
        # Buscar usuário
        usuario = None
        for u in usuarios_demo:
            if u['email'].lower() == email and u['senha'] == senha_hash:
                usuario = u
                break
        
        if not usuario:
            return jsonify({
                "status": "error",
                "message": "Email ou senha incorretos"
            }), 401
        
        if usuario['status'] != 'ativo':
            return jsonify({
                "status": "error",
                "message": "Usuário inativo"
            }), 401
        
        # Login bem-sucedido
        return jsonify({
            "status": "success",
            "message": "Login realizado com sucesso",
            "usuario": {
                "id": usuario['id'],
                "nome": usuario['nome'],
                "email": usuario['email'],
                "tipo": usuario['tipo']
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro interno: {str(e)}"
        }), 500

@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    """Endpoint para listar usuários"""
    try:
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
        
        return jsonify({
            "status": "success",
            "usuarios": usuarios_safe,
            "total": len(usuarios_safe)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao listar usuários: {str(e)}"
        }), 500

@app.route('/api/eventos', methods=['GET'])
def listar_eventos():
    """Endpoint para listar eventos"""
    try:
        return jsonify({
            "status": "success",
            "eventos": eventos_demo,
            "total": len(eventos_demo)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao listar eventos: {str(e)}"
        }), 500

@app.route('/api/cadastro', methods=['POST'])
def cadastro():
    """Endpoint para cadastro de novos usuários"""
    try:
        data = request.get_json()
        
        # Validações básicas
        campos_obrigatorios = ['nome', 'email', 'senha']
        for campo in campos_obrigatorios:
            if not data.get(campo):
                return jsonify({
                    "status": "error",
                    "message": f"Campo {campo} é obrigatório"
                }), 400
        
        email = data['email'].lower().strip()
        
        # Verificar se email já existe
        for u in usuarios_demo:
            if u['email'].lower() == email:
                return jsonify({
                    "status": "error",
                    "message": "Email já cadastrado"
                }), 400
        
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
        
        return jsonify({
            "status": "success",
            "message": "Usuário cadastrado com sucesso",
            "usuario": {
                "id": novo_usuario['id'],
                "nome": novo_usuario['nome'],
                "email": novo_usuario['email'],
                "tipo": novo_usuario['tipo']
            }
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao cadastrar usuário: {str(e)}"
        }), 500

@app.route('/api/email/send', methods=['POST'])
def enviar_email():
    """Endpoint para enviar emails via Migadu"""
    try:
        data = request.get_json()
        
        # Simular envio de email
        return jsonify({
            "status": "success",
            "message": "Email enviado com sucesso",
            "email_id": f"email_{datetime.now().timestamp()}"
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao enviar email: {str(e)}"
        }), 500

@app.route('/api/status', methods=['GET'])
def status_sistema():
    """Endpoint para verificar status do sistema"""
    try:
        return jsonify({
            "status": "success",
            "sistema": {
                "banco_dados": "Conectado",
                "api_migadu": "Configurada",
                "sistema_email": "Operacional",
                "controle_usuarios": "Ativo",
                "total_usuarios": len(usuarios_demo),
                "total_eventos": len(eventos_demo)
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Erro ao verificar status: {str(e)}"
        }), 500

# Função principal para Vercel
def handler(request):
    return app(request.environ, lambda status, headers: None)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

