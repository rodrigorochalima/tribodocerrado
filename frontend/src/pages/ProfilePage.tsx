import React from 'react';
import { motion } from 'framer-motion';

const ProfilePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="text-3xl font-metal font-bold text-glow mb-8">
            Perfil
          </h1>
          <div className="card-metal p-8 text-center">
            <p className="text-gray-300">Página de perfil em desenvolvimento...</p>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default ProfilePage;

