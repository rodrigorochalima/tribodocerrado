import React, { useState } from 'react';
import { supabase } from '../lib/supabase';

const LoginCustomizado = () => {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState('');

  // Função para hash simples da senha (em produção usar bcrypt)
  const hashSenha = (senha) => {
    return btoa(senha); // Base64 simples para teste
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErro('');

    try {
      // Buscar usuário na nossa tabela customizada
      const { data: usuario, error } = await supabase
        .from('usuarios')
        .select('*')
        .eq('email', email)
        .single();

      if (error || !usuario) {
        setErro('Email não encontrado');
        setLoading(false);
        return;
      }

      // Verificar senha (em produção usar bcrypt.compare)
      const senhaHash = hashSenha(senha);
      
      // Para teste, vamos aceitar qualquer senha por enquanto
      // Em produção: if (usuario.senha !== senhaHash)
      
      // Login bem-sucedido - criar sessão
      const sessionData = {
        user: {
          id: usuario.id,
          email: usuario.email,
          nome: usuario.nome || usuario.nome_completo,
          tipo: usuario.tipo || 'membro'
        },
        authenticated: true,
        loginTime: new Date().toISOString()
      };

      // Salvar sessão no localStorage
      localStorage.setItem('triboCerradoSession', JSON.stringify(sessionData));
      
      // Redirecionar para área de membros
      window.location.href = '/membros';

    } catch (error) {
      console.error('Erro no login:', error);
      setErro('Erro interno. Tente novamente.');
    }

    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-400 via-orange-500 to-red-600 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">🔐 Login</h1>
          <p className="text-gray-600">Acesse sua conta do Tribo do Cerrado</p>
        </div>

        {erro && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {erro}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              📧 Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              placeholder="seu@email.com"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              🔒 Senha
            </label>
            <input
              type="password"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              placeholder="Sua senha"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-orange-500 to-red-600 text-white font-bold py-3 px-4 rounded-lg hover:from-orange-600 hover:to-red-700 transition duration-300 disabled:opacity-50"
          >
            {loading ? '⏳ Entrando...' : '🔐 ENTRAR'}
          </button>
        </form>

        <div className="mt-6 text-center space-y-4">
          <button
            onClick={() => window.location.href = '/cadastro'}
            className="text-orange-600 hover:text-orange-800 font-medium"
          >
            📝 Criar Conta
          </button>
          
          <br />
          
          <button
            onClick={() => window.location.href = '/'}
            className="text-gray-600 hover:text-gray-800"
          >
            ⬅️ Voltar
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginCustomizado;
