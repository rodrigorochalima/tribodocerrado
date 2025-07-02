# 🏍️ Tribo do Cerrado - Motoclube de Goiânia

Sistema completo para o motoclube Tribo do Cerrado, desenvolvido com tecnologias modernas e arquitetura escalável.

## 🌐 **Site Oficial**
**https://tribodocerrado.org**

## 🚀 **Tecnologias**

### **Frontend**
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS (design system)
- Framer Motion (animações)
- React Router (navegação)
- Leaflet (mapas interativos)

### **Backend**
- Node.js + Express
- TypeScript
- Prisma ORM
- PostgreSQL (Neon)
- JWT + bcrypt (autenticação)
- Cloudinary (upload de imagens)
- Nodemailer + Migadu (e-mail)

### **Infraestrutura**
- GitHub Actions (CI/CD)
- Neon PostgreSQL (banco gratuito)
- GitHub Pages (hospedagem)
- Cloudinary (CDN de imagens)
- Migadu (servidor de e-mail)

## 📁 **Estrutura do Projeto**

```
tribodocerrado/
├── frontend/                 # Aplicação React
│   ├── src/
│   │   ├── components/      # Componentes reutilizáveis
│   │   ├── pages/          # Páginas da aplicação
│   │   ├── contexts/       # Context API (estado global)
│   │   ├── services/       # Serviços e APIs
│   │   └── styles/         # Estilos globais
│   ├── public/             # Arquivos estáticos
│   └── package.json
├── backend/                  # API Node.js
│   ├── src/
│   │   ├── routes/         # Rotas da API
│   │   ├── middleware/     # Middlewares
│   │   ├── utils/          # Utilitários
│   │   └── server.ts       # Servidor principal
│   ├── prisma/             # Schema do banco
│   └── package.json
├── .github/workflows/        # GitHub Actions
├── index.html               # Página inicial (GitHub Pages)
├── LogoTriboSite.png        # Logo oficial
├── FundoSIte.png           # Imagem de fundo
└── README.md               # Este arquivo
```

## 🎯 **Funcionalidades**

### **✅ Implementadas**
- 🏠 **Página inicial** com design responsivo
- 🔐 **Sistema de autenticação** (login/registro)
- 👤 **Perfis de usuário** completos
- 📅 **Agenda de eventos** interativa
- 🗺️ **Mapas integrados** (OpenStreetMap)
- 📧 **Sistema de e-mail** (Migadu API)
- 🖼️ **Upload de imagens** (Cloudinary)
- 📱 **Design responsivo** (mobile-first)
- 🔥 **Animações** e efeitos visuais

### **🚧 Em Desenvolvimento**
- 📊 Dashboard administrativo
- 🚗 Sistema de comboios
- 🏆 Sistema de prêmios e menções
- 👨‍👩‍👧‍👦 Cadastro de familiares
- 🏍️ Cadastro de motos
- 📄 Visualizador de estatuto

## 🛠️ **Desenvolvimento Local**

### **Pré-requisitos**
- Node.js 18+
- npm ou yarn
- Conta no Neon PostgreSQL
- Conta no Cloudinary (opcional)

### **Configuração**

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/rodrigorochalima/tribodocerrado.git
   cd tribodocerrado
   ```

2. **Configure o backend:**
   ```bash
   cd backend
   npm install
   cp .env.example .env
   # Configure as variáveis no .env
   npx prisma generate
   npx prisma db push
   npm run dev
   ```

3. **Configure o frontend:**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Acesse:**
   - Frontend: http://localhost:5173
   - Backend: http://localhost:3000

## 🔧 **Configuração de Produção**

### **Variáveis de Ambiente**
```env
# Banco de dados
DATABASE_URL=postgresql://user:pass@host/db

# Autenticação
JWT_SECRET=sua-chave-secreta

# Cloudinary (upload de imagens)
CLOUDINARY_CLOUD_NAME=seu-cloud-name
CLOUDINARY_API_KEY=sua-api-key
CLOUDINARY_API_SECRET=seu-api-secret

# E-mail (Migadu)
SMTP_HOST=smtp.migadu.com
SMTP_PORT=587
SMTP_USER=admin@tribodocerrado.org
SMTP_PASS=sua-senha
```

### **Deploy Automático**
O projeto usa GitHub Actions para deploy automático:
- **Push na main** → Deploy automático
- **Testes** executados automaticamente
- **Build** e deploy no GitHub Pages

## 📊 **Banco de Dados**

### **Schema Principal**
- **usuarios** - Dados dos membros
- **eventos** - Agenda de eventos
- **familiares** - Familiares dos membros
- **motos** - Motos cadastradas
- **premios_mencoes** - Prêmios e menções
- **participacoes_eventos** - Participações em eventos

### **Dados Iniciais**
- **Admin:** admin@tribodocerrado.org / 123456
- **Eventos de exemplo** carregados
- **Estrutura completa** configurada

## 🎨 **Design System**

### **Cores**
- **Primária:** #ff6b35 (laranja fogo)
- **Secundária:** #ff8c42 (laranja claro)
- **Dourado:** #FFD700 (títulos)
- **Escuro:** #0f172a (backgrounds)

### **Tipografia**
- **Títulos:** Cinzel (serif elegante)
- **Corpo:** Inter (sans-serif moderna)

### **Componentes**
- Botões com efeito de fogo
- Cards metálicos
- Animações fluidas
- Design responsivo

## 📱 **Responsividade**

- **Desktop:** Layout completo
- **Tablet:** Adaptado para touch
- **Mobile:** Menu colapsável, layout vertical

## 🔐 **Segurança**

- **JWT** para autenticação
- **bcrypt** para senhas
- **CORS** configurado
- **Validação** de dados
- **Sanitização** de inputs

## 📞 **Contato**

**Tribo do Cerrado Motoclube**
- **Site:** https://tribodocerrado.org
- **E-mail:** admin@tribodocerrado.org
- **Localização:** Goiânia, GO

---

## 📄 **Licença**

Este projeto é propriedade do **Tribo do Cerrado Motoclube**.

---

**🏍️ Desenvolvido com ❤️ para a Tribo do Cerrado**

