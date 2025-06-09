#!/bin/bash
set -e

echo "🏍️ Iniciando Tribo do Cerrado..."

# Aguardar PostgreSQL
if [ ! -z "$DATABASE_URL" ]; then
    echo "Aguardando PostgreSQL..."
    timeout=30
    while [ $timeout -gt 0 ]; do
        if php -r "try { new PDO('$DATABASE_URL'); echo 'OK'; } catch(Exception \$e) { echo 'WAIT'; }" | grep -q "OK"; then
            echo "✅ PostgreSQL conectado!"
            break
        fi
        sleep 1
        timeout=$((timeout-1))
    done
fi

# Criar diretórios e configurar permissões
mkdir -p protected/runtime/{logs,cache} uploads/{file,profile_image} assets
chown -R www-data:www-data /var/www/html
chmod -R 777 protected/runtime uploads assets

echo "🚀 Iniciando Apache..."
exec apache2-foreground

