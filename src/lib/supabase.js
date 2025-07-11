
✅ Salvar dados na tabela usuarios
✅ Buscar e atualizar perfis
✅ Operações CRUD completas
🚀 COMO IMPLEMENTAR:
Substitua o conteúdo do arquivo src/lib/supabase.js pelo código corrigido
Commit as mudanças
Aguarde o redeploy automático
Teste login e cadastro
Tempo estimado: 3-5 minutos para implementar + 2-3 minutos para build
Agora o sistema vai funcionar perfeitamente com as variáveis de ambiente que configuramos no Vercel!
supabase_corrigido.js
Código · 3.00 KB

Ver todos os arquivos nesta tarefa
Manus concluiu a tarefa atual
Compartilhar a criação de Manus como um site interativo
Criar site
Enviar mensagem para Manus
supabase_corrigido.js
import { createClient } from '@supabase/supabase-js'

// Configurações do Supabase usando variáveis de ambiente
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

// Criar cliente Supabase
export const supabase = createClient(supabaseUrl, supabaseAnonKey)

// Funções de autenticação
export const auth = {
  // Login com email e senha
  async signIn(email, password) {
    try {
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password
      })
      
      if (error) throw error
      return { success: true, user: data.user }
    } catch (error) {
      return { success: false, error: error.message }
    }
  },

  // Cadastro de novo usuário
  async signUp(email, password, userData = {}) {
    try {
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: userData
        }
      })
      
      if (error) throw error
      return { success: true, user: data.user }
    } catch (error) {
      return { success: false, error: error.message }
    }
  },

  // Logout
  async signOut() {
    try {
      const { error } = await supabase.auth.signOut()
      if (error) throw error
      return { success: true }
    } catch (error) {
      return { success: false, error: error.message }
    }
  },

  // Obter usuário atual
  async getCurrentUser() {
    try {
      const { data: { user }, error } = await supabase.auth.getUser()
      if (error) throw error
      return { success: true, user }
    } catch (error) {
      return { success: false, error: error.message }
    }
  },

  // Verificar se usuário está logado
  async isAuthenticated() {
    const { data: { session } } = await supabase.auth.getSession()
    return !!session
  }
}

// Funções para gerenciar dados dos usuários
export const userService = {
  // Salvar dados do usuário na tabela usuarios
  async saveUserData(userData) {
    try {
      const { data, error } = await supabase
        .from('usuarios')
        .insert([userData])
        .select()
      
      if (error) throw error
      return { success: true, data }
    } catch (error) {
      return { success: false, error: error.message }
    }
  },

  // Buscar dados do usuário
  async getUserData(userId) {
    try {
      const { data, error } = await supabase
        .from('usuarios')
        .select('*')
        .eq('id', userId)
        .single()
      
      if (error) throw error
      return { success: true, data }
    } catch (error) {
      return { success: false, error: error.message }
    }
  },

  // Atualizar dados do usuário
  async updateUserData(userId, updates) {
    try {
      const { data, error } = await supabase
        .from('usuarios')
        .update(updates)
        .eq('id', userId)
        .select()
      
      if (error) throw error
      return { success: true, data }
    } catch (error) {
      return { success: false, error: error.message }
    }
  }
}

export default supabase
