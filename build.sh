#!/bin/bash

# Script de build para Tribo do Cerrado
set -e

echo "🏗️ Iniciando build do Tribo do Cerrado..."

# Verificar se estamos no diretório correto
if [ ! -f "composer.json" ]; then
    echo "❌ Erro: composer.json não encontrado. Execute este script no diretório raiz do projeto."
    exit 1
fi

# Instalar dependências PHP
echo "📦 Instalando dependências PHP..."
if command -v composer &> /dev/null; then
    composer install --no-dev --optimize-autoloader --no-interaction
else
    echo "⚠️ Composer não encontrado, pulando instalação de dependências PHP"
fi

# Instalar dependências Node.js se package.json existir
if [ -f "package.json" ]; then
    echo "📦 Instalando dependências Node.js..."
    if command -v npm &> /dev/null; then
        npm ci --production
        npm run build 2>/dev/null || echo "⚠️ Script de build não encontrado, continuando..."
    else
        echo "⚠️ npm não encontrado, pulando instalação de dependências Node.js"
    fi
fi

# Criar diretórios necessários
echo "📁 Criando diretórios necessários..."
mkdir -p protected/runtime/{logs,cache,mail}
mkdir -p uploads/{file,profile_image}
mkdir -p assets

# Configurar permissões
echo "🔐 Configurando permissões..."
chmod -R 755 .
chmod -R 777 protected/runtime uploads assets 2>/dev/null || true

# Gerar informações de build
echo "📋 Gerando informações de build..."
cat > build-info.json << EOF
{
    "build_time": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "git_commit": "$(git rev-parse HEAD 2>/dev/null || echo 'unknown')",
    "version": "1.0.0",
    "environment": "${ENVIRONMENT:-production}"
}
EOF

echo "✅ Build concluído com sucesso!"
echo "📊 Informações do build salvas em build-info.json"

