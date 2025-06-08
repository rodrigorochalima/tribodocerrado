# Tribo do Cerrado - Rede Social para Motociclistas

![Tribo do Cerrado](assets/images/LogoTribodoCerrado.png)

## 🏍️ Sobre o Projeto

A **Tribo do Cerrado** é uma rede social especializada criada especificamente para motociclistas brasileiros. Inspirada no clássico Orkut, nossa plataforma combina nostalgia com funcionalidades modernas, oferecendo um espaço seguro e acolhedor para a irmandade do motociclismo.

### 🎯 Missão
*"Aqui, todas as tribos são uma só. Bem-vindo à irmandade do motociclismo."*

## ✨ Funcionalidades Principais

### 🎨 Visual e Interface
- ✅ **Tema Personalizado**: Visual inspirado no motociclismo com identidade Tribo do Cerrado
- ✅ **Layout Estilo Orkut**: Interface nostálgica com funcionalidades modernas
- ✅ **Design Responsivo**: Compatível com desktop e mobile
- ✅ **Paleta Motociclista**: Tons escuros com contrastes em vermelho e metálico

### 👥 Sistema de Usuários
- ✅ **Cadastro com Validação**: Registro por email com aprovação manual
- ✅ **Perfis Personalizados**: Informações específicas para motociclistas
- ✅ **Sistema de Amizades**: Conexões entre membros da comunidade
- ✅ **Grupos e Comunidades**: Organização por interesses e localização

### 🛡️ Moderação e Segurança
- ✅ **Sistema de Denúncias**: Ferramenta para reportar conteúdo inadequado
- ✅ **Painel de Moderação**: Dashboard completo para moderadores
- ✅ **Níveis de Permissão**: Moderador principal e submoderadores
- ✅ **Notificações Automáticas**: Alertas por email para moderadores
- ✅ **Logs de Atividade**: Rastreamento completo de ações de moderação

### 🗄️ Banco de Dados
- ✅ **PostgreSQL**: Migração completa do MySQL padrão
- ✅ **Otimizado para Render.com**: Configuração específica para deploy
- ✅ **Escalabilidade**: Estrutura preparada para crescimento
- ✅ **Backup Automático**: Scripts de backup e recuperação

### 🚀 Deploy e Hospedagem
- ✅ **Docker**: Containerização completa da aplicação
- ✅ **Render.com Ready**: Configuração otimizada para deploy gratuito
- ✅ **GitHub Integration**: Deploy automático via GitHub
- ✅ **Health Checks**: Monitoramento de saúde da aplicação

## 🛠️ Tecnologias Utilizadas

### Backend
- **PHP 8.1+**: Linguagem principal
- **HumHub**: Framework de rede social open-source
- **Yii2**: Framework PHP para desenvolvimento web
- **PostgreSQL 14**: Banco de dados principal

### Frontend
- **HTML5/CSS3**: Estrutura e estilização
- **JavaScript ES6+**: Interatividade
- **Bootstrap 4**: Framework CSS responsivo
- **Font Awesome**: Biblioteca de ícones

### DevOps
- **Docker**: Containerização
- **Apache**: Servidor web
- **Render.com**: Plataforma de hospedagem
- **GitHub Actions**: CI/CD pipeline

## 📋 Pré-requisitos

### Para Desenvolvimento Local
- PHP 8.1 ou superior
- PostgreSQL 14 ou superior
- Composer
- Docker (opcional)
- Git

### Para Deploy em Produção
- Conta no GitHub
- Conta no Render.com
- Domínio personalizado (opcional)

## 🚀 Instalação e Deploy

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/tribo-cerrado-social.git
cd tribo-cerrado-social
```

### 2. Configuração Local
```bash
# Instalar dependências
composer install

# Configurar banco de dados
cp protected/config/common.php.example protected/config/common.php
# Edite as configurações de banco

