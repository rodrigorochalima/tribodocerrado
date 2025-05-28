#!/bin/bash

# Script de inicialização para o Render
# Este script é executado pelo Render durante o processo de deploy

echo "Iniciando script de inicialização para o Render..."

# Garantir que o diretório de uploads existe
mkdir -p static/uploads/gallery
mkdir -p static/uploads/motorcycles
mkdir -p static/uploads/family
mkdir -p static/uploads/profile

echo "Diretórios de upload criados"

# Executar migração do banco de dados
echo "Executando migração do banco de dados..."
python src/db_migration.py

# Iniciar o servidor Gunicorn
echo "Iniciando o servidor Gunicorn..."
gunicorn "src.main:create_app()" --bind 0.0.0.0:$PORT --log-level info

# Criar diretórios para uploads
mkdir -p static/img
mkdir -p static/uploads/profile
mkdir -p static/uploads/gallery
mkdir -p static/uploads/motorcycles
mkdir -p static/uploads/family
chmod -R 777 static

# Criar diretórios necessários para uploads
mkdir -p static/images/profiles
mkdir -p static/uploads/profile
mkdir -p static/uploads/family
mkdir -p static/uploads/gallery
mkdir -p static/uploads/motorcycles
chmod -R 777 static/images
chmod -R 777 static/uploads

