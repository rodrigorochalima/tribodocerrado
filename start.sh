#!/bin/bash

# Script de inicialização para o Render
echo "Iniciando script de inicialização para o Render..."

# Garantir que o diretório de uploads existe
mkdir -p static/uploads/gallery
mkdir -p static/uploads/motorcycles
mkdir -p static/uploads/family
mkdir -p static/uploads/profile

echo "Diretórios de upload criados"

# Executar migração do banco de dados
echo "Executando migração do banco de dados..."
python -c "import os, sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')); from src.db_migration import main; main()"

# Iniciar o servidor Gunicorn
echo "Iniciando o servidor Gunicorn..."
gunicorn wsgi:application --bind 0.0.0.0:$PORT --log-level info
