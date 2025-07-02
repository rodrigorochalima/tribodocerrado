import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Eye, EyeOff, Mail, Lock } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      await login(formData.email, formData.password);
      navigate('/dashboard');
    } catch (err) {
      setError('Email ou senha incorretos');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden">
      {/* Background Image - Integral */}
      <div 
        className="absolute inset-0 bg-cover bg-center bg-no-repeat"
        style={{
          backgroundImage: `url('/FundoSIte.png')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundRepeat: 'no-repeat'
        }}
      />
      
      {/* Overlay escuro */}
      <div className="absolute inset-0 bg-black/60" />

      {/* Botão Voltar */}
      <motion.button
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.5 }}
        onClick={() => navigate('/')}
        className="absolute top-6 left-6 z-20 flex items-center gap-2 text-white hover:text-primary-400 transition-colors duration-300"
      >
        <ArrowLeft className="w-6 h-6" />
        <span className="text-lg font-medium">Voltar</span>
      </motion.button>

      {/* Formulário de Login */}
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.6 }}
        className="relative z-10 w-full max-w-md mx-4"
      >
        <div className="card-metal p-8">
          {/* Logo pequena no formulário */}
          <div className="text-center mb-8">
            <img 
              src="/LogoTriboSite.png" 
              alt="Tribo do Cerrado" 
              className="w-20 h-20 mx-auto mb-4 object-contain"
            />
            <h2 className="text-2xl font-metal font-bold text-glow">
              Fazer Login
            </h2>
            <p className="text-gray-300 mt-2">
              Entre na sua conta do motoclube
            </p>
          </div>

          {/* Formulário */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-red-500/20 border border-red-500/50 rounded-lg p-3 text-red-300 text-center"
              >
                {error}
              </motion.div>
            )}

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                E-mail
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="input-metal w-full pl-10"
                  placeholder="seu@email.com"
                />
              </div>
            </div>

            {/* Senha */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Senha
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  className="input-metal w-full pl-10 pr-10"
                  placeholder="Sua senha"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {/* Esqueci a senha */}
            <div className="text-right">
              <button
                type="button"
                onClick={() => navigate('/esqueci-senha')}
                className="text-primary-400 hover:text-primary-300 text-sm transition-colors duration-300"
              >
                Esqueci minha senha
              </button>
            </div>

            {/* Botão de Login */}
            <motion.button
              type="submit"
              disabled={isLoading}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="w-full btn-fire-effect text-lg py-4 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Entrando...' : 'ENTRAR'}
            </motion.button>

            {/* Link para cadastro */}
            <div className="text-center pt-4 border-t border-gray-600">
              <p className="text-gray-300">
                Não tem conta?{' '}
                <button
                  type="button"
                  onClick={() => navigate('/register')}
                  className="text-primary-400 hover:text-primary-300 font-medium transition-colors duration-300"
                >
                  Criar cadastro
                </button>
              </p>
            </div>
          </form>
        </div>
      </motion.div>
    </div>
  );
};

export default LoginPage;

