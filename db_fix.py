import os
import sys
import psycopg2
from psycopg2 import sql
from urllib.parse import urlparse

# Função para obter a conexão com o banco de dados
def get_db_connection():
    # Verificar se estamos no ambiente Render
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # Estamos no Render, usar DATABASE_URL
        print("Usando DATABASE_URL do ambiente Render")
        result = urlparse(database_url)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        port = result.port
        
        return psycopg2.connect(
            database=database,
            user=username,
            password=password,
            host=hostname,
            port=port
        )
    else:
        # Estamos em ambiente local, usar variáveis de ambiente específicas
        print("Usando variáveis de ambiente locais para conexão")
        db_host = os.environ.get('DB_HOST', 'localhost')
        db_port = os.environ.get('DB_PORT', '5432')
        db_name = os.environ.get('DB_NAME', 'tribodocerrado')
        db_user = os.environ.get('DB_USER', 'postgres')
        db_pass = os.environ.get('DB_PASS', 'postgres')
        
        return psycopg2.connect(
            host=db_host,
            port=db_port,
            dbname=db_name,
            user=db_user,
            password=db_pass
        )

# Função para verificar se uma coluna existe
def column_exists(cursor, table, column):
    cursor.execute("""
        SELECT 1 FROM information_schema.columns 
        WHERE table_name = %s AND column_name = %s
    """, (table, column))
    return cursor.fetchone() is not None

# Função para adicionar uma coluna se não existir
def add_column_if_not_exists(cursor, table, column, data_type, default=None):
    if not column_exists(cursor, table, column):
        query = sql.SQL("ALTER TABLE {} ADD COLUMN {} {}").format(
            sql.Identifier(table),
            sql.Identifier(column),
            sql.SQL(data_type)
        )
        
        if default is not None:
            query = sql.SQL("{} DEFAULT {}").format(query, sql.SQL(default))
        
        try:
            cursor.execute(query)
            print(f"Coluna {column} adicionada à tabela {table}")
            return True
        except Exception as e:
            print(f"Erro ao adicionar coluna {column}: {e}")
            return False
    else:
        print(f"Coluna {column} já existe na tabela {table}")
        return False

