# 🏍️ Tribo do Cerrado - Agenda de Eventos

Sistema completo de agenda de eventos para motoclubes com funcionalidades avançadas de moderação, calendário interativo e sistema de participação.

## ✨ Funcionalidades

### 🎯 **Para Usuários:**
- ✅ Calendário interativo com navegação por meses
- ✅ Visualização de eventos aprovados
- ✅ Sistema de sugestão de eventos com mapa
- ✅ Busca automática de endereços
- ✅ Sistema de participação e comboios
- ✅ Interface responsiva (mobile/desktop)

### 🛡️ **Para Administradores:**
- ✅ Painel de moderação exclusivo
- ✅ Gerenciamento completo de usuários
- ✅ Aprovação/rejeição de eventos
- ✅ Criação direta de eventos (aprovados automaticamente)
- ✅ Exclusão de usuários e eventos
- ✅ Controle total do sistema

## 🚀 Deploy Permanente

### **1. Configurar Neon PostgreSQL (GRATUITO)**

1. **Criar conta no Neon:**
   - Acesse: https://neon.com/
   - Clique em "Sign Up" (gratuito)
   - Use GitHub ou email para criar conta

2. **Criar projeto:**
   - Nome: `tribo-cerrado-agenda`
   - Região: `US East (Ohio)` (recomendado)
   - PostgreSQL version: `16` (mais recente)

3. **Copiar string de conexão:**
   - No dashboard, clique em "Connection string"
   - Copie a URL completa que começa com `postgresql://`
   - Exemplo: `postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require`

### **2. Configurar GitHub Secrets**

No seu repositório GitHub, vá em **Settings > Secrets and variables > Actions** e adicione:

```
NEON_DATABASE_URL = postgresql://user:pass@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
SECRET_KEY = tribo-cerrado-agenda-eventos-2025-super-segura
CLOUDINARY_CLOUD_NAME = demo
CLOUDINARY_API_KEY = your-api-key  
CLOUDINARY_API_SECRET = your-api-secret
```

### **3. Fazer Deploy**

1. **Push para GitHub:**
   ```bash
   git add .
   git commit -m "Deploy sistema completo Tribo do Cerrado"
   git push origin main
   ```

2. **Acompanhar deploy:**
   - Vá em **Actions** no GitHub
   - Veja os logs em tempo real
   - Deploy automático a cada push

### **4. Acessar Sistema**

- **URL**: Será gerada automaticamente pelo GitHub Pages ou Vercel
- **Admin**: `admin@tribodocerrado.com` / `123456`
- **Moderação**: Aba "Moderação" (apenas para admins)

## 🔧 Configuração Local

### **Pré-requisitos:**
- Python 3.11+
- PostgreSQL (ou usar Neon)

### **Instalação:**

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SEU_USUARIO/tribo-cerrado-agenda.git
   cd tribo-cerrado-agenda
   ```

2. **Instale dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure .env:**
   ```bash
   cp .env.example .env
   # Edite .env com suas configurações
   ```

4. **Execute:**
   ```bash
   python src/main.py
   ```

5. **Acesse:**
   - Local: http://localhost:5000
   - Admin: admin@tribodocerrado.com / 123456

## 📊 Logs e Monitoramento

### **GitHub Actions:**
- Logs completos de cada deploy
- Status de sucesso/falha
- Testes automáticos
- Notificações de erro

### **Neon Dashboard:**
- Métricas de uso do banco
- Logs de conexão
- Backup automático
- Branching para desenvolvimento

## 🛠️ Tecnologias

- **Backend**: Flask + SQLAlchemy
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Banco**: PostgreSQL (Neon)
- **Mapas**: OpenStreetMap + Leaflet
- **Deploy**: GitHub Actions
- **Hospedagem**: Neon (banco) + GitHub Pages

## 📱 Responsividade

- **Desktop**: Logo 300px, layout completo
- **Tablet**: Logo 250px, navegação adaptada
- **Mobile**: Logo 200px, menu vertical

## 🎨 Design

- **Tema**: Harley Davidson (laranja/preto)
- **Logo**: Emblema fixo no topo
- **Fundo**: Imagem dramática com fogo e caveiras
- **Transparência**: Caixas flutuantes sobre o fundo

## 🔐 Segurança

- Autenticação por sessão
- Validação de permissões
- Sanitização de dados
- CORS configurado
- Secrets no GitHub

## 📞 Suporte

Sistema desenvolvido especificamente para a **Tribo do Cerrado**.

**Funcionalidades principais:**
- ✅ Sistema de eventos completo
- ✅ Moderação avançada
- ✅ Deploy automático
- ✅ Logs visíveis
- ✅ Banco gratuito (Neon)
- ✅ Interface profissional

---

**🏍️ Desenvolvido para a Tribo do Cerrado - Motoclube**

