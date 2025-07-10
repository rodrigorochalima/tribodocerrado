import { useState, useEffect } from 'react'
import { Routes, Route, Link, useLocation, useNavigate } from 'react-router-dom'
import { supabase } from '../lib/supabase'
import { Button } from './ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar'
import { 
  Home, 
  Mail, 
  Settings, 
  User, 
  LogOut, 
  Users, 
  Calendar,
  Camera,
  BarChart3,
  Menu,
  X
} from 'lucide-react'

// Componentes das abas
import DashboardHome from './dashboard/DashboardHome'
import DashboardEmail from './dashboard/DashboardEmail'
import DashboardAdmin from './dashboard/DashboardAdmin'
import DashboardPerfil from './dashboard/DashboardPerfil'

export default function Dashboard({ session }) {
  const [usuario, setUsuario] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const location = useLocation()
  const navigate = useNavigate()

  useEffect(() => {
    if (session?.user) {
      carregarDadosUsuario()
    }
  }, [session])

  const carregarDadosUsuario = async () => {
    try {
      const { data, error } = await supabase
        .from('usuarios')
        .select('*')
        .eq('id', session.user.id)
        .single()

      if (error) {
        console.error('Erro ao carregar dados do usuário:', error)
      } else {
        setUsuario(data)
      }
    } catch (err) {
      console.error('Erro inesperado:', err)
    }
  }

  const handleLogout = async () => {
    await supabase.auth.signOut()
    navigate('/login')
  }

  const menuItems = [
    {
      path: '/dashboard',
      icon: Home,
      label: 'Dashboard',
      description: 'Visão geral do sistema'
    },
    {
      path: '/dashboard/email',
      icon: Mail,
      label: 'Email',
      description: 'Sistema de mensagens'
    },
    {
      path: '/dashboard/admin',
      icon: Settings,
      label: 'Administrador',
      description: 'Gestão do motoclube',
      adminOnly: true
    },
    {
      path: '/dashboard/perfil',
      icon: User,
      label: 'Perfil',
      description: 'Meus dados pessoais'
    }
  ]

  const isAdmin = usuario?.tipo === 'admin'
  const filteredMenuItems = menuItems.filter(item => !item.adminOnly || isAdmin)

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-900 via-red-900 to-black">
      <div className="flex">
        {/* Sidebar */}
        <div className={`fixed inset-y-0 left-0 z-50 w-64 bg-black/80 backdrop-blur-sm border-r border-orange-500/30 transform ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0`}>
          <div className="flex items-center justify-between h-16 px-6 border-b border-orange-500/30">
            <h1 className="text-xl font-bold text-white">Tribo do Cerrado</h1>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden text-orange-400 hover:text-orange-300"
            >
              <X className="h-6 w-6" />
            </button>
          </div>

          {/* Perfil do usuário */}
          <div className="p-6 border-b border-orange-500/30">
            <div className="flex items-center space-x-3">
              <Avatar className="h-12 w-12">
                <AvatarImage src={usuario?.foto_url} />
                <AvatarFallback className="bg-orange-600 text-white">
                  {usuario?.nome?.charAt(0) || session?.user?.email?.charAt(0)}
                </AvatarFallback>
              </Avatar>
              <div>
                <p className="text-white font-medium">
                  {usuario?.nome || 'Carregando...'}
                </p>
                <p className="text-orange-200 text-sm">
                  {usuario?.tipo === 'admin' ? 'Administrador' : 'Membro'}
                </p>
              </div>
            </div>
          </div>

          {/* Menu de navegação */}
          <nav className="flex-1 px-4 py-6 space-y-2">
            {filteredMenuItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path || 
                             (item.path === '/dashboard' && location.pathname === '/dashboard/')
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setSidebarOpen(false)}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive 
                      ? 'bg-orange-600 text-white' 
                      : 'text-orange-200 hover:bg-orange-500/20 hover:text-white'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <div>
                    <p className="font-medium">{item.label}</p>
                    <p className="text-xs opacity-75">{item.description}</p>
                  </div>
                </Link>
              )
            })}
          </nav>

          {/* Botão de logout */}
          <div className="p-4 border-t border-orange-500/30">
            <Button
              onClick={handleLogout}
              variant="outline"
              className="w-full border-orange-500/50 text-orange-400 hover:bg-orange-500 hover:text-white"
            >
              <LogOut className="h-4 w-4 mr-2" />
              Sair
            </Button>
          </div>
        </div>

        {/* Overlay para mobile */}
        {sidebarOpen && (
          <div 
            className="fixed inset-0 bg-black/50 z-40 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}

        {/* Conteúdo principal */}
        <div className="flex-1 lg:ml-0">
          {/* Header */}
          <header className="bg-black/50 backdrop-blur-sm border-b border-orange-500/30 px-6 py-4">
            <div className="flex items-center justify-between">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden text-orange-400 hover:text-orange-300"
              >
                <Menu className="h-6 w-6" />
              </button>
              
              <div className="flex items-center space-x-4">
                <div className="text-right">
                  <p className="text-white font-medium">
                    Bem-vindo, {usuario?.nome?.split(' ')[0] || 'Usuário'}!
                  </p>
                  <p className="text-orange-200 text-sm">
                    {new Date().toLocaleDateString('pt-BR', { 
                      weekday: 'long', 
                      year: 'numeric', 
                      month: 'long', 
                      day: 'numeric' 
                    })}
                  </p>
                </div>
              </div>
            </div>
          </header>

          {/* Conteúdo das páginas */}
          <main className="p-6">
            <Routes>
              <Route path="/" element={<DashboardHome usuario={usuario} />} />
              <Route path="/email" element={<DashboardEmail usuario={usuario} />} />
              {isAdmin && (
                <Route path="/admin" element={<DashboardAdmin usuario={usuario} />} />
              )}
              <Route path="/perfil" element={<DashboardPerfil usuario={usuario} session={session} onUsuarioUpdate={setUsuario} />} />
            </Routes>
          </main>
        </div>
      </div>
    </div>
  )
}

