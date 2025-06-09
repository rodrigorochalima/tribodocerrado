#!/bin/bash

# Script de inicialização para Tribo do Cerrado
echo "🏍️ Iniciando Tribo do Cerrado..."

# Aguardar banco de dados
echo "Aguardando PostgreSQL..."
while ! pg_isready -h ${DATABASE_HOST:-localhost} -p ${DATABASE_PORT:-5432} -q 2>/dev/null; do
    echo "Aguardando conexão com PostgreSQL..."
    sleep 2
done
echo "✅ PostgreSQL conectado!"

# Criar diretórios necessários
mkdir -p protected/runtime/{logs,cache,mail}
mkdir -p uploads/{file,profile_image}
mkdir -p assets

# Configurar permissões
chown -R www-data:www-data /var/www/html
chmod -R 755 /var/www/html
chmod -R 777 uploads protected/runtime assets

# Executar migrações se solicitado
if [ "$RUN_MIGRATIONS" = "true" ]; then
    echo "Executando migrações do banco de dados..."
    php protected/yii migrate --interactive=0 || echo "⚠️ Erro nas migrações, continuando..."
fi

# Criar usuário administrador se solicitado
if [ "$CREATE_ADMIN" = "true" ] && [ ! -z "$ADMIN_EMAIL" ]; then
    echo "Criando usuário administrador..."
    php protected/yii user/create-admin \
        --email="$ADMIN_EMAIL" \
        --password="$ADMIN_PASSWORD" \
        --interactive=0 || echo "⚠️ Usuário admin já existe ou erro na criação"
fi

# Limpar cache se solicitado
if [ "$ENABLE_CACHE" = "true" ]; then
    echo "Limpando cache..."
    rm -rf protected/runtime/cache/* || true
fi

echo "🚀 Iniciando Apache..."
exec apache2-foreground

