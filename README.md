# Tribo do Cerrado - Backend

Este é o backend básico para cadastro de membros do motoclube Tribo do Cerrado, usando Node.js, Express e PostgreSQL.

## Rotas

- `GET /` — Testa se a API está online
- `POST /membros` — Adiciona membro (campos: nome, email, telefone)
- `GET /membros` — Lista todos os membros cadastrados

## Como rodar localmente

1. Copie `.env.example` para `.env` e preencha com suas credenciais do banco
2. Instale os pacotes:

```bash
npm install
```

3. Rode a aplicação:

```bash
npm start
```