# Executar migrações
php protected/yii migrate
```

### 3. Deploy no Render.com
Consulte o [Manual de Deploy](docs/MANUAL_DEPLOY.md) para instruções detalhadas.

## 📚 Documentação

### Manuais Disponíveis
- 📖 **[Manual de Deploy](docs/MANUAL_DEPLOY.md)**: Guia completo para deploy no GitHub e Render.com
- 👤 **[Manual do Usuário](docs/MANUAL_USUARIO.md)**: Guia completo para usuários da plataforma
- 🔧 **[Documentação Técnica](docs/DOCUMENTACAO_TECNICA.md)**: Especificações técnicas e arquitetura

### Estrutura do Projeto
```
tribo-cerrado-social/
├── assets/                    # Assets estáticos
├── docs/                      # Documentação
├── protected/                 # Código da aplicação
│   ├── config/               # Configurações
│   ├── modules/              # Módulos customizados
│   └── ...
├── themes/                    # Temas personalizados
│   └── tribo-cerrado/        # Tema principal
├── docker/                    # Configurações Docker
├── database/                  # Scripts de banco
├── Dockerfile                 # Configuração Docker
├── render.yaml               # Configuração Render.com
└── README.md                 # Este arquivo
```

## 🎨 Personalização

### Tema Tribo do Cerrado
O tema personalizado está localizado em `themes/tribo-cerrado/` e inclui:
- CSS customizado com paleta motociclista
- Layouts adaptados para a comunidade
- JavaScript personalizado
- Assets visuais (logos, ícones)

### Módulo de Moderação
Localizado em `protected/modules/tribo-moderation/`, oferece:
- Sistema completo de denúncias
- Dashboard de moderação
- Logs de atividade
- Notificações automáticas

## 🔧 Configuração

### Variáveis de Ambiente
```bash
# Banco de dados
DATABASE_URL=postgresql://user:pass@host:port/db

# Segurança
COOKIE_VALIDATION_KEY=sua-chave-secreta

# Email
MAILER_HOST=smtp.gmail.com
MAILER_USERNAME=seu-email@gmail.com
MAILER_PASSWORD=sua-senha-app

# Administração
ADMIN_EMAIL=admin@tribodocerrado.com
ADMIN_PASSWORD=senha-segura
```

### Configurações Específicas
- **Moderação**: Configure níveis de permissão em `protected/modules/tribo-moderation/config/`
- **Tema**: Personalize cores e estilos em `themes/tribo-cerrado/css/`
- **Email**: Configure templates em `protected/mail/`

## 🤝 Contribuindo

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Diretrizes
- Siga os padrões PSR-12 para PHP
- Documente novas funcionalidades
- Teste suas alterações localmente
- Mantenha commits pequenos e focados

## 🐛 Reportando Problemas

### Issues no GitHub
Use o sistema de Issues do GitHub para:
- Reportar bugs
- Sugerir melhorias
- Solicitar novas funcionalidades
- Fazer perguntas técnicas

### Informações Úteis
Ao reportar problemas, inclua:
- Descrição detalhada do problema
- Passos para reproduzir
- Screenshots (se aplicável)
- Informações do ambiente (navegador, OS)

## 📈 Roadmap

### Próximas Funcionalidades
- 🎥 **Integração YouTube**: Exibição de vídeos dos usuários
- 📁 **Integração Mega.nz**: Repositório de fotos compartilhado
- 📱 **App Mobile**: Progressive Web App (PWA)
- 🗺️ **Sistema de Rotas**: Planejamento de viagens
- 🛒 **Marketplace**: Compra e venda de equipamentos

### Melhorias Planejadas
- Sistema de eventos avançado
- Chat em tempo real
- Notificações push
- Integração com redes sociais
- Sistema de reputação

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Equipe

### Desenvolvimento
- **Manus AI**: Arquiteto Principal e Desenvolvedor

### Comunidade
- **Motociclistas do Cerrado**: Inspiração e feedback
- **Contribuidores**: Desenvolvedores da comunidade

## 📞 Suporte

### Contatos
- **Email Geral**: contato@tribodocerrado.com
- **Suporte Técnico**: suporte@tribodocerrado.com
- **Emergências**: emergencia@tribodocerrado.com

### Links Úteis
- **Site Oficial**: https://tribodocerrado.com
- **Documentação**: https://docs.tribodocerrado.com
- **Status**: https://status.tribodocerrado.com

## 🙏 Agradecimentos

Agradecemos especialmente:
- **Comunidade HumHub**: Pelo framework open-source
- **Motociclistas do Brasil**: Pela inspiração e feedback
- **Render.com**: Pela plataforma de hospedagem
- **Todos os Contribuidores**: Que ajudam a melhorar o projeto

---

## 🏍️ Junte-se à Tribo!

*"Aqui, todas as tribos são uma só. Bem-vindo à irmandade do motociclismo."*

**Que a estrada seja sempre segura e as aventuras inesquecíveis!**

---

**Versão**: 1.0.0  
**Data**: Junho 2024  
**Última Atualização**: 08/06/2024

