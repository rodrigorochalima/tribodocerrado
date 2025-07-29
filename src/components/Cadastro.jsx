import React, { useState } from 'react';
import { supabase } from '../lib/supabase';

const CadastroIntegrado = () => {
  const [formData, setFormData] = useState({
    nomeCompleto: '',
    email: '',
    telefone: '',
    senha: '',
    confirmarSenha: ''
  });
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState('');
  const [sucesso, setSucesso] = useState(false);

  // Função para hash simples da senha (em produção usar bcrypt)
  const hashSenha = (senha) => {
    return btoa(senha); // Base64 simples para teste
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErro('');

    // Validações
    if (formData.senha !== formData.confirmarSenha) {
      setErro('As senhas não coincidem');
      setLoading(false);
      return;
    }

    if (formData.senha.length < 6) {
      setErro('A senha deve ter pelo menos 6 caracteres');
      setLoading(false);
      return;
    }

    try {
      // Verificar se email já existe
      const { data: emailExiste } = await supabase
        .from('usuarios')
        .select('email')
        .eq('email', formData.email)
        .single();

      if (emailExiste) {
        setErro('Este email já está cadastrado');
        setLoading(false);
        return;
      }

      // Hash da senha
      const senhaHash = hashSenha(formData.senha);

      // Inserir usuário na tabela customizada
      const { data, error } = await supabase
        .from('usuarios')
        .insert([
          {
            nome_completo: formData.nomeCompleto,
            nome: formData.nomeCompleto.split(' ')[0], // Primeiro nome
            email: formData.email,
            telefone: formData.telefone,
            senha: senhaHash, // Adicionar campo senha na tabela
            tipo: 'membro',
            status: 'ativo',
            ativo: true,
            data_cadastro: new Date().toISOString(),
            criado_em: new Date().toISOString(),
            atualizado_em: new Date().toISOString()
          }
        ])
        .select();

      if (error) {
        console.error('Erro ao cadastrar:', error);
        setErro('Erro ao salvar dados. Tente novamente.');
        setLoading(false);
        return;
      }

      // Sucesso - mostrar mensagem e redirecionar
      setSucesso(true);
      
      // Aguardar 2 segundos e redirecionar para login
      setTimeout(() => {
        window.location.href = '/login';
      }, 2000);

    } catch (error) {
      console.error('Erro no cadastro:', error);
      setErro('Erro interno. Tente novamente.');
    }

    setLoading(false);
  };

  if (sucesso) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-400 via-blue-500 to-purple-600 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md text-center">
          <div className="text-6xl mb-4">🎉</div>
          <h1 className="text-3xl font-bold text-green-600 mb-4">Cadastro Realizado!</h1>
          <p className="text-gray-600 mb-6">
            Sua conta foi criada com sucesso. Você será redirecionado para o login em instantes.
          </p>
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-green-500 mx-auto"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-400 via-blue-500 to-purple-600 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">📝 Cadastro</h1>
          <p className="text-gray-600">Registre-se como novo membro do Tribo do Cerrado</p>
        </div>

        {erro && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {erro}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              👤 Nome Completo
            </label>
            <input
              type="text"
              name="nomeCompleto"
              value={formData.nomeCompleto}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Seu nome completo"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              📧 Email
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="seu@email.com"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              📱 Telefone
            </label>
            <input
              type="tel"
              name="telefone"
              value={formData.telefone}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="(62) 99999-9999"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              🔒 Senha
            </label>
            <input
              type="password"
              name="senha"
              value={formData.senha}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Mínimo 6 caracteres"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              🔒 Confirmar Senha
            </label>
            <input
              type="password"
              name="confirmarSenha"
              value={formData.confirmarSenha}
              onChange={handleInputChange}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Digite a senha novamente"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white font-bold py-3 px-4 rounded-lg hover:from-blue-600 hover:to-purple-700 transition duration-300 disabled:opacity-50"
          >
            {loading ? '⏳ Cadastrando...' : '📝 CRIAR CONTA'}
          </button>
        </form>

        <div className="mt-6 text-center space-y-4">
          <button
            onClick={() => window.location.href = '/login'}
            className="text-blue-600 hover:text-blue-800 font-medium"
          >
            🔐 Já tenho conta
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

export default CadastroIntegrado;
