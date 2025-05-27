import os
import sys
import sqlite3
from datetime import datetime

# Adicionar o diretório atual ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Função simples para gerar hash de senha
def generate_password_hash(password):
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

def main():
    # Definir o caminho do banco de dados
    db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance')
    os.makedirs(db_dir, exist_ok=True)
    db_path = os.path.join(db_dir, 'tribo_cerrado.db')
    
    print(f"Diretório do banco de dados: {db_dir}")
    print(f"Caminho do banco de dados: {db_path}")
    
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Criar tabelas se não existirem
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT,
        nickname TEXT,
        profile_image TEXT,
        bio TEXT,
        birth_date DATE,
        collection_date DATE,
        blood_type TEXT,
        address_street TEXT,
        address_number TEXT,
        address_complement TEXT,
        address_district TEXT,
        address_city TEXT,
        address_state TEXT,
        address_zipcode TEXT,
        health_notes TEXT,
        health_insurance TEXT,
        health_insurance_number TEXT,
        godfather_id INTEGER,
        is_admin BOOLEAN DEFAULT 0,
        is_approved BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        FOREIGN KEY (godfather_id) REFERENCES users (id)
    )
    ''')
    
    # Criar outras tabelas necessárias
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS family_members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        relationship_type TEXT NOT NULL,
        birth_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emergency_contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        relationship TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS motorcycles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        manufacturing_year INTEGER,
        model_year INTEGER,
        chassis_number TEXT,
        engine_number TEXT,
        license_plate TEXT,
        ipva_due_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS motorcycle_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        motorcycle_id INTEGER NOT NULL,
        image_url TEXT NOT NULL,
        caption TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (motorcycle_id) REFERENCES motorcycles (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS gallery_images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        image_url TEXT NOT NULL,
        caption TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    print("Tabelas verificadas/criadas")
    
    # Adicionar colunas extras se necessário
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN nickname TEXT")
        print("Coluna nickname adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna nickname: coluna já existe")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN birth_date DATE")
        print("Coluna birth_date adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna birth_date: coluna já existe")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN collection_date DATE")
        print("Coluna collection_date adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna collection_date: coluna já existe")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN blood_type TEXT")
        print("Coluna blood_type adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna blood_type: coluna já existe")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN address_street TEXT")
        print("Coluna address_street adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna address_street: coluna já existe")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN address_number TEXT")
        print("Coluna address_number adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna address_number: coluna já existe")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN address_complement TEXT")
        print("Coluna address_complement adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna address_complement: coluna já existe")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN address_district TEXT")
        print("Coluna address_district adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna address_district: coluna já existe")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN address_city TEXT")
        print("Coluna address_city adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna address_city: coluna já existe")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN address_state TEXT")
        print("Coluna address_state adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna address_state: coluna já existe")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN address_zipcode TEXT")
        print("Coluna address_zipcode adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna address_zipcode: coluna já existe")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN health_notes TEXT")
        print("Coluna health_notes adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna health_notes: coluna já existe")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN health_insurance TEXT")
        print("Coluna health_insurance adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna health_insurance: coluna já existe")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN health_insurance_number TEXT")
        print("Coluna health_insurance_number adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna health_insurance_number: coluna já existe")
    
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN godfather_id INTEGER REFERENCES users(id)")
        print("Coluna godfather_id adicionada")
    except sqlite3.OperationalError:
        print("Erro ao adicionar coluna godfather_id: coluna já existe")
    
    # Criar usuário administrador padrão se não existir
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
    admin_exists = cursor.fetchone()[0]
    
    if admin_exists == 0:
        print("Criando usuário administrador padrão")
        hashed_password = generate_password_hash('admin123')
        cursor.execute('''
        INSERT INTO users (username, email, password, full_name, is_admin, is_approved)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', ('admin', 'admin@tribodocerrado.com', hashed_password, 'Administrador', 1, 1))
        print("Usuário administrador criado: admin")
    
    # Salvar alterações
    conn.commit()
    conn.close()
    
    print("Migração do banco de dados concluída com sucesso!")

if __name__ == "__main__":
    main()

