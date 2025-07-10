import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Input } from '../ui/input'
import { Label } from '../ui/label'
import { Alert, AlertDescription } from '../ui/alert'
import { 
  Users, 
  Calendar, 
  BookOpen, 
  Camera, 
  Settings, 
  Plus,
  Edit,
  Trash2,
  Save,
  X
} from 'lucide-react'
import { database } from '../../lib/supabase'

export default function DashboardAdmin({ usuario }) {
  const [secaoAtiva, setSecaoAtiva] = useState('usuarios')
  const [usuarios, setUsuarios] = useState([])
  const [eventos, setEventos] = useState([])
  const [historias, setHistorias] = useState([])
  const [fotos, setFotos] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [editando, setEditando] = useState(null)
  const [novoItem, setNovoItem] = useState({})

  useEffect(() => {
    carregarDados()
  }, [secaoAtiva])

  const carregarDados = async () => {
    setLoading(true)
    setError('')
    
    try {
      switch (secaoAtiva) {
        case 'usuarios':
          const usersResult = await database.getUsers()
          if (usersResult.success) {
            setUsuarios(usersResult.data)
          } else {
            setError('Erro ao carregar usuários: ' + usersResult.error)
          }
          break
          
        case 'eventos':
          const eventsResult = await database.getEvents()
          if (eventsResult.success) {
            setEventos(eventsResult.data)
          } else {
            setError('Erro ao carregar eventos: ' + eventsResult.error)
          }
          break
          
        case 'historias':
          const storiesResult = await database.getStories()
          if (storiesResult.success) {
            setHistorias(storiesResult.data)
          } else {
            setError('Erro ao carregar histórias: ' + storiesResult.error)
          }
          break
          
        case 'fotos':
          const photosResult = await database.getPhotos()
          if (photosResult.success) {
            setFotos(photosResult.data)
          } else {
            setError('Erro ao carregar fotos: ' + photosResult.error)
          }
          break
      }
    } catch (err) {
      setError('Erro inesperado: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id, tipo) => {
    if (!confirm('Tem certeza que deseja excluir este item?')) return
    
    setLoading(true)
    try {
      let result
      switch (tipo) {
        case 'usuario':
          result = await database.deleteUser(id)
          break
        case 'evento':
          result = await database.deleteEvent(id)
          break
        default:
          setError('Tipo de exclusão não implementado')
          return
      }
      
      if (result.success) {
        setSuccess('Item excluído com sucesso!')
        carregarDados()
      } else {
        setError('Erro ao excluir: ' + result.error)
      }
    } catch (err) {
      setError('Erro inesperado: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async (item, tipo) => {
    setLoading(true)
    try {
      let result
      
      if (item.id) {
        // Atualizar
        switch (tipo) {
          case 'usuario':
            result = await database.updateUser(item.id, item)
            break
          case 'evento':
            result = await database.updateEvent(item.id, item)
            break
        }
      } else {
        // Criar novo
        switch (tipo) {
          case 'usuario':
            result = await database.createUser(item)
            break
          case 'evento':
            result = await database.createEvent(item)
            break
          case 'historia':
            result = await database.createStory(item)
            break
          case 'foto':
            result = await database.createPhoto(item)
            break
        }
      }
      
      if (result.success) {
        setSuccess(item.id ? 'Item atualizado com sucesso!' : 'Item criado com sucesso!')
        setEditando(null)
        setNovoItem({})
        carregarDados()
      } else {
        setError('Erro ao salvar: ' + result.error)
      }
    } catch (err) {
      setError('Erro inesperado: ' + err.message)
    } finally {
      setLoading(false)
    }
  }

  const secoes = [
    { id: 'usuarios', nome: 'Usuários', icon: Users },
    { id: 'eventos', nome: 'Eventos', icon: Calendar },
    { id: 'historias', nome: 'Histórias', icon: BookOpen },
    { id: 'fotos', nome: 'Fotos', icon: Camera },
    { id: 'configuracoes', nome: 'Configurações', icon: Settings }
  ]

  const renderUsuarios = () => (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Gestão de Usuários</h3>
        <Button 
          onClick={() => setEditando('novo')}
          className="bg-green-500 hover:bg-green-600"
        >
          <Plus className="w-4 h-4 mr-2" />
          Novo Usuário
        </Button>
      </div>

      {editando === 'novo' && (
        <Card>
          <CardHeader>
            <CardTitle>Novo Usuário</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Nome</Label>
                <Input
                  value={novoItem.nome || ''}
                  onChange={(e) => setNovoItem({...novoItem, nome: e.target.value})}
                  placeholder="Nome completo"
                />
              </div>
              <div>
                <Label>Email</Label>
                <Input
                  value={novoItem.email || ''}
                  onChange={(e) => setNovoItem({...novoItem, email: e.target.value})}
                  placeholder="email@exemplo.com"
                />
              </div>
              <div>
                <Label>Telefone</Label>
                <Input
                  value={novoItem.telefone || ''}
                  onChange={(e) => setNovoItem({...novoItem, telefone: e.target.value})}
                  placeholder="(62) 99999-9999"
                />
              </div>
              <div>
                <Label>Tipo</Label>
                <select 
                  className="w-full p-2 border rounded"
                  value={novoItem.tipo || 'membro'}
                  onChange={(e) => setNovoItem({...novoItem, tipo: e.target.value})}
                >
                  <option value="membro">Membro</option>
                  <option value="admin">Administrador</option>
                  <option value="moderador">Moderador</option>
                </select>
              </div>
            </div>
            <div className="flex gap-2">
              <Button 
                onClick={() => handleSave(novoItem, 'usuario')}
                disabled={loading}
              >
                <Save className="w-4 h-4 mr-2" />
                Salvar
              </Button>
              <Button 
                variant="outline"
                onClick={() => {setEditando(null); setNovoItem({})}}
              >
                <X className="w-4 h-4 mr-2" />
                Cancelar
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4">
        {usuarios.map((user) => (
          <Card key={user.id}>
            <CardContent className="p-4">
              <div className="flex justify-between items-center">
                <div>
                  <h4 className="font-semibold">{user.nome}</h4>
                  <p className="text-sm text-gray-600">{user.email}</p>
                  <p className="text-sm text-gray-500">
                    {user.tipo} • {user.status}
                  </p>
                </div>
                <div className="flex gap-2">
                  <Button 
                    size="sm" 
                    variant="outline"
                    onClick={() => setEditando(user.id)}
                  >
                    <Edit className="w-4 h-4" />
                  </Button>
                  <Button 
                    size="sm" 
                    variant="destructive"
                    onClick={() => handleDelete(user.id, 'usuario')}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )

  const renderEventos = () => (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Gestão de Eventos</h3>
        <Button 
          onClick={() => setEditando('novo')}
          className="bg-blue-500 hover:bg-blue-600"
        >
          <Plus className="w-4 h-4 mr-2" />
          Novo Evento
        </Button>
      </div>

      {editando === 'novo' && (
        <Card>
          <CardHeader>
            <CardTitle>Novo Evento</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <Label>Título</Label>
                <Input
                  value={novoItem.titulo || ''}
                  onChange={(e) => setNovoItem({...novoItem, titulo: e.target.value})}
                  placeholder="Título do evento"
                />
              </div>
              <div>
                <Label>Data</Label>
                <Input
                  type="date"
                  value={novoItem.data_evento || ''}
                  onChange={(e) => setNovoItem({...novoItem, data_evento: e.target.value})}
                />
              </div>
              <div className="col-span-2">
                <Label>Descrição</Label>
                <textarea
                  className="w-full p-2 border rounded"
                  rows="3"
                  value={novoItem.descricao || ''}
                  onChange={(e) => setNovoItem({...novoItem, descricao: e.target.value})}
                  placeholder="Descrição do evento"
                />
              </div>
              <div>
                <Label>Local</Label>
                <Input
                  value={novoItem.local || ''}
                  onChange={(e) => setNovoItem({...novoItem, local: e.target.value})}
                  placeholder="Local do evento"
                />
              </div>
              <div>
                <Label>Horário</Label>
                <Input
                  type="time"
                  value={novoItem.horario || ''}
                  onChange={(e) => setNovoItem({...novoItem, horario: e.target.value})}
                />
              </div>
            </div>
            <div className="flex gap-2">
              <Button 
                onClick={() => handleSave(novoItem, 'evento')}
                disabled={loading}
              >
                <Save className="w-4 h-4 mr-2" />
                Salvar
              </Button>
              <Button 
                variant="outline"
                onClick={() => {setEditando(null); setNovoItem({})}}
              >
                <X className="w-4 h-4 mr-2" />
                Cancelar
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      <div className="grid gap-4">
        {eventos.map((evento) => (
          <Card key={evento.id}>
            <CardContent className="p-4">
              <div className="flex justify-between items-center">
                <div>
                  <h4 className="font-semibold">{evento.titulo}</h4>
                  <p className="text-sm text-gray-600">
                    {new Date(evento.data_evento).toLocaleDateString('pt-BR')} • {evento.horario}
                  </p>
                  <p className="text-sm text-gray-500">{evento.local}</p>
                </div>
                <div className="flex gap-2">
                  <Button 
                    size="sm" 
                    variant="outline"
                    onClick={() => setEditando(evento.id)}
                  >
                    <Edit className="w-4 h-4" />
                  </Button>
                  <Button 
                    size="sm" 
                    variant="destructive"
                    onClick={() => handleDelete(evento.id, 'evento')}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )

  const renderConteudo = () => {
    if (loading) {
      return (
        <div className="text-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-yellow-500 mx-auto"></div>
          <p className="mt-2 text-gray-600">Carregando...</p>
        </div>
      )
    }

    switch (secaoAtiva) {
      case 'usuarios':
        return renderUsuarios()
      case 'eventos':
        return renderEventos()
      case 'historias':
        return <div className="text-center py-8 text-gray-500">Gestão de histórias em desenvolvimento</div>
      case 'fotos':
        return <div className="text-center py-8 text-gray-500">Gestão de fotos em desenvolvimento</div>
      case 'configuracoes':
        return <div className="text-center py-8 text-gray-500">Configurações em desenvolvimento</div>
      default:
        return renderUsuarios()
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Settings className="w-5 h-5" />
            Painel Administrativo
          </CardTitle>
          <CardDescription>
            Gerencie usuários, eventos e configurações do sistema
          </CardDescription>
        </CardHeader>
      </Card>

      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {success && (
        <Alert className="border-green-500 text-green-700">
          <AlertDescription>{success}</AlertDescription>
        </Alert>
      )}

      <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
        {/* Menu lateral */}
        <div className="md:col-span-1">
          <Card>
            <CardContent className="p-0">
              <nav className="space-y-1">
                {secoes.map((secao) => {
                  const Icon = secao.icon
                  return (
                    <button
                      key={secao.id}
                      onClick={() => setSecaoAtiva(secao.id)}
                      className={`w-full text-left px-4 py-3 text-sm font-medium rounded-none transition-colors flex items-center gap-2 ${
                        secaoAtiva === secao.id
                          ? 'bg-yellow-50 text-yellow-700 border-r-2 border-yellow-500'
                          : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                      {secao.nome}
                    </button>
                  )
                })}
              </nav>
            </CardContent>
          </Card>
        </div>

        {/* Conteúdo principal */}
        <div className="md:col-span-4">
          <Card>
            <CardContent className="p-6">
              {renderConteudo()}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

