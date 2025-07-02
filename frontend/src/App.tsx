import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { motion } from 'framer-motion';
import HomePage from './pages/HomePage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import DashboardPage from './pages/DashboardPage';
import EventsPage from './pages/EventsPage';
import ProfilePage from './pages/ProfilePage';
import EmailPage from './pages/EmailPage';
import StatutePage from './pages/StatutePage';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import './index.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gradient-to-br from-dark-900 via-dark-800 to-dark-900">
          {/* Background Pattern */}
          <div className="fixed inset-0 opacity-10">
            <div className="absolute inset-0 bg-[url('data:image/svg+xml,%3Csvg width="60" height="60" viewBox="0 0 60 60" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23f97316" fill-opacity="0.1"%3E%3Ccircle cx="30" cy="30" r="2"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E')]"></div>
          </div>

          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8 }}
            className="relative z-10"
          >
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/estatuto" element={<StatutePage />} />
              
              {/* Rotas protegidas */}
              <Route path="/dashboard" element={
                <ProtectedRoute>
                  <>
                    <Navbar />
                    <DashboardPage />
                  </>
                </ProtectedRoute>
              } />
              
              <Route path="/eventos" element={
                <ProtectedRoute>
                  <>
                    <Navbar />
                    <EventsPage />
                  </>
                </ProtectedRoute>
              } />
              
              <Route path="/perfil" element={
                <ProtectedRoute>
                  <>
                    <Navbar />
                    <ProfilePage />
                  </>
                </ProtectedRoute>
              } />
              
              <Route path="/email" element={
                <ProtectedRoute>
                  <>
                    <Navbar />
                    <EmailPage />
                  </>
                </ProtectedRoute>
              } />
            </Routes>
          </motion.div>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;

