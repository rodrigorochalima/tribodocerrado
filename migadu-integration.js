/**
 * INTEGRAÇÃO MIGADU API - TRIBO DO CERRADO
 * Sistema para gerenciar emails @tribodocerrado.org
 */

class MigaduIntegration {
    constructor() {
        this.baseURL = 'https://api.migadu.com/v1';
        this.domain = 'tribodocerrado.org';
        
        // CONFIGURAÇÕES DA API - DEVEM SER CONFIGURADAS NO PAINEL MIGADU
        this.config = {
            username: 'administrador@tribodocerrado.org', // Email do administrador
            apiKey: 'SUA_API_KEY_AQUI', // Gerar no painel Migadu
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
        };
    }

    /**
     * Criar autenticação Basic Auth para API
     */
    getAuthHeader() {
        const credentials = btoa(`${this.config.username}:${this.config.apiKey}`);
        return `Basic ${credentials}`;
    }

    /**
     * Criar nova caixa de email @tribodocerrado.org
     * @param {Object} userData - Dados do usuário
     * @returns {Promise<Object>} - Resultado da criação
     */
    async criarEmailUsuario(userData) {
        try {
            const localPart = this.gerarLocalPart(userData.apelido);
            const emailCompleto = `${localPart}@${this.domain}`;
            
            const mailboxData = {
                local_part: localPart,
                name: userData.nome,
                password: this.gerarSenhaTemporaria(),
                is_internal: true,
                may_send: true,
                may_receive: true,
                may_access_imap: true,
                may_access_pop3: true,
                may_access_managesieve: true,
                password_method: "password"
            };

            const response = await this.fazerRequisicao(
                'POST',
                `/domains/${this.domain}/mailboxes`,
                mailboxData
            );

            if (response.success) {
                // Salvar dados do email no localStorage
                this.salvarDadosEmail(userData.id, {
                    email: emailCompleto,
                    senha: mailboxData.password,
                    dataCriacao: new Date().toISOString(),
                    status: 'ativo'
                });

                return {
                    success: true,
                    email: emailCompleto,
                    senha: mailboxData.password,
                    message: 'Email criado com sucesso!'
                };
            } else {
                throw new Error(response.message || 'Erro ao criar email');
            }

        } catch (error) {
            console.error('Erro ao criar email Migadu:', error);
            return {
                success: false,
                message: `Erro: ${error.message}`
            };
        }
    }

    /**
     * Listar todas as caixas de email do domínio
     */
    async listarEmails() {
        try {
            const response = await this.fazerRequisicao(
                'GET',
                `/domains/${this.domain}/mailboxes`
            );

            return response;
        } catch (error) {
            console.error('Erro ao listar emails:', error);
            return { success: false, message: error.message };
        }
    }

    /**
     * Atualizar dados de uma caixa de email
     */
    async atualizarEmail(localPart, dadosAtualizacao) {
        try {
            const response = await this.fazerRequisicao(
                'PUT',
                `/domains/${this.domain}/mailboxes/${localPart}`,
                dadosAtualizacao
            );

            return response;
        } catch (error) {
            console.error('Erro ao atualizar email:', error);
            return { success: false, message: error.message };
        }
    }

    /**
     * Deletar caixa de email
     */
    async deletarEmail(localPart) {
        try {
            const response = await this.fazerRequisicao(
                'DELETE',
                `/domains/${this.domain}/mailboxes/${localPart}`
            );

            return response;
        } catch (error) {
            console.error('Erro ao deletar email:', error);
            return { success: false, message: error.message };
        }
    }

    /**
     * Fazer requisição para API Migadu
     */
    async fazerRequisicao(method, endpoint, data = null) {
        try {
            const url = `${this.baseURL}${endpoint}`;
            const options = {
                method: method,
                headers: {
                    ...this.config.headers,
                    'Authorization': this.getAuthHeader()
                }
            };

            if (data && (method === 'POST' || method === 'PUT')) {
                options.body = JSON.stringify(data);
            }

            const response = await fetch(url, options);
            const responseData = await response.json();

            if (response.ok) {
                return {
                    success: true,
                    data: responseData,
                    status: response.status
                };
            } else {
                return {
                    success: false,
                    message: responseData.message || 'Erro na API',
                    status: response.status
                };
            }

        } catch (error) {
            console.error('Erro na requisição:', error);
            return {
                success: false,
                message: 'Erro de conexão com a API'
            };
        }
    }

