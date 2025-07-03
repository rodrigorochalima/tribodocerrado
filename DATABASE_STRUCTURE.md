# 🗄️ ESTRUTURA DO BANCO DE DADOS - TRIBO DO CERRADO

## 📋 TABELA: usuarios

### Campos:
- **id** (INTEGER PRIMARY KEY) - ID único do usuário
- **nome** (VARCHAR(100)) - Nome completo
- **apelido** (VARCHAR(50)) - Apelido/Alcunha
- **email** (VARCHAR(100) UNIQUE) - Email único
- **senha** (VARCHAR(255)) - Senha criptografada
- **telefone** (VARCHAR(20)) - Telefone de contato
- **cidade** (VARCHAR(50)) - Cidade
- **estado** (VARCHAR(2)) - Estado (sigla)
- **moto** (VARCHAR(100)) - Motocicleta (marca/modelo/ano)
- **experiencia** (VARCHAR(20)) - Nível de experiência
- **motivacao** (TEXT) - Motivação para participar
- **newsletter** (BOOLEAN) - Aceita receber newsletter
- **ativo** (BOOLEAN) - Usuário ativo
- **data_cadastro** (DATETIME) - Data do cadastro
- **ultimo_login** (DATETIME) - Último login

### SQL de Criação:
```sql
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL,
    apelido VARCHAR(50),
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    telefone VARCHAR(20) NOT NULL,
    cidade VARCHAR(50) NOT NULL,
    estado VARCHAR(2) NOT NULL,
    moto VARCHAR(100) NOT NULL,
    experiencia VARCHAR(20) NOT NULL,
    motivacao TEXT,
    newsletter BOOLEAN DEFAULT FALSE,
    ativo BOOLEAN DEFAULT TRUE,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP,
    ultimo_login DATETIME
);
```

## 📋 TABELA: eventos

### Campos:
- **id** (INTEGER PRIMARY KEY) - ID único do evento
- **titulo** (VARCHAR(100)) - Título do evento
- **descricao** (TEXT) - Descrição detalhada
- **data_inicio** (DATETIME) - Data/hora de início
- **data_fim** (DATETIME) - Data/hora de fim
- **local** (VARCHAR(100)) - Local do evento
- **endereco** (TEXT) - Endereço completo
- **vagas** (INTEGER) - Número de vagas
- **valor** (DECIMAL(10,2)) - Valor da inscrição
- **ativo** (BOOLEAN) - Evento ativo
- **data_criacao** (DATETIME) - Data de criação

### SQL de Criação:
```sql
CREATE TABLE eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT,
    data_inicio DATETIME NOT NULL,
    data_fim DATETIME,
    local VARCHAR(100) NOT NULL,
    endereco TEXT,
    vagas INTEGER DEFAULT 0,
    valor DECIMAL(10,2) DEFAULT 0.00,
    ativo BOOLEAN DEFAULT TRUE,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 📋 TABELA: inscricoes

### Campos:
- **id** (INTEGER PRIMARY KEY) - ID único da inscrição
- **usuario_id** (INTEGER) - ID do usuário
- **evento_id** (INTEGER) - ID do evento
- **status** (VARCHAR(20)) - Status da inscrição
- **data_inscricao** (DATETIME) - Data da inscrição
- **observacoes** (TEXT) - Observações

### SQL de Criação:
```sql
CREATE TABLE inscricoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    evento_id INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'pendente',
    data_inscricao DATETIME DEFAULT CURRENT_TIMESTAMP,
    observacoes TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY (evento_id) REFERENCES eventos(id),
    UNIQUE(usuario_id, evento_id)
);
```

## 🔧 DADOS INICIAIS

### Usuário Administrador:
```sql
INSERT INTO usuarios (nome, email, senha, telefone, cidade, estado, moto, experiencia, ativo) 
VALUES ('Administrador', 'admin@tribodocerrado.org', '123456', '(62) 99999-9999', 'Goiânia', 'GO', 'Honda CB 600F 2020', 'expert', TRUE);
```

### Eventos de Exemplo:
```sql
INSERT INTO eventos (titulo, descricao, data_inicio, local, vagas) VALUES
('Encontro Mensal - Janeiro', 'Encontro mensal dos membros para confraternização', '2025-01-06 14:00:00', 'Praça Central - Goiânia', 50),
('Viagem ao Jalapão', 'Aventura de 3 dias pelas trilhas do Jalapão', '2025-03-15 06:00:00', 'Jalapão - TO', 20),
('Moto Fest Goiânia', 'Participação no maior evento motociclístico de Goiás', '2025-04-22 08:00:00', 'Centro de Convenções - Goiânia', 100);
```

## 🔐 CONFIGURAÇÃO DE SEGURANÇA

### Criptografia de Senhas:
- Usar bcrypt ou similar para hash das senhas
- Nunca armazenar senhas em texto plano
- Salt único para cada senha

### Validações:
- Email único obrigatório
- Senha mínima de 6 caracteres
- Telefone obrigatório
- Campos obrigatórios validados

## 📊 RELATÓRIOS ÚTEIS

### Usuários Ativos:
```sql
SELECT COUNT(*) as total_usuarios FROM usuarios WHERE ativo = TRUE;
```

### Eventos Próximos:
```sql
SELECT * FROM eventos WHERE data_inicio > datetime('now') AND ativo = TRUE ORDER BY data_inicio;
```

### Inscrições por Evento:
```sql
SELECT e.titulo, COUNT(i.id) as total_inscricoes 
FROM eventos e 
LEFT JOIN inscricoes i ON e.id = i.evento_id 
GROUP BY e.id, e.titulo;
```

---

**Nota:** Esta estrutura está preparada para expansão futura com novas funcionalidades como:
- Sistema de mensagens
- Galeria de fotos
- Histórico de viagens
- Sistema de pontuação
- Integração com redes sociais

