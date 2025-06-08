#!/bin/bash

# Script de build para Tribo do Cerrado
echo "🏗️  Iniciando build do Tribo do Cerrado..."

# Verificar se estamos no diretório correto
if [ ! -f "composer.json" ]; then
    echo "❌ Erro: composer.json não encontrado. Execute este script no diretório raiz do projeto."
    exit 1
fi

# Instalar dependências PHP
echo "📦 Instalando dependências PHP..."
if [ "$NODE_ENV" = "production" ]; then
    composer install --no-dev --optimize-autoloader --no-interaction
else
    composer install
fi

# Verificar se o Composer foi executado com sucesso
if [ $? -ne 0 ]; then
    echo "❌ Erro ao instalar dependências PHP"
    exit 1
fi

# Instalar dependências Node.js (se necessário)
if [ -f "package.json" ]; then
    echo "📦 Instalando dependências Node.js..."
    npm install
    
    if [ $? -ne 0 ]; then
        echo "❌ Erro ao instalar dependências Node.js"
        exit 1
    fi
    
    # Build dos assets
    echo "🎨 Compilando assets..."
    npm run build
fi

# Criar diretórios necessários
echo "📁 Criando diretórios necessários..."
mkdir -p protected/runtime/logs
mkdir -p protected/runtime/cache
mkdir -p protected/runtime/mail
mkdir -p uploads/file
mkdir -p uploads/profile_image
mkdir -p assets

# Configurar permissões
echo "🔐 Configurando permissões..."
chmod -R 755 .
chmod -R 777 protected/runtime
chmod -R 777 uploads
chmod -R 777 assets

# Criar arquivos .gitkeep para diretórios vazios
touch uploads/.gitkeep
touch uploads/file/.gitkeep
touch uploads/profile_image/.gitkeep
touch assets/.gitkeep
touch protected/runtime/logs/.gitkeep
touch protected/runtime/cache/.gitkeep

# Verificar configuração
echo "⚙️  Verificando configuração..."

# Verificar se o arquivo de configuração existe
if [ ! -f "protected/config/common.php" ]; then
    echo "❌ Erro: Arquivo de configuração não encontrado"
    exit 1
fi

# Verificar sintaxe PHP
echo "🐘 Verificando sintaxe PHP..."
find . -name "*.php" -not -path "./vendor/*" -exec php -l {} \; | grep -v "No syntax errors"

if [ ${PIPESTATUS[0]} -ne 0 ]; then
    echo "❌ Erro de sintaxe encontrado em arquivos PHP"
    exit 1
fi

# Verificar se as extensões PHP necessárias estão instaladas
echo "🔍 Verificando extensões PHP..."
php -m | grep -E "(pdo|pgsql|mbstring|xml|zip|bcmath|intl|gd|curl)" > /dev/null

if [ $? -ne 0 ]; then
    echo "⚠️  Algumas extensões PHP podem estar faltando"
fi

# Otimizar autoloader
echo "⚡ Otimizando autoloader..."
composer dump-autoload --optimize

# Limpar cache se existir
if [ -d "protected/runtime/cache" ]; then
    echo "🧹 Limpando cache..."
    rm -rf protected/runtime/cache/*
fi

# Gerar informações de build
echo "📋 Gerando informações de build..."
cat > build-info.json << EOF
{
    "build_time": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "build_number": "${BUILD_NUMBER:-local}",
    "git_commit": "$(git rev-parse HEAD 2>/dev/null || echo 'unknown')",
    "git_branch": "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo 'unknown')",
    "php_version": "$(php -r 'echo PHP_VERSION;')",
    "environment": "${NODE_ENV:-development}",
    "project": "Tribo do Cerrado",
    "version": "1.0.0"
}
EOF

# Verificar saúde básica da aplicação
echo "🏥 Verificando saúde da aplicação..."
php -r "
try {
    require_once 'protected/config/common.php';
    echo 'Configuração carregada com sucesso\n';
} catch (Exception \$e) {
    echo 'Erro ao carregar configuração: ' . \$e->getMessage() . '\n';
    exit(1);
}
"

if [ $? -ne 0 ]; then
    echo "❌ Erro na verificação de saúde"
    exit 1
fi

# Estatísticas do build
echo ""
echo "📊 Estatísticas do build:"
echo "   Arquivos PHP: $(find . -name "*.php" -not -path "./vendor/*" | wc -l)"
echo "   Tamanho vendor: $(du -sh vendor 2>/dev/null | cut -f1 || echo 'N/A')"
echo "   Tamanho total: $(du -sh . | cut -f1)"
echo ""

echo "✅ Build concluído com sucesso!"
echo "🏍️  Tribo do Cerrado está pronto para deploy!"

# Instruções finais
echo ""
echo "📝 Próximos passos:"
echo "   1. Configurar variáveis de ambiente no Render.com"
echo "   2. Fazer push para o repositório GitHub"
echo "   3. Conectar repositório ao Render.com"
echo "   4. Aguardar deploy automático"
echo ""
echo "🌐 Variáveis de ambiente necessárias:"
echo "   - DATABASE_URL"
echo "   - COOKIE_VALIDATION_KEY"
echo "   - ADMIN_EMAIL"
echo "   - ADMIN_PASSWORD"
echo "   - MAILER_USERNAME"
echo "   - MAILER_PASSWORD"
echo ""

