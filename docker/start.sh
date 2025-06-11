#!/bin/bash
set -e

echo "🏍️ Iniciando Tribo do Cerrado..."

# Aguardar PostgreSQL se configurado
if [ ! -z "$DATABASE_URL" ]; then
    echo "Aguardando PostgreSQL..."
    for i in {1..30}; do
        if php -r "try { new PDO('$DATABASE_URL'); echo 'OK'; exit(0); } catch(Exception \$e) { exit(1); }" 2>/dev/null; then
            echo "✅ PostgreSQL conectado!"
            break
        fi
        echo "Tentativa $i/30..."
        sleep 2
    done
fi

# Configurar permissões
chown -R www-data:www-data /var/www/html
chmod -R 777 protected/runtime uploads assets 2>/dev/null || true

# Garantir que Apache escute na porta correta
echo "Listen 80" > /etc/apache2/ports.conf
echo "ServerName tribodocerrado.onrender.com" >> /etc/apache2/apache2.conf

echo "🚀 Iniciando Apache na porta 80..."
exec apache2-foreground