    /**
     * Gerar parte local do email baseada no apelido
     */
    gerarLocalPart(apelido) {
        return apelido
            .toLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '') // Remove acentos
            .replace(/[^a-z0-9]/g, '') // Remove caracteres especiais
            .substring(0, 20); // Limita tamanho
    }

    /**
     * Gerar senha temporária segura
     */
    gerarSenhaTemporaria() {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%';
        let senha = '';
        for (let i = 0; i < 12; i++) {
            senha += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return senha;
    }

    /**
     * Salvar dados do email no localStorage
     */
    salvarDadosEmail(userId, dadosEmail) {
        const emails = JSON.parse(localStorage.getItem('emails_tribodocerrado') || '{}');
        emails[userId] = dadosEmail;
        localStorage.setItem('emails_tribodocerrado', JSON.stringify(emails));
    }

    /**
     * Obter dados do email do usuário
     */
    obterDadosEmail(userId) {
        const emails = JSON.parse(localStorage.getItem('emails_tribodocerrado') || '{}');
        return emails[userId] || null;
    }

    /**
     * Testar conexão com API
     */
    async testarConexao() {
        try {
            const response = await this.fazerRequisicao('GET', `/domains/${this.domain}`);
            return response;
        } catch (error) {
            return {
                success: false,
                message: 'Erro ao conectar com API Migadu'
            };
        }
    }

    /**
     * Configurar API Key (deve ser chamado após obter a chave)
     */
    configurarAPIKey(apiKey) {
        this.config.apiKey = apiKey;
        localStorage.setItem('migadu_api_key', apiKey);
    }

    /**
     * Carregar API Key salva
     */
    carregarAPIKey() {
        const apiKey = localStorage.getItem('migadu_api_key');
        if (apiKey) {
            this.config.apiKey = apiKey;
            return true;
        }
        return false;
    }
}

// Instância global
const migaduAPI = new MigaduIntegration();

/**
 * FUNÇÕES AUXILIARES PARA INTEGRAÇÃO COM O SITE
 */

/**
 * Criar email automaticamente no cadastro
 */
async function criarEmailNoCadastro(userData) {
    try {
        // Verificar se API está configurada
        if (!migaduAPI.carregarAPIKey()) {
            console.warn('API Migadu não configurada');
            return {
                success: false,
                message: 'Sistema de email não configurado'
            };
        }

        // Criar email via API
        const resultado = await migaduAPI.criarEmailUsuario(userData);
        
        if (resultado.success) {
            console.log(`Email criado: ${resultado.email}`);
            
            // Atualizar dados do usuário com email da Tribo
            const usuarios = JSON.parse(localStorage.getItem('usuarios') || '[]');
            const usuarioIndex = usuarios.findIndex(u => u.id === userData.id);
            
            if (usuarioIndex !== -1) {
                usuarios[usuarioIndex].emailTriboDoCerrado = resultado.email;
                usuarios[usuarioIndex].senhaEmailTriboDoCerrado = resultado.senha;
                localStorage.setItem('usuarios', JSON.stringify(usuarios));
            }
        }

        return resultado;

    } catch (error) {
        console.error('Erro ao criar email no cadastro:', error);
        return {
            success: false,
            message: 'Erro interno ao criar email'
        };
    }
}

/**
 * Obter configurações de email para cliente
 */
function obterConfiguracoesMigadu() {
    return {
        imap: {
            servidor: 'imap.migadu.com',
            porta: 993,
            ssl: true
        },
        smtp: {
            servidor: 'smtp.migadu.com',
            porta: 465,
            ssl: true
        },
        pop3: {
            servidor: 'pop.migadu.com',
            porta: 995,
            ssl: true
        },
        webmail: 'https://webmail.migadu.com'
    };
}

/**
 * Gerar link direto para webmail
 */
function gerarLinkWebmail(email) {
    return `https://webmail.migadu.com/?_user=${encodeURIComponent(email)}`;
}

// Exportar para uso global
window.MigaduIntegration = MigaduIntegration;
window.migaduAPI = migaduAPI;
window.criarEmailNoCadastro = criarEmailNoCadastro;
window.obterConfiguracoesMigadu = obterConfiguracoesMigadu;
window.gerarLinkWebmail = gerarLinkWebmail;