# Função principal para corrigir o banco de dados
def fix_database():
    print("Iniciando correção do banco de dados...")
    
    try:
        conn = get_db_connection()
        conn.autocommit = True  # Importante para evitar problemas de transação
        cursor = conn.cursor()
        
        # Verificar se a tabela users existe
        cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'users'")
        if cursor.fetchone() is None:
            print("Tabela users não existe! Criando tabela...")
            # Criar tabela users se não existir
            cursor.execute("""
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(120),
                    nickname VARCHAR(80),
                    birth_date DATE,
                    blood_type VARCHAR(10),
                    profile_image VARCHAR(255),
                    address_street VARCHAR(255),
                    address_number VARCHAR(20),
                    address_complement VARCHAR(255),
                    address_district VARCHAR(255),
                    address_city VARCHAR(255),
                    address_state VARCHAR(2),
                    address_zipcode VARCHAR(20),
                    health_notes TEXT,
                    health_insurance VARCHAR(255),
                    health_insurance_number VARCHAR(255),
                    collection_date DATE,
                    join_date DATE,
                    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
                    last_login TIMESTAMP WITHOUT TIME ZONE,
                    is_admin BOOLEAN DEFAULT FALSE,
                    is_active BOOLEAN DEFAULT TRUE,
                    is_public_profile BOOLEAN DEFAULT FALSE,
                    is_public_full_name BOOLEAN DEFAULT FALSE,
                    is_public_birth_date BOOLEAN DEFAULT FALSE,
                    is_public_blood_type BOOLEAN DEFAULT FALSE,
                    is_public_address BOOLEAN DEFAULT FALSE,
                    is_public_health_info BOOLEAN DEFAULT FALSE,
                    is_public_collection_date BOOLEAN DEFAULT FALSE,
                    is_public_join_date BOOLEAN DEFAULT TRUE
                )
            """)
            print("Tabela users criada com sucesso!")
        
        # Adicionar colunas ausentes à tabela users
        add_column_if_not_exists(cursor, 'users', 'updated_at', 'TIMESTAMP WITHOUT TIME ZONE', 'NOW()')
        
        # Atualizar updated_at para usar created_at se estiver NULL
        cursor.execute("""
            UPDATE users SET updated_at = created_at WHERE updated_at IS NULL
        """)
        
        # Adicionar outras colunas que podem estar faltando
        add_column_if_not_exists(cursor, 'users', 'last_login', 'TIMESTAMP WITHOUT TIME ZONE')
        add_column_if_not_exists(cursor, 'users', 'is_admin', 'BOOLEAN', 'FALSE')
        add_column_if_not_exists(cursor, 'users', 'is_active', 'BOOLEAN', 'TRUE')
        
        # Adicionar colunas de privacidade
        add_column_if_not_exists(cursor, 'users', 'is_public_profile', 'BOOLEAN', 'FALSE')
        add_column_if_not_exists(cursor, 'users', 'is_public_full_name', 'BOOLEAN', 'FALSE')
        add_column_if_not_exists(cursor, 'users', 'is_public_birth_date', 'BOOLEAN', 'FALSE')
        add_column_if_not_exists(cursor, 'users', 'is_public_blood_type', 'BOOLEAN', 'FALSE')
        add_column_if_not_exists(cursor, 'users', 'is_public_address', 'BOOLEAN', 'FALSE')
        add_column_if_not_exists(cursor, 'users', 'is_public_health_info', 'BOOLEAN', 'FALSE')
        add_column_if_not_exists(cursor, 'users', 'is_public_collection_date', 'BOOLEAN', 'FALSE')
        add_column_if_not_exists(cursor, 'users', 'is_public_join_date', 'BOOLEAN', 'TRUE')
        
        # Verificar se existe pelo menos um usuário admin
        cursor.execute("SELECT 1 FROM users WHERE is_admin = TRUE LIMIT 1")
        if cursor.fetchone() is None:
            print("Nenhum usuário admin encontrado. Criando usuário admin padrão...")
            # Criar usuário admin padrão se não existir nenhum
            from werkzeug.security import generate_password_hash
            admin_password = generate_password_hash('admin123')
            
            cursor.execute("""
                INSERT INTO users (username, email, password, full_name, is_admin, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                ON CONFLICT (username) DO NOTHING
            """, ('admin', 'admin@tribodocerrado.com.br', admin_password, 'Administrador', True))
            
            print("Usuário admin criado com sucesso!")
        
        # Verificar se a tabela motorcycles existe
        cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'motorcycles'")
        if cursor.fetchone() is None:
            print("Tabela motorcycles não existe! Criando tabela...")
            # Criar tabela motorcycles se não existir
            cursor.execute("""
                CREATE TABLE motorcycles (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    brand VARCHAR(100) NOT NULL,
                    model VARCHAR(100) NOT NULL,
                    manufacturing_year INTEGER NOT NULL,
                    model_year INTEGER NOT NULL,
                    color VARCHAR(50),
                    license_plate VARCHAR(20),
                    engine_capacity VARCHAR(20),
                    purchase_date DATE,
                    ipva_due_date DATE,
                    insurance_due_date DATE,
                    insurance_company VARCHAR(100),
                    last_maintenance DATE,
                    next_maintenance DATE,
                    maintenance_notes TEXT,
                    image_url VARCHAR(255),
                    notes TEXT,
                    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
                )
            """)
            print("Tabela motorcycles criada com sucesso!")
        
        # Adicionar colunas ausentes à tabela motorcycles
        add_column_if_not_exists(cursor, 'motorcycles', 'updated_at', 'TIMESTAMP WITHOUT TIME ZONE', 'NOW()')
        
        # Atualizar updated_at para usar created_at se estiver NULL
        cursor.execute("""
            UPDATE motorcycles SET updated_at = created_at WHERE updated_at IS NULL
        """)
        
        # Verificar se a tabela motorcycle_images existe
        cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'motorcycle_images'")
        if cursor.fetchone() is None:
            print("Tabela motorcycle_images não existe! Criando tabela...")
            # Criar tabela motorcycle_images se não existir
            cursor.execute("""
                CREATE TABLE motorcycle_images (
                    id SERIAL PRIMARY KEY,
                    motorcycle_id INTEGER NOT NULL REFERENCES motorcycles(id),
                    image_url VARCHAR(255) NOT NULL,
                    caption VARCHAR(255),
                    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
                )
            """)
            print("Tabela motorcycle_images criada com sucesso!")
        
        # Adicionar colunas ausentes à tabela motorcycle_images
        add_column_if_not_exists(cursor, 'motorcycle_images', 'updated_at', 'TIMESTAMP WITHOUT TIME ZONE', 'NOW()')
        
        # Atualizar updated_at para usar created_at se estiver NULL
        cursor.execute("""
            UPDATE motorcycle_images SET updated_at = created_at WHERE updated_at IS NULL
        """)
        
        # Verificar se a tabela emergency_contacts existe
        cursor.execute("SELECT 1 FROM information_schema.tables WHERE table_name = 'emergency_contacts'")
        if cursor.fetchone() is None:
            print("Tabela emergency_contacts não existe! Criando tabela...")
            # Criar tabela emergency_contacts se não existir
            cursor.execute("""
                CREATE TABLE emergency_contacts (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL REFERENCES users(id),
                    name VARCHAR(120) NOT NULL,
                    relationship VARCHAR(50),
                    phone VARCHAR(20) NOT NULL,
                    email VARCHAR(120),
                    address VARCHAR(255),
                    notes TEXT,
                    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
                    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
                )
            """)
            print("Tabela emergency_contacts criada com sucesso!")
        
        # Adicionar colunas ausentes à tabela emergency_contacts
        add_column_if_not_exists(cursor, 'emergency_contacts', 'updated_at', 'TIMESTAMP WITHOUT TIME ZONE', 'NOW()')
        
        # Atualizar updated_at para usar created_at se estiver NULL
        cursor.execute("""
            UPDATE emergency_contacts SET updated_at = created_at WHERE updated_at IS NULL
        """)
        
        print("Correção do banco de dados concluída com sucesso!")
        
    except Exception as e:
        print(f"Erro ao corrigir o banco de dados: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    fix_database()
