import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Bike, Users, Calendar, Mail, FileText } from 'lucide-react';

const HomePage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center relative overflow-hidden">
      {/* Background Image - Integral e bem posicionada */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `url('/FundoSIte.png')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat'
        }}
      />
      
      {/* Overlay escuro para melhor legibilidade */}
      <div className="absolute inset-0 bg-black/40" />
      
      {/* Logo ÚNICA - Tamanho dobrado + 15% conforme solicitado */}
      <motion.div
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="relative z-10 mb-8"
      >
        <img 
          src="/LogoTriboSite.png" 
          alt="Tribo do Cerrado" 
          className="w-80 h-80 md:w-96 md:h-96 object-contain drop-shadow-2xl"
        />
      </motion.div>

      {/* Main Content */}
      <motion.div
        initial={{ y: 50, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.8, delay: 0.3 }}
        className="relative z-10 text-center max-w-4xl mx-auto px-6"
      >
        {/* Title */}
        <h1 className="font-metal text-4xl md:text-6xl lg:text-7xl font-bold text-glow mb-4">
          TRIBO DO CERRADO
        </h1>
        
        <p className="text-xl md:text-2xl text-primary-300 mb-2 font-medium">
          Motoclube de Goiânia
        </p>
        
        <p className="text-lg text-gray-300 mb-12 max-w-2xl mx-auto">
          Unidos pela paixão das duas rodas, explorando as belezas do Cerrado brasileiro
        </p>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-6 justify-center mb-16">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/login')}
            className="btn-fire-effect text-xl px-10 py-5 flex items-center gap-3 font-bold"
          >
            <Users className="w-7 h-7" />
            ENTRAR
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => navigate('/estatuto')}
            className="btn-secondary text-xl px-10 py-5 flex items-center gap-3 font-bold"
          >
            <FileText className="w-7 h-7" />
            ESTATUTO
          </motion.button>
        </div>

        {/* Features Grid */}
        <motion.div
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto"
        >
          <div className="card-metal p-6 text-center">
            <Calendar className="w-12 h-12 text-primary-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Eventos</h3>
            <p className="text-gray-300">Trilhas, encontros e aventuras pelo Cerrado</p>
          </div>
          
          <div className="card-metal p-6 text-center">
            <Bike className="w-12 h-12 text-primary-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Comboios</h3>
            <p className="text-gray-300">Viagens organizadas com segurança e diversão</p>
          </div>
          
          <div className="card-metal p-6 text-center">
            <Mail className="w-12 h-12 text-primary-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Comunicação</h3>
            <p className="text-gray-300">Sistema integrado de mensagens e notificações</p>
          </div>
        </motion.div>
      </motion.div>

      {/* Footer */}
      <motion.footer
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8, delay: 1 }}
        className="absolute bottom-4 left-0 right-0 text-center text-gray-400 text-sm"
      >
        © 2025 Tribo do Cerrado Motoclube - Goiânia, GO
      </motion.footer>
    </div>
  );
};

export default HomePage;

