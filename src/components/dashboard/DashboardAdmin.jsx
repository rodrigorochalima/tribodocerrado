import { useState, useEffect } from 'react'
import { supabase } from '../../lib/supabase'
import { uploadImageToCloudinary } from '../../lib/cloudinary'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Input } from '../ui/input'
import { Textarea } from '../ui/textarea'
import { Label } from '../ui/label'
import { Alert, AlertDescription } from '../ui/alert'
import { Badge } from '../ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar'
import { 
  Users, 
  Calendar, 
  BookOpen, 
  Camera, 
  Plus, 
  Edit, 
  Trash2, 
  Save,
  X,
  Search,
  Filter,
  Upload,
  Eye,
  Settings
} from 'lucide-react'

export default function DashboardAdmin({ usuario }) {
  const [abaAtiva, setAbaAtiva] = useState('usuarios')
  const [usuarios, setUsuarios] = useState([])
  const [eventos, setEventos] = useState([])
  const [historias, setHistorias] = useState([])
  const [fotos, setFotos] = useState([])
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })
  const [modalAberto, setModalAberto] = useState(false)
  const [itemEditando, setItemEditando] = useState(null)
  const [filtro, setFiltro] = useState('')

  // Estados para formulários
  const [novoUsuario, setNovoUsuario] = useState({
    nome: '',
    email: '',
    telefone: '',
    tipo: 'membro'
  })
  const [novoEvento, setNovoEvento] = useState({
    titulo: '',
    descricao: '',
    data_evento: '',
    local: '',
    max_participantes: ''
  })
  const [novaHistoria, setNovaHistoria] = useState({
    titulo: '',
    conteudo: '',
    tags: ''
  })

  useEffect(() => {
    carregarDados()
  }, [abaAtiva])

  const carregarDados = async () => {
    setLoading(true)
    try {
      switch (abaAtiva) {
        case 'usuarios':
          await carregarUsuarios()
          break
        case 'eventos':
          await carregarEventos()
          break
        case 'historias':
          await carregarHistorias()
          break
        case 'fotos':
          await carregarFotos()
          break
      }
    } catch (error) {
      console.error('Erro ao carregar dados:', error)
    } finally {
      setLoading(false)
    }
  }

  const carregarUsuarios = async () => {
    const { data, error } = await supabase
      .from('usuarios')
      .select('*')
      .order('created_at', { ascending: false })

    if (error) {
      setMessage({ type: 'error', text: 'Erro ao carregar usuários' })
    } else {
      setUsuarios(data || [])
    }
  }

  const carregarEventos = async () => {
    const { data, error } = await supabase
      .from('eventos')
      .select('*')
      .order('data_evento', { ascending: false })

    if (error) {
      setMessage({ type: 'error', text: 'Erro ao carregar eventos' })
    } else {
      setEventos(data || [])
    }
  }

  const carregarHistorias = async () => {
    const { data, error } = await supabase
      .from('historias')
      .select('*, usuarios(nome)')
      .order('created_at', { ascending: false })

    if (error) {
      setMessage({ type: 'error', text: 'Erro ao carregar histórias' })
    } else {
      setHistorias(data || [])
    }
  }

  const carregarFotos = async () => {
    const { data, error } = await supabase
      .from('fotos')
      .select('*, usuarios(nome), eventos(titulo)')
      .order('created_at', { ascending: false })

    if (error) {
      setMessage({ type: 'error', text: 'Erro ao carregar fotos' })
    } else {
      setFotos(data || [])
    }
  }

  const excluirUsuario = async (id) => {
    if (!confirm('Tem certeza que deseja excluir este usuário?')) return

    const { error } = await supabase
      .from('usuarios')
      .delete()
      .eq('id', id)

    if (error) {
      setMessage({ type: 'error', text: 'Erro ao excluir usuário' })
    } else {
      setMessage({ type: 'success', text: 'Usuário excluído com sucesso' })
      carregarUsuarios()
    }
  }

  const excluirEvento = async (id) => {
    if (!confirm('Tem certeza que deseja excluir este evento?')) return

    const { error } = await supabase
      .from('eventos')
      .delete()
      .eq('id', id)

    if (error) {
      setMessage({ type: 'error', text: 'Erro ao excluir evento' })
    } else {
      setMessage({ type: 'success', text: 'Evento excluído com sucesso' })
      carregarEventos()
    }
  }

  const excluirHistoria = async (id) => {
    if (!confirm('Tem certeza que deseja excluir esta história?')) return

    const { error } = await supabase
      .from('historias')
      .delete()
      .eq('id', id)

    if (error) {
      setMessage({ type: 'error', text: 'Erro ao excluir história' })
    } else {
      setMessage({ type: 'success', text: 'História excluída com sucesso' })
      carregarHistorias()
    }
  }

  const salvarEvento = async () => {
    setLoading(true)
    try {
      const { error } = await supabase
        .from('eventos')
        .insert([{
          ...novoEvento,
          max_participantes: novoEvento.max_participantes ? parseInt(novoEvento.max_participantes) : null,
          criado_por: usuario.id
        }])

      if (error) {
        setMessage({ type: 'error', text: 'Erro ao criar evento' })
      } else {
        setMessage({ type: 'success', text: 'Evento criado com sucesso' })
        setModalAberto(false)
        setNovoEvento({ titulo: '', descricao: '', data_evento: '', local: '', max_participantes: '' })
        carregarEventos()
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Erro inesperado' })
    } finally {
      setLoading(false)
    }
  }

  const salvarHistoria = async () => {
    setLoading(true)
    try {
      const { error } = await supabase
        .from('historias')
        .insert([{
          ...novaHistoria,
          autor_id: usuario.id
        }])

      if (error) {
        setMessage({ type: 'error', text: 'Erro ao criar história' })
      } else {
        setMessage({ type: 'success', text: 'História criada com sucesso' })
        setModalAberto(false)
        setNovaHistoria({ titulo: '', conteudo: '', tags: '' })
        carregarHistorias()
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Erro inesperado' })
    } finally {
      setLoading(false)
    }
  }

  const formatarData = (dataString) => {
    return new Date(dataString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const abas = [
    { id: 'usuarios', nome: 'Usuários', icon: Users },
    { id: 'eventos', nome: 'Eventos', icon: Calendar },
    { id: 'historias', nome: 'Histórias', icon: BookOpen },
    { id: 'fotos', nome: 'Fotos', icon: Camera }
  ]

  const dadosFiltrados = () => {
    let dados = []
    switch (abaAtiva) {
      case 'usuarios':
        dados = usuarios
        break
      case 'eventos':
        dados = eventos
        break
      case 'historias':
        dados = historias
        break
      case 'fotos':
        dados = fotos
        break
    }

    if (!filtro) return dados

    return dados.filter(item => {
      const texto = JSON.stringify(item).toLowerCase()
      return texto.includes(filtro.toLowerCase())
    })
  }

  return (
    <div className="space-y-6">
      {/* Cabeçalho */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">
            Painel Administrativo
          </h1>
          <p className="text-orange-200">
            Gerencie usuários, eventos, histórias e fotos do motoclube
          </p>
        </div>
        <Button 
          onClick={() => setModalAberto(true)}
          className="bg-orange-600 hover:bg-orange-700 text-white"
        >
          <Plus className="h-4 w-4 mr-2" />
          Novo {abaAtiva === 'usuarios' ? 'Usuário' : abaAtiva === 'eventos' ? 'Evento' : abaAtiva === 'historias' ? 'História' : 'Foto'}
        </Button>
      </div>

      {/* Mensagens */}
      {message.text && (
        <Alert className={`${message.type === 'error' ? 'border-red-500/50 bg-red-500/10' : 'border-green-500/50 bg-green-500/10'}`}>
          <AlertDescription className={message.type === 'error' ? 'text-red-200' : 'text-green-200'}>
            {message.text}
          </AlertDescription>
        </Alert>
      )}

      {/* Navegação das Abas */}
      <div className="flex space-x-1 bg-black/30 p-1 rounded-lg">
        {abas.map((aba) => {
          const Icon = aba.icon
          return (
            <button
              key={aba.id}
              onClick={() => setAbaAtiva(aba.id)}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md transition-colors ${
                abaAtiva === aba.id
                  ? 'bg-orange-600 text-white'
                  : 'text-orange-200 hover:bg-orange-500/20 hover:text-white'
              }`}
            >
              <Icon className="h-4 w-4" />
              <span>{aba.nome}</span>
            </button>
          )
        })}
      </div>

      {/* Filtros */}
      <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
        <CardContent className="pt-6">
          <div className="flex items-center space-x-4">
            <div className="flex-1">
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-orange-400" />
                <Input
                  placeholder={`Buscar ${abaAtiva}...`}
                  value={filtro}
                  onChange={(e) => setFiltro(e.target.value)}
                  className="pl-10 bg-black/30 border-orange-500/30 text-white"
                />
              </div>
            </div>
            <Button variant="outline" className="border-orange-500/50 text-orange-400 hover:bg-orange-500 hover:text-white">
              <Filter className="h-4 w-4 mr-2" />
              Filtros
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Conteúdo das Abas */}
      <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-white">
            {abas.find(a => a.id === abaAtiva)?.nome} ({dadosFiltrados().length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="flex items-center justify-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-400"></div>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Lista de Usuários */}
              {abaAtiva === 'usuarios' && (
                <div className="space-y-3">
                  {dadosFiltrados().map((user) => (
                    <div key={user.id} className="flex items-center justify-between p-4 bg-orange-500/10 rounded-lg border border-orange-500/20">
                      <div className="flex items-center space-x-4">
                        <Avatar>
                          <AvatarImage src={user.foto_url} />
                          <AvatarFallback className="bg-orange-600 text-white">
                            {user.nome?.charAt(0)}
                          </AvatarFallback>
                        </Avatar>
                        <div>
                          <h4 className="text-white font-medium">{user.nome}</h4>
                          <p className="text-orange-200 text-sm">{user.email}</p>
                          <div className="flex items-center space-x-2 mt-1">
                            <Badge variant={user.tipo === 'admin' ? 'default' : 'secondary'}>
                              {user.tipo}
                            </Badge>
                            <Badge variant={user.ativo ? 'default' : 'destructive'}>
                              {user.ativo ? 'Ativo' : 'Inativo'}
                            </Badge>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        <Button variant="ghost" size="sm" className="text-orange-400 hover:text-white">
                          <Edit className="h-4 w-4" />
                        </Button>
                        <Button 
                          variant="ghost" 
                          size="sm" 
                          className="text-red-400 hover:text-white"
                          onClick={() => excluirUsuario(user.id)}
                        >
                          <Trash2 className="h-4 w-4" />
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Lista de Eventos */}
              {abaAtiva === 'eventos' && (
                <div className="space-y-3">
                  {dadosFiltrados().map((evento) => (
                    <div key={evento.id} className="p-4 bg-orange-500/10 rounded-lg border border-orange-500/20">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className="text-white font-medium text-lg">{evento.titulo}</h4>
                          <p className="text-orange-200 text-sm mt-1">{evento.descricao}</p>
                          <div className="flex items-center space-x-4 mt-3 text-xs text-orange-300">
                            <span>📅 {formatarData(evento.data_evento)}</span>
                            {evento.local && <span>📍 {evento.local}</span>}
                            {evento.max_participantes && <span>👥 Máx: {evento.max_participantes}</span>}
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Button variant="ghost" size="sm" className="text-orange-400 hover:text-white">
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm" className="text-orange-400 hover:text-white">
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button 
                            variant="ghost" 
                            size="sm" 
                            className="text-red-400 hover:text-white"
                            onClick={() => excluirEvento(evento.id)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Lista de Histórias */}
              {abaAtiva === 'historias' && (
                <div className="space-y-3">
                  {dadosFiltrados().map((historia) => (
                    <div key={historia.id} className="p-4 bg-orange-500/10 rounded-lg border border-orange-500/20">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h4 className="text-white font-medium text-lg">{historia.titulo}</h4>
                          <p className="text-orange-200 text-sm mt-1 line-clamp-2">{historia.conteudo}</p>
                          <div className="flex items-center space-x-4 mt-3 text-xs text-orange-300">
                            <span>✍️ {historia.usuarios?.nome}</span>
                            <span>📅 {formatarData(historia.created_at)}</span>
                            {historia.tags && <span>🏷️ {historia.tags}</span>}
                          </div>
                        </div>
                        <div className="flex items-center space-x-2">
                          <Button variant="ghost" size="sm" className="text-orange-400 hover:text-white">
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button variant="ghost" size="sm" className="text-orange-400 hover:text-white">
                            <Edit className="h-4 w-4" />
                          </Button>
                          <Button 
                            variant="ghost" 
                            size="sm" 
                            className="text-red-400 hover:text-white"
                            onClick={() => excluirHistoria(historia.id)}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Lista de Fotos */}
              {abaAtiva === 'fotos' && (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {dadosFiltrados().map((foto) => (
                    <div key={foto.id} className="bg-orange-500/10 rounded-lg border border-orange-500/20 overflow-hidden">
                      <img 
                        src={foto.url} 
                        alt={foto.descricao}
                        className="w-full h-48 object-cover"
                      />
                      <div className="p-3">
                        <p className="text-white text-sm font-medium">{foto.descricao}</p>
                        <div className="flex items-center justify-between mt-2 text-xs text-orange-300">
                          <span>{foto.usuarios?.nome}</span>
                          <span>{formatarData(foto.created_at)}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {dadosFiltrados().length === 0 && (
                <div className="text-center py-8">
                  <p className="text-orange-200">Nenhum item encontrado</p>
                </div>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Modal para Criar/Editar */}
      {modalAberto && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="bg-black/90 border-orange-500/30 backdrop-blur-sm w-full max-w-2xl max-h-[90vh] overflow-y-auto">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-white">
                  Novo {abaAtiva === 'eventos' ? 'Evento' : abaAtiva === 'historias' ? 'História' : 'Item'}
                </CardTitle>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={() => setModalAberto(false)}
                  className="text-orange-400 hover:text-white"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Formulário de Evento */}
              {abaAtiva === 'eventos' && (
                <>
                  <div>
                    <Label className="text-white">Título do Evento</Label>
                    <Input
                      value={novoEvento.titulo}
                      onChange={(e) => setNovoEvento({...novoEvento, titulo: e.target.value})}
                      className="mt-1 bg-black/30 border-orange-500/30 text-white"
                    />
                  </div>
                  <div>
                    <Label className="text-white">Descrição</Label>
                    <Textarea
                      value={novoEvento.descricao}
                      onChange={(e) => setNovoEvento({...novoEvento, descricao: e.target.value})}
                      rows={3}
                      className="mt-1 bg-black/30 border-orange-500/30 text-white"
                    />
                  </div>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <Label className="text-white">Data e Hora</Label>
                      <Input
                        type="datetime-local"
                        value={novoEvento.data_evento}
                        onChange={(e) => setNovoEvento({...novoEvento, data_evento: e.target.value})}
                        className="mt-1 bg-black/30 border-orange-500/30 text-white"
                      />
                    </div>
                    <div>
                      <Label className="text-white">Máx. Participantes</Label>
                      <Input
                        type="number"
                        value={novoEvento.max_participantes}
                        onChange={(e) => setNovoEvento({...novoEvento, max_participantes: e.target.value})}
                        className="mt-1 bg-black/30 border-orange-500/30 text-white"
                      />
                    </div>
                  </div>
                  <div>
                    <Label className="text-white">Local</Label>
                    <Input
                      value={novoEvento.local}
                      onChange={(e) => setNovoEvento({...novoEvento, local: e.target.value})}
                      className="mt-1 bg-black/30 border-orange-500/30 text-white"
                    />
                  </div>
                </>
              )}

              {/* Formulário de História */}
              {abaAtiva === 'historias' && (
                <>
                  <div>
                    <Label className="text-white">Título da História</Label>
                    <Input
                      value={novaHistoria.titulo}
                      onChange={(e) => setNovaHistoria({...novaHistoria, titulo: e.target.value})}
                      className="mt-1 bg-black/30 border-orange-500/30 text-white"
                    />
                  </div>
                  <div>
                    <Label className="text-white">Conteúdo</Label>
                    <Textarea
                      value={novaHistoria.conteudo}
                      onChange={(e) => setNovaHistoria({...novaHistoria, conteudo: e.target.value})}
                      rows={8}
                      className="mt-1 bg-black/30 border-orange-500/30 text-white"
                    />
                  </div>
                  <div>
                    <Label className="text-white">Tags (separadas por vírgula)</Label>
                    <Input
                      value={novaHistoria.tags}
                      onChange={(e) => setNovaHistoria({...novaHistoria, tags: e.target.value})}
                      placeholder="aventura, viagem, motoclube"
                      className="mt-1 bg-black/30 border-orange-500/30 text-white"
                    />
                  </div>
                </>
              )}

              <div className="flex items-center justify-end space-x-3 pt-4">
                <Button 
                  variant="outline" 
                  onClick={() => setModalAberto(false)}
                  className="border-orange-500/50 text-orange-400 hover:bg-orange-500 hover:text-white"
                >
                  Cancelar
                </Button>
                <Button 
                  onClick={abaAtiva === 'eventos' ? salvarEvento : salvarHistoria}
                  disabled={loading}
                  className="bg-orange-600 hover:bg-orange-700 text-white"
                >
                  <Save className="h-4 w-4 mr-2" />
                  {loading ? 'Salvando...' : 'Salvar'}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}

