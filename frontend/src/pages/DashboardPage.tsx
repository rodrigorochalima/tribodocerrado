import React from 'react';
import { motion } from 'framer-motion';
import { Calendar, Users, Bike, Mail } from 'lucide-react';

const DashboardPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="text-3xl font-metal font-bold text-glow mb-8">
            Dashboard - Tribo do Cerrado
          </h1>

          {/* Cards de estatísticas */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="card-metal p-6 text-center">
              <Calendar className="w-12 h-12 text-primary-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Próximos Eventos</h3>
              <p className="text-3xl font-bold text-primary-400">3</p>
            </div>
            
            <div className="card-metal p-6 text-center">
              <Users className="w-12 h-12 text-primary-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Membros Ativos</h3>
              <p className="text-3xl font-bold text-primary-400">45</p>
            </div>
            
            <div className="card-metal p-6 text-center">
              <Bike className="w-12 h-12 text-primary-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Comboios</h3>
              <p className="text-3xl font-bold text-primary-400">2</p>
            </div>
            
            <div className="card-metal p-6 text-center">
              <Mail className="w-12 h-12 text-primary-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">Mensagens</h3>
              <p className="text-3xl font-bold text-primary-400">8</p>
            </div>
          </div>

          {/* Conteúdo principal */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="card-metal p-6">
              <h2 className="text-2xl font-semibold mb-4 text-primary-400">
                Próximos Eventos
              </h2>
              <div className="space-y-4">
                <div className="border-l-4 border-primary-500 pl-4">
                  <h3 className="font-semibold">Encontro Mensal - Janeiro</h3>
                  <p className="text-gray-300">15 de Janeiro, 2025</p>
                  <p className="text-sm text-gray-400">Parque Areião - Goiânia</p>
                </div>
                <div className="border-l-4 border-primary-500 pl-4">
                  <h3 className="font-semibold">Trilha do Descoberto</h3>
                  <p className="text-gray-300">22 de Janeiro, 2025</p>
                  <p className="text-sm text-gray-400">Águas Lindas - GO</p>
                </div>
                <div className="border-l-4 border-primary-500 pl-4">
                  <h3 className="font-semibold">Passeio Histórico</h3>
                  <p className="text-gray-300">5 de Fevereiro, 2025</p>
                  <p className="text-sm text-gray-400">Pirenópolis - GO</p>
                </div>
              </div>
            </div>

            <div className="card-metal p-6">
              <h2 className="text-2xl font-semibold mb-4 text-primary-400">
                Atividades Recentes
              </h2>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
                  <p className="text-gray-300">João Silva se inscreveu no evento "Trilha do Descoberto"</p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
                  <p className="text-gray-300">Maria Santos atualizou seu perfil</p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
                  <p className="text-gray-300">Novo membro: Carlos Oliveira</p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-primary-500 rounded-full"></div>
                  <p className="text-gray-300">Evento "Encontro Mensal" foi atualizado</p>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default DashboardPage;

