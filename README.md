
# Tribo do Cerrado - Site Oficial

Este projeto é um site desenvolvido com Flask, preparado para deploy automático via Render.com com GitHub.

---

## ✅ Requisitos

- Conta no GitHub
- Conta no [Render.com](https://render.com)
- PostgreSQL provisionado no Render (banco externo)
- Variáveis de ambiente definidas no Render

---

## 🚀 Deploy no Render (Passo a passo)

1. **Faça push do projeto para um repositório no GitHub**.
2. **Crie um novo serviço no [Render](https://render.com)** do tipo "Web Service".
3. Escolha a opção **"Connect a repository"** e selecione este projeto.
4. Configure o deploy com:
   - **Build Command**: *(deixe em branco)*
   - **Start Command**: `gunicorn "src.main:create_app()"`
   - **Environment**: `Python 3`
5. Vá na aba **Environment > Environment Variables** e adicione:
   - `DATABASE_URL` = `postgresql://usuario:senha@host:porta/banco`
   - `SECRET_KEY` = `sua_chave_aleatoria_segura`
   - `FLASK_ENV` = `production` (opcional)

---

## 🧪 Teste local

```bash
# Ativar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Rodar localmente
python src/main.py
```

---

## 📁 Estrutura do Projeto

- `src/` → Código-fonte principal
- `src/models/` → Modelos do banco (User, Post, Gallery etc.)
- `src/routes/` → Blueprints organizados por função
- `templates/` → HTMLs do Jinja2
- `static/` → Imagens, CSS, JS (criar se ainda não existir)
- `Procfile` → Instrução para o Render
- `start.sh` → Script auxiliar (opcional)
- `reset_db.py` → Utilitário para resetar o banco (desenvolvimento)

---

## 👥 Admin

Após criar o banco, rode `reset_admin.py` para criar um usuário admin localmente.

---

## 🛠️ Observações

- Para produção, considere usar Flask-Migrate no lugar de `db.create_all()`.
