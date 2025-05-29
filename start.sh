#!/bin/bash

# Configurações do banco de dados
export DB_HOST=${DB_HOST:-$PGHOST}
export DB_PORT=${DB_PORT:-$PGPORT}
export DB_NAME=${DB_NAME:-$PGDATABASE}
export DB_USER=${DB_USER:-$PGUSER}
export DB_PASS=${DB_PASS:-$PGPASSWORD}

echo "Iniciando script de inicialização..."

# Verificar se o ambiente virtual existe e criar se não existir
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Criar diretórios necessários para uploads e imagens
echo "Criando diretórios para uploads e imagens..."
mkdir -p src/static/images/profiles
mkdir -p src/static/uploads/profile
mkdir -p src/static/uploads/family
mkdir -p src/static/uploads/gallery
mkdir -p src/static/uploads/motorcycles

# Ajustar permissões dos diretórios
echo "Ajustando permissões dos diretórios..."
chmod -R 777 src/static/images
chmod -R 777 src/static/uploads

# Executar script de correção do banco de dados
echo "Executando script de correção do banco de dados..."
python db_fix.py

# Iniciar o servidor Gunicorn
echo "Iniciando o servidor Gunicorn..."
cd /opt/render/project/src && gunicorn -w 1 -b 0.0.0.0:$PORT "src.main:app"
