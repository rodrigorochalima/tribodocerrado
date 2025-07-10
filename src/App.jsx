import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import { supabase } from './lib/supabase'
import './App.css'

// Componentes das páginas
import Login from './components/Login'
import Dashboard from './components/Dashboard'
import Cadastro from './components/Cadastro'
import PaginaPublica from './components/PaginaPublica'

function App() {
  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Verificar sessão atual
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setLoading(false)
    })

    // Escutar mudanças na autenticação
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
    })

    return () => subscription.unsubscribe()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-900 via-red-900 to-black flex items-center justify-center">
        <div className="text-white text-xl">Carregando...</div>
      </div>
    )
  }

  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-orange-900 via-red-900 to-black">
        <Routes>
          {/* Página pública */}
          <Route path="/" element={<PaginaPublica />} />
          
          {/* Páginas de autenticação */}
          <Route 
            path="/login" 
            element={session ? <Navigate to="/dashboard" /> : <Login />} 
          />
          <Route 
            path="/cadastro" 
            element={session ? <Navigate to="/dashboard" /> : <Cadastro />} 
          />
          
          {/* Dashboard protegido */}
          <Route 
            path="/dashboard/*" 
            element={session ? <Dashboard session={session} /> : <Navigate to="/login" />} 
          />
          
          {/* Redirecionar rotas não encontradas */}
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

