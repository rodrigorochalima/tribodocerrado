import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { Home, Calendar, User, Mail, LogOut } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const Navbar: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <motion.nav
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="bg-dark-900/95 backdrop-blur-sm border-b border-primary-500/30 sticky top-0 z-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <img 
              src="/LogoTriboSite.png" 
              alt="Tribo do Cerrado" 
              className="w-10 h-10 object-contain"
            />
            <span className="ml-3 text-xl font-metal font-bold text-glow">
              Tribo do Cerrado
            </span>
          </div>

          {/* Menu de navegação */}
          <div className="hidden md:block">
            <div className="ml-10 flex items-baseline space-x-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="nav-link flex items-center gap-2"
              >
                <Home className="w-4 h-4" />
                Dashboard
              </button>
              
              <button
                onClick={() => navigate('/eventos')}
                className="nav-link flex items-center gap-2"
              >
                <Calendar className="w-4 h-4" />
                Eventos
              </button>
              
              <button
                onClick={() => navigate('/perfil')}
                className="nav-link flex items-center gap-2"
              >
                <User className="w-4 h-4" />
                Perfil
              </button>
              
              <button
                onClick={() => navigate('/email')}
                className="nav-link flex items-center gap-2"
              >
                <Mail className="w-4 h-4" />
                E-mail
              </button>
            </div>
          </div>

          {/* Usuário e logout */}
          <div className="flex items-center gap-4">
            <span className="text-gray-300 text-sm">
              Olá, {user?.nome || 'Usuário'}
            </span>
            <button
              onClick={handleLogout}
              className="nav-link flex items-center gap-2 text-red-400 hover:text-red-300"
            >
              <LogOut className="w-4 h-4" />
              Sair
            </button>
          </div>
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;

