import React, { useState, useEffect } from 'react';
import { supabase } from '../lib/supabase';

const AreaMembros = () => {
  const [usuario, setUsuario] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('perfil');

  useEffect(() => {
    // Verificar sessão
    const session = localStorage.getItem('triboCerradoSession');
    if (!session) {
      window.location.href = '/login';
      return;
    }

    try {
      const sessionData = JSON.parse(session);
      if (!sessionData.authenticated) {
        window.location.href = '/login';
        return;
      }

      setUsuario(sessionData.user);
      setLoading(false);
    } catch (error) {
      console.error('Erro ao verificar sessão:', error);
      window.location.href = '/login';
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('triboCerradoSession');
    window.location.href = '/';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-400 via-blue-500 to-purple-600 flex items-center justify-center">
        <div className="text-white text-2xl">⏳ Carregando...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-400 via-blue-500 to-purple-600">
      {/* Header */}
      <header className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <h1 className="text-3xl font-bold text-gray-900">🏍️ Tribo do Cerrado MC</h1>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Olá, {usuario?.nome || 'Membro'}!</span>
              <button
                onClick={handleLogout}
                className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition duration-300"
              >
                🚪 Sair
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          {/* Navigation Tabs */}
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {[
                { id: 'perfil', label: '👤 Perfil', icon: '👤' },
                { id: 'eventos', label: '📅 Eventos', icon: '📅' },
                { id: 'membros', label: '👥 Membros', icon: '👥' },
                { id: 'configuracoes', label: '⚙️ Configurações', icon: '⚙️' }
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-2 border-b-2 font-medium text-sm ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>

          {/* Content */}
          <div className="p-6">
            {activeTab === 'perfil' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-gray-900">👤 Meu Perfil</h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="bg-gray-50 p-6 rounded-lg">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">📋 Informações Pessoais</h3>
                    <div className="space-y-3">
                      <div>
                        <label className="block text-sm font-medium text-gray-700">Nome</label>
                        <p className="mt-1 text-sm text-gray-900">{usuario?.nome || 'Não informado'}</p>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700">Email</label>
                        <p className="mt-1 text-sm text-gray-900">{usuario?.email}</p>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700">Tipo de Membro</label>
                        <p className="mt-1 text-sm text-gray-900 capitalize">{usuario?.tipo || 'Membro'}</p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-gray-50 p-6 rounded-lg">
                    <h3 className="text-lg font-semibold text-gray-900 mb-4">🏍️ Status no Clube</h3>
                    <div className="space-y-3">
                      <div className="flex items-center">
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          ✅ Ativo
                        </span>
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700">Membro desde</label>
                        <p className="mt-1 text-sm text-gray-900">Hoje</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-blue-50 p-6 rounded-lg">
                  <h3 className="text-lg font-semibold text-blue-900 mb-2">🎉 Bem-vindo ao Tribo do Cerrado MC!</h3>
                  <p className="text-blue-700">
                    Você agora faz parte da nossa família motociclística. Explore as abas acima para conhecer mais sobre eventos, 
                    outros membros e configurar seu perfil.
                  </p>
                </div>
              </div>
            )}

            {activeTab === 'eventos' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-gray-900">📅 Eventos</h2>
                <div className="bg-yellow-50 p-6 rounded-lg">
                  <h3 className="text-lg font-semibold text-yellow-900 mb-2">🚧 Em Desenvolvimento</h3>
                  <p className="text-yellow-700">
                    A seção de eventos está sendo desenvolvida. Em breve você poderá ver e se inscrever em eventos do clube.
                  </p>
                </div>
              </div>
            )}

            {activeTab === 'membros' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-gray-900">👥 Membros</h2>
                <div className="bg-purple-50 p-6 rounded-lg">
                  <h3 className="text-lg font-semibold text-purple-900 mb-2">🚧 Em Desenvolvimento</h3>
                  <p className="text-purple-700">
                    A seção de membros está sendo desenvolvida. Em breve você poderá ver outros membros do clube.
                  </p>
                </div>
              </div>
            )}

            {activeTab === 'configuracoes' && (
              <div className="space-y-6">
                <h2 className="text-2xl font-bold text-gray-900">⚙️ Configurações</h2>
                <div className="bg-gray-50 p-6 rounded-lg">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">🔧 Configurações da Conta</h3>
                  <div className="space-y-4">
                    <button className="w-full text-left p-4 bg-white border border-gray-200 rounded-lg hover:bg-gray-50">
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="font-medium text-gray-900">✏️ Editar Perfil</h4>
                          <p className="text-sm text-gray-500">Alterar informações pessoais</p>
                        </div>
                        <span className="text-gray-400">→</span>
                      </div>
                    </button>
                    
                    <button className="w-full text-left p-4 bg-white border border-gray-200 rounded-lg hover:bg-gray-50">
                      <div className="flex items-center justify-between">
                        <div>
                          <h4 className="font-medium text-gray-900">🔒 Alterar Senha</h4>
                          <p className="text-sm text-gray-500">Modificar senha de acesso</p>
                        </div>
                        <span className="text-gray-400">→</span>
                      </div>
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AreaMembros;
