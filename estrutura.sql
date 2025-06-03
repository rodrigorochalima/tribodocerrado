CREATE TABLE IF NOT EXISTS membros (
    id SERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    email TEXT,
    telefone TEXT
);