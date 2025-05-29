#!/bin/bash

# Script de inicialização para o site Tribo do Cerrado
# Este script executa comandos SQL diretos para garantir que o banco de dados esteja corretamente configurado
# antes de iniciar a aplicação Flask

echo "Iniciando script de inicialização..."

# Verificar se a variável de ambiente DATABASE_URL está definida
if [ -z "$DATABASE_URL" ]; then
    echo "ERRO: Variável de ambiente DATABASE_URL não está definida!"
    exit 1
fi

# Extrair informações de conexão do DATABASE_URL
DB_URL=$(echo $DATABASE_URL | sed 's/postgresql:\/\///')
DB_USER=$(echo $DB_URL | cut -d':' -f1)
DB_PASS=$(echo $DB_URL | cut -d':' -f2 | cut -d'@' -f1)
DB_HOST=$(echo $DB_URL | cut -d'@' -f2 | cut -d':' -f1)
DB_PORT=$(echo $DB_URL | cut -d':' -f3 | cut -d'/' -f1)
DB_NAME=$(echo $DB_URL | cut -d'/' -f2 | cut -d'?' -f1)

echo "Conectando ao banco de dados PostgreSQL..."
echo "Host: $DB_HOST, Porta: $DB_PORT, Banco: $DB_NAME"

# Criar arquivo temporário com comandos SQL
cat > /tmp/fix_schema.sql << EOF
-- Verificar e adicionar coluna updated_at se não existir
DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'updated_at'
    ) THEN
        ALTER TABLE users ADD COLUMN updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW();
        UPDATE users SET updated_at = created_at WHERE updated_at IS NULL;
        RAISE NOTICE 'Coluna updated_at adicionada à tabela users';
    ELSE
        RAISE NOTICE 'Coluna updated_at já existe na tabela users';
    END IF;
END \$\$;

-- Verificar e adicionar coluna last_login se não existir
DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'last_login'
    ) THEN
        ALTER TABLE users ADD COLUMN last_login TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL;
        RAISE NOTICE 'Coluna last_login adicionada à tabela users';
    ELSE
        RAISE NOTICE 'Coluna last_login já existe na tabela users';
    END IF;
END \$\$;

-- Verificar e adicionar colunas de privacidade se não existirem
DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'is_public_profile'
    ) THEN
        ALTER TABLE users ADD COLUMN is_public_profile BOOLEAN DEFAULT FALSE;
        RAISE NOTICE 'Coluna is_public_profile adicionada à tabela users';
    ELSE
        RAISE NOTICE 'Coluna is_public_profile já existe na tabela users';
    END IF;
END \$\$;

DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'is_public_full_name'
    ) THEN
        ALTER TABLE users ADD COLUMN is_public_full_name BOOLEAN DEFAULT FALSE;
        RAISE NOTICE 'Coluna is_public_full_name adicionada à tabela users';
    ELSE
        RAISE NOTICE 'Coluna is_public_full_name já existe na tabela users';
    END IF;
END \$\$;

DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'is_public_birth_date'
    ) THEN
        ALTER TABLE users ADD COLUMN is_public_birth_date BOOLEAN DEFAULT FALSE;
        RAISE NOTICE 'Coluna is_public_birth_date adicionada à tabela users';
    ELSE
        RAISE NOTICE 'Coluna is_public_birth_date já existe na tabela users';
    END IF;
END \$\$;

DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'is_public_blood_type'
    ) THEN
        ALTER TABLE users ADD COLUMN is_public_blood_type BOOLEAN DEFAULT FALSE;
        RAISE NOTICE 'Coluna is_public_blood_type adicionada à tabela users';
    ELSE
        RAISE NOTICE 'Coluna is_public_blood_type já existe na tabela users';
    END IF;
END \$\$;

DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'is_public_address'
    ) THEN
        ALTER TABLE users ADD COLUMN is_public_address BOOLEAN DEFAULT FALSE;
        RAISE NOTICE 'Coluna is_public_address adicionada à tabela users';
    ELSE
        RAISE NOTICE 'Coluna is_public_address já existe na tabela users';
    END IF;
END \$\$;

DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'is_public_health_info'
    ) THEN
        ALTER TABLE users ADD COLUMN is_public_health_info BOOLEAN DEFAULT FALSE;
        RAISE NOTICE 'Coluna is_public_health_info adicionada à tabela users';
    ELSE
        RAISE NOTICE 'Coluna is_public_health_info já existe na tabela users';
    END IF;
END \$\$;

DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'is_public_collection_date'
    ) THEN
        ALTER TABLE users ADD COLUMN is_public_collection_date BOOLEAN DEFAULT FALSE;
        RAISE NOTICE 'Coluna is_public_collection_date adicionada à tabela users';
    ELSE
        RAISE NOTICE 'Coluna is_public_collection_date já existe na tabela users';
    END IF;
END \$\$;

DO \$\$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = 'users' AND column_name = 'is_public_join_date'
    ) THEN
        ALTER TABLE users ADD COLUMN is_public_join_date BOOLEAN DEFAULT TRUE;
        RAISE NOTICE 'Coluna is_public_join_date adicionada à tabela users';
    ELSE
        RAISE NOTICE 'Coluna is_public_join_date já existe na tabela users';
    END IF;
END \$\$;
EOF

# Executar os comandos SQL usando PSQL
export PGPASSWORD=$DB_PASS
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f /tmp/fix_schema.sql

# Remover arquivo temporário
rm /tmp/fix_schema.sql

echo "Correção do schema concluída!"

# Iniciar o servidor Gunicorn
echo "Iniciando o servidor Gunicorn..."
cd /opt/render/project/src && gunicorn -w 1 -b 0.0.0.0:$PORT "src.main:app"
