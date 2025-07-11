import { useState, useEffect } from 'react'
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isSameDay, parseISO } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import { supabase } from '../../lib/supabase'
import { Card, CardContent, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Input } from '../ui/input'
import { Label } from '../ui/label'
import { Textarea } from '../ui/textarea'

export default function DashboardEventos() {
  const [eventos, setEventos] = useState([])
  const [selectedDate, setSelectedDate] = useState(new Date())
  const [currentMonth, setCurrentMonth] = useState(new Date())
  const [showForm, setShowForm] = useState(false)
  const [novoEvento, setNovoEvento] = useState({
    titulo: '',
    descricao: '',
    data: '',
    hora: '',
    local: '',
    max_participantes: ''
  })

  useEffect(() => {
    carregarEventos()
  }, [])

  const carregarEventos = async () => {
    try {
      const { data, error } = await supabase
        .from('eventos')
        .select('*')
        .order('data', { ascending: true })

      if (error) throw error
      setEventos(data || [])
    } catch (error) {
      console.error('Erro ao carregar eventos:', error)
    }
  }

  const criarEvento = async (e) => {
    e.preventDefault()
    try {
      const { data, error } = await supabase
        .from('eventos')
        .insert([{
          ...novoEvento,
          data: format(selectedDate, 'yyyy-MM-dd'),
          criado_por: (await supabase.auth.getUser()).data.user?.id
        }])

      if (error) throw error
      
      setNovoEvento({
        titulo: '',
        descricao: '',
        data: '',
        hora: '',
        local: '',
        max_participantes: ''
      })
      setShowForm(false)
      carregarEventos()
    } catch (error) {
      console.error('Erro ao criar evento:', error)
    }
  }

  // Gerar dias do calendário
  const monthStart = startOfMonth(currentMonth)
  const monthEnd = endOfMonth(currentMonth)
  const calendarDays = eachDayOfInterval({ start: monthStart, end: monthEnd })

  // Verificar se um dia tem eventos
  const hasEvent = (day) => {
    return eventos.some(evento => isSameDay(parseISO(evento.data), day))
  }

  const eventosProximos = eventos
    .filter(evento => new Date(evento.data) >= new Date())
    .slice(0, 5)

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold">📅 Eventos do Motoclube</h2>
        <Button onClick={() => setShowForm(!showForm)}>
          ➕ Novo Evento
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Calendário Simples */}
        <Card className="lg:col-span-1">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>📅 {format(currentMonth, 'MMMM yyyy', { locale: ptBR })}</span>
              <div className="flex gap-2">
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() - 1))}
                >
                  ←
                </Button>
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={() => setCurrentMonth(new Date(currentMonth.getFullYear(), currentMonth.getMonth() + 1))}
                >
                  →
                </Button>
              </div>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-7 gap-1 text-center text-sm">
              {['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'].map(day => (
                <div key={day} className="font-medium p-2 text-gray-500">
                  {day}
                </div>
              ))}
              
              {calendarDays.map(day => (
                <button
                  key={day.toISOString()}
                  onClick={() => setSelectedDate(day)}
                  className={`p-2 text-sm rounded hover:bg-gray-100 ${
                    isSameDay(day, selectedDate) 
                      ? 'bg-blue-500 text-white' 
                      : hasEvent(day)
                      ? 'bg-red-100 text-red-700 font-bold'
                      : 'text-gray-700'
                  }`}
                >
                  {format(day, 'd')}
                </button>
              ))}
            </div>
            
            <div className="mt-4 text-sm text-gray-600">
              <div className="flex items-center gap-4">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-red-100 border border-red-300 rounded mr-2"></div>
                  Dias com eventos
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-blue-500 rounded mr-2"></div>
                  Selecionado
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Lista de Eventos */}
        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>🏍️ Próximos Eventos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {eventosProximos.length === 0 ? (
                <p className="text-gray-500 text-center py-8">
                  Nenhum evento agendado
                </p>
              ) : (
                eventosProximos.map((evento) => (
                  <div key={evento.id} className="border rounded-lg p-4 hover:bg-gray-50">
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <h3 className="font-semibold text-lg">{evento.titulo}</h3>
                        <p className="text-gray-600 mt-1">{evento.descricao}</p>
                        
                        <div className="flex flex-wrap gap-4 mt-3 text-sm text-gray-500">
                          <div className="flex items-center">
                            📅 {format(parseISO(evento.data), 'dd/MM/yyyy', { locale: ptBR })}
                          </div>
                          
                          {evento.hora && (
                            <div className="flex items-center">
                              🕐 {evento.hora}
                            </div>
                          )}
                          
                          {evento.local && (
                            <div className="flex items-center">
                              📍 {evento.local}
                            </div>
                          )}
                          
                          {evento.max_participantes && (
                            <div className="flex items-center">
                              👥 Máx: {evento.max_participantes}
                            </div>
                          )}
                        </div>
                      </div>
                      
                      <span className={`px-2 py-1 text-xs rounded ${
                        new Date(evento.data) > new Date() 
                          ? 'bg-green-100 text-green-700' 
                          : 'bg-gray-100 text-gray-700'
                      }`}>
                        {new Date(evento.data) > new Date() ? 'Agendado' : 'Realizado'}
                      </span>
                    </div>
                  </div>
                ))
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Formulário de Novo Evento */}
      {showForm && (
        <Card>
          <CardHeader>
            <CardTitle>➕ Criar Novo Evento</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={criarEvento} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="titulo">Título do Evento</Label>
                  <Input
                    id="titulo"
                    value={novoEvento.titulo}
                    onChange={(e) => setNovoEvento({...novoEvento, titulo: e.target.value})}
                    placeholder="Ex: Encontro Mensal"
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="data">Data</Label>
                  <Input
                    id="data"
                    type="date"
                    value={format(selectedDate, 'yyyy-MM-dd')}
                    onChange={(e) => setSelectedDate(new Date(e.target.value))}
                    required
                  />
                </div>
                
                <div>
                  <Label htmlFor="hora">Horário</Label>
                  <Input
                    id="hora"
                    type="time"
                    value={novoEvento.hora}
                    onChange={(e) => setNovoEvento({...novoEvento, hora: e.target.value})}
                  />
                </div>
                
                <div>
                  <Label htmlFor="local">Local</Label>
                  <Input
                    id="local"
                    value={novoEvento.local}
                    onChange={(e) => setNovoEvento({...novoEvento, local: e.target.value})}
                    placeholder="Ex: Praça Central"
                  />
                </div>
                
                <div>
                  <Label htmlFor="max_participantes">Máx. Participantes</Label>
                  <Input
                    id="max_participantes"
                    type="number"
                    value={novoEvento.max_participantes}
                    onChange={(e) => setNovoEvento({...novoEvento, max_participantes: e.target.value})}
                    placeholder="Ex: 50"
                  />
                </div>
              </div>
              
              <div>
                <Label htmlFor="descricao">Descrição</Label>
                <Textarea
                  id="descricao"
                  value={novoEvento.descricao}
                  onChange={(e) => setNovoEvento({...novoEvento, descricao: e.target.value})}
                  placeholder="Descreva o evento..."
                  rows={3}
                />
              </div>
              
              <div className="flex gap-2">
                <Button type="submit">Criar Evento</Button>
                <Button type="button" variant="outline" onClick={() => setShowForm(false)}>
                  Cancelar
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

