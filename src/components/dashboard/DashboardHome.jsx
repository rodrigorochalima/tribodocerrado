import { useState, useEffect } from 'react'
import { supabase } from '../../lib/supabase'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Users, Calendar, Camera, TrendingUp, Clock, MapPin } from 'lucide-react'

export default function DashboardHome({ usuario }) {
  const [stats, setStats] = useState({
    totalMembros: 0,
    eventosProximos: 0,
    fotosRecentes: 0,
    historiasRecentes: 0
  })
  const [proximosEventos, setProximosEventos] = useState([])
  const [atividadesRecentes, setAtividadesRecentes] = useState([])

  useEffect(() => {
    carregarEstatisticas()
    carregarProximosEventos()
    carregarAtividadesRecentes()
  }, [])

  const carregarEstatisticas = async () => {
    try {
      // Total de membros
      const { count: totalMembros } = await supabase
        .from('usuarios')
        .select('*', { count: 'exact', head: true })
        .eq('ativo', true)

      // Eventos próximos (próximos 30 dias)
      const dataLimite = new Date()
      dataLimite.setDate(dataLimite.getDate() + 30)
      
      const { count: eventosProximos } = await supabase
        .from('eventos')
        .select('*', { count: 'exact', head: true })
        .gte('data_evento', new Date().toISOString())
        .lte('data_evento', dataLimite.toISOString())

      // Fotos recentes (últimos 7 dias)
      const dataRecente = new Date()
      dataRecente.setDate(dataRecente.getDate() - 7)
      
      const { count: fotosRecentes } = await supabase
        .from('fotos')
        .select('*', { count: 'exact', head: true })
        .gte('created_at', dataRecente.toISOString())

      // Histórias recentes (últimos 30 dias)
      const dataHistorias = new Date()
      dataHistorias.setDate(dataHistorias.getDate() - 30)
      
      const { count: historiasRecentes } = await supabase
        .from('historias')
        .select('*', { count: 'exact', head: true })
        .gte('created_at', dataHistorias.toISOString())

      setStats({
        totalMembros: totalMembros || 0,
        eventosProximos: eventosProximos || 0,
        fotosRecentes: fotosRecentes || 0,
        historiasRecentes: historiasRecentes || 0
      })
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error)
    }
  }

  const carregarProximosEventos = async () => {
    try {
      const { data, error } = await supabase
        .from('eventos')
        .select('*')
        .gte('data_evento', new Date().toISOString())
        .order('data_evento', { ascending: true })
        .limit(3)

      if (error) {
        console.error('Erro ao carregar eventos:', error)
      } else {
        setProximosEventos(data || [])
      }
    } catch (error) {
      console.error('Erro inesperado:', error)
    }
  }

  const carregarAtividadesRecentes = async () => {
    try {
      // Simular atividades recentes (pode ser expandido para incluir logs reais)
      const atividades = [
        {
          id: 1,
          tipo: 'evento',
          descricao: 'Novo evento criado: Encontro Mensal',
          tempo: '2 horas atrás',
          icon: Calendar
        },
        {
          id: 2,
          tipo: 'membro',
          descricao: 'Novo membro se cadastrou',
          tempo: '5 horas atrás',
          icon: Users
        },
        {
          id: 3,
          tipo: 'foto',
          descricao: 'Novas fotos adicionadas à galeria',
          tempo: '1 dia atrás',
          icon: Camera
        }
      ]
      
      setAtividadesRecentes(atividades)
    } catch (error) {
      console.error('Erro ao carregar atividades:', error)
    }
  }

  const formatarData = (dataString) => {
    const data = new Date(dataString)
    return data.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="space-y-6">
      {/* Cabeçalho */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">
          Dashboard - Tribo do Cerrado MC
        </h1>
        <p className="text-orange-200">
          Bem-vindo ao sistema de gestão do motoclube. Aqui você encontra um resumo de todas as atividades.
        </p>
      </div>

      {/* Cards de Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-white">
              Total de Membros
            </CardTitle>
            <Users className="h-4 w-4 text-orange-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-400">
              {stats.totalMembros}
            </div>
            <p className="text-xs text-orange-200">
              Membros ativos no motoclube
            </p>
          </CardContent>
        </Card>

        <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-white">
              Próximos Eventos
            </CardTitle>
            <Calendar className="h-4 w-4 text-orange-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-400">
              {stats.eventosProximos}
            </div>
            <p className="text-xs text-orange-200">
              Eventos nos próximos 30 dias
            </p>
          </CardContent>
        </Card>

        <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-white">
              Fotos Recentes
            </CardTitle>
            <Camera className="h-4 w-4 text-orange-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-400">
              {stats.fotosRecentes}
            </div>
            <p className="text-xs text-orange-200">
              Fotos adicionadas esta semana
            </p>
          </CardContent>
        </Card>

        <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-white">
              Histórias Novas
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-orange-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-400">
              {stats.historiasRecentes}
            </div>
            <p className="text-xs text-orange-200">
              Histórias publicadas este mês
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Próximos Eventos */}
        <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <Calendar className="h-5 w-5 mr-2 text-orange-400" />
              Próximos Eventos
            </CardTitle>
            <CardDescription className="text-orange-200">
              Eventos programados para os próximos dias
            </CardDescription>
          </CardHeader>
          <CardContent>
            {proximosEventos.length > 0 ? (
              <div className="space-y-4">
                {proximosEventos.map((evento) => (
                  <div key={evento.id} className="flex items-start space-x-3 p-3 rounded-lg bg-orange-500/10 border border-orange-500/20">
                    <div className="flex-shrink-0">
                      <div className="w-2 h-2 bg-orange-400 rounded-full mt-2"></div>
                    </div>
                    <div className="flex-1">
                      <h4 className="text-white font-medium">{evento.titulo}</h4>
                      <p className="text-orange-200 text-sm">{evento.descricao}</p>
                      <div className="flex items-center mt-2 text-xs text-orange-300">
                        <Clock className="h-3 w-3 mr-1" />
                        {formatarData(evento.data_evento)}
                        {evento.local && (
                          <>
                            <MapPin className="h-3 w-3 ml-3 mr-1" />
                            {evento.local}
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-orange-200 text-center py-4">
                Nenhum evento programado
              </p>
            )}
          </CardContent>
        </Card>

        {/* Atividades Recentes */}
        <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <TrendingUp className="h-5 w-5 mr-2 text-orange-400" />
              Atividades Recentes
            </CardTitle>
            <CardDescription className="text-orange-200">
              Últimas atividades no sistema
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {atividadesRecentes.map((atividade) => {
                const Icon = atividade.icon
                return (
                  <div key={atividade.id} className="flex items-start space-x-3">
                    <div className="flex-shrink-0">
                      <Icon className="h-4 w-4 text-orange-400 mt-1" />
                    </div>
                    <div className="flex-1">
                      <p className="text-white text-sm">{atividade.descricao}</p>
                      <p className="text-orange-300 text-xs">{atividade.tempo}</p>
                    </div>
                  </div>
                )
              })}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Ações Rápidas */}
      <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-white">Ações Rápidas</CardTitle>
          <CardDescription className="text-orange-200">
            Acesse rapidamente as principais funcionalidades
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Button 
              className="bg-orange-600 hover:bg-orange-700 text-white"
              onClick={() => window.location.href = '/dashboard/perfil'}
            >
              <User className="h-4 w-4 mr-2" />
              Editar Perfil
            </Button>
            
            <Button 
              variant="outline"
              className="border-orange-500/50 text-orange-400 hover:bg-orange-500 hover:text-white"
              onClick={() => window.location.href = '/dashboard/email'}
            >
              <Mail className="h-4 w-4 mr-2" />
              Ver Mensagens
            </Button>
            
            {usuario?.tipo === 'admin' && (
              <Button 
                variant="outline"
                className="border-orange-500/50 text-orange-400 hover:bg-orange-500 hover:text-white"
                onClick={() => window.location.href = '/dashboard/admin'}
              >
                <Settings className="h-4 w-4 mr-2" />
                Administração
              </Button>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

