import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Avatar, AvatarFallback, AvatarImage } from './ui/avatar'
import { auth, database } from '../lib/supabase'
import DashboardHome from './dashboard/DashboardHome'
import DashboardEmail from './dashboard/DashboardEmail'
import DashboardAdmin from './dashboard/DashboardAdmin'
import DashboardPerfil from './dashboard/DashboardPerfil'

export default function Dashboard() {
  const [abaAtiva, setAbaAtiva] = useState('dashboard')
  const [usuario, setUsuario] = useState(null)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    checkUser()
  }, [])

  const checkUser = async () => {
    try {
      const user = await auth.getCurrentUser()
      
      if (!user) {
        navigate('/login')
        return
      }

      // Buscar dados completos do usuário na tabela usuarios
      const result = await database.getUsers()
      if (result.success) {
        const userData = result.data.find(u => u.auth_id === user.id)
        if (userData) {
          setUsuario({
            ...userData,
            email: user.email
          })
        } else {
          // Usuário não encontrado na tabela, criar registro
          const newUserData = {
            nome: user.user_metadata?.nome || user.email.split('@')[0],
            email: user.email,
            telefone: user.user_metadata?.telefone || '',
            tipo: 'membro',
            status: 'ativo',
            auth_id: user.id
          }
          
          const createResult = await database.createUser(newUserData)
          if (createResult.success) {
            setUsuario(createResult.data)
          }
        }
      }
    } catch (error) {
      console.error('Erro ao verificar usuário:', error)
      navigate('/login')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = async () => {
    try {
      await auth.signOut()
      navigate('/login')
    } catch (error) {
      console.error('Erro ao fazer logout:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-yellow-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Carregando...</p>
        </div>
      </div>
    )
  }

  if (!usuario) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardContent className="text-center p-6">
            <p className="text-red-600">Erro ao carregar dados do usuário</p>
            <Button onClick={() => navigate('/login')} className="mt-4">
              Fazer Login Novamente
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  const abas = [
    { id: 'dashboard', nome: '🏠 Dashboard', icon: '🏠' },
    { id: 'email', nome: '📧 Email', icon: '📧' },
    { id: 'admin', nome: '⚙️ Administrador', icon: '⚙️' },
    { id: 'perfil', nome: '👤 Perfil', icon: '👤' }
  ]

  const renderConteudo = () => {
    switch (abaAtiva) {
      case 'dashboard':
        return <DashboardHome usuario={usuario} />
      case 'email':
        return <DashboardEmail usuario={usuario} />
      case 'admin':
        return <DashboardAdmin usuario={usuario} />
      case 'perfil':
        return <DashboardPerfil usuario={usuario} />
      default:
        return <DashboardHome usuario={usuario} />
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <img 
                src="/src/assets/LogoTriboSite.png" 
                alt="Tribo do Cerrado" 
                className="h-10 w-auto"
              />
              <h1 className="ml-3 text-xl font-bold text-gray-900">
                Tribo do Cerrado
              </h1>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <Avatar className="h-8 w-8">
                  <AvatarImage src={usuario.foto_url} />
                  <AvatarFallback>
                    {usuario.nome?.charAt(0)?.toUpperCase() || '?'}
                  </AvatarFallback>
                </Avatar>
                <span className="text-sm font-medium text-gray-700">
                  {usuario.nome}
                </span>
              </div>
              
              <Button 
                onClick={handleLogout}
                variant="outline"
                size="sm"
                className="text-red-600 hover:text-red-700 hover:bg-red-50"
              >
                🚪 Sair
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col lg:flex-row gap-8">
          {/* Sidebar */}
          <div className="lg:w-64">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Menu</CardTitle>
              </CardHeader>
              <CardContent className="p-0">
                <nav className="space-y-1">
                  {abas.map((aba) => (
                    <button
                      key={aba.id}
                      onClick={() => setAbaAtiva(aba.id)}
                      className={`w-full text-left px-4 py-3 text-sm font-medium rounded-none transition-colors ${
                        abaAtiva === aba.id
                          ? 'bg-yellow-50 text-yellow-700 border-r-2 border-yellow-500'
                          : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                      }`}
                    >
                      <span className="mr-3">{aba.icon}</span>
                      {aba.nome}
                    </button>
                  ))}
                </nav>
              </CardContent>
            </Card>
          </div>

          {/* Conteúdo Principal */}
          <div className="flex-1">
            {renderConteudo()}
          </div>
        </div>
      </div>
    </div>
  )
}

