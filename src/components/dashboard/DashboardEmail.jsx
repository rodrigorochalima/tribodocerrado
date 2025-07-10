import { useState, useEffect } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Input } from '../ui/input'
import { Textarea } from '../ui/textarea'
import { Badge } from '../ui/badge'
import { 
  Mail, 
  Send, 
  Inbox, 
  SendHorizontal, 
  FileText, 
  Trash2, 
  Search, 
  Plus,
  Star,
  Archive,
  Reply,
  Forward,
  MoreHorizontal
} from 'lucide-react'

export default function DashboardEmail({ usuario }) {
  const [pastaAtiva, setPastaAtiva] = useState('inbox')
  const [emailSelecionado, setEmailSelecionado] = useState(null)
  const [mostrarComposer, setMostrarComposer] = useState(false)
  const [emails, setEmails] = useState([])
  const [novoEmail, setNovoEmail] = useState({
    para: '',
    assunto: '',
    mensagem: ''
  })

  useEffect(() => {
    carregarEmails()
  }, [pastaAtiva])

  const carregarEmails = () => {
    // Simulação de emails (pode ser integrado com API real)
    const emailsSimulados = {
      inbox: [
        {
          id: 1,
          de: 'admin@tribodocerrado.org',
          para: usuario?.email,
          assunto: 'Bem-vindo à Tribo do Cerrado MC!',
          preview: 'Seja bem-vindo ao nosso motoclube. Aqui você encontrará uma família...',
          mensagem: 'Seja bem-vindo ao nosso motoclube. Aqui você encontrará uma família unida pela paixão pelas duas rodas. Esperamos que você aproveite todos os recursos do sistema e participe ativamente de nossos eventos.',
          data: '2024-01-10T10:30:00',
          lido: false,
          importante: true
        },
        {
          id: 2,
          de: 'eventos@tribodocerrado.org',
          para: usuario?.email,
          assunto: 'Próximo Encontro - Sábado 15/01',
          preview: 'Não perca nosso próximo encontro! Será no sábado às 14h...',
          mensagem: 'Não perca nosso próximo encontro! Será no sábado às 14h no Parque da Cidade. Traga sua moto e venha confraternizar com a galera. Haverá churrasco e muita diversão!',
          data: '2024-01-09T15:45:00',
          lido: true,
          importante: false
        },
        {
          id: 3,
          de: 'secretaria@tribodocerrado.org',
          para: usuario?.email,
          assunto: 'Atualização de Dados Cadastrais',
          preview: 'Por favor, verifique e atualize seus dados cadastrais...',
          mensagem: 'Por favor, verifique e atualize seus dados cadastrais no sistema. É importante manter suas informações sempre atualizadas para receber comunicados importantes.',
          data: '2024-01-08T09:15:00',
          lido: true,
          importante: false
        }
      ],
      sent: [
        {
          id: 4,
          de: usuario?.email,
          para: 'admin@tribodocerrado.org',
          assunto: 'Dúvida sobre próximo evento',
          preview: 'Gostaria de saber mais detalhes sobre o próximo evento...',
          mensagem: 'Gostaria de saber mais detalhes sobre o próximo evento. Qual o horário exato e se preciso levar alguma coisa específica?',
          data: '2024-01-09T16:20:00',
          lido: true,
          importante: false
        }
      ],
      drafts: [],
      trash: []
    }

    setEmails(emailsSimulados[pastaAtiva] || [])
  }

  const pastas = [
    { id: 'inbox', nome: 'Caixa de Entrada', icon: Inbox, count: 3 },
    { id: 'sent', nome: 'Enviados', icon: SendHorizontal, count: 1 },
    { id: 'drafts', nome: 'Rascunhos', icon: FileText, count: 0 },
    { id: 'trash', nome: 'Lixeira', icon: Trash2, count: 0 }
  ]

  const formatarData = (dataString) => {
    const data = new Date(dataString)
    const hoje = new Date()
    const ontem = new Date(hoje)
    ontem.setDate(ontem.getDate() - 1)

    if (data.toDateString() === hoje.toDateString()) {
      return data.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    } else if (data.toDateString() === ontem.toDateString()) {
      return 'Ontem'
    } else {
      return data.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' })
    }
  }

  const enviarEmail = () => {
    // Simular envio de email
    console.log('Enviando email:', novoEmail)
    setMostrarComposer(false)
    setNovoEmail({ para: '', assunto: '', mensagem: '' })
    // Aqui seria integrado com API real de email
  }

  const marcarComoLido = (emailId) => {
    setEmails(emails.map(email => 
      email.id === emailId ? { ...email, lido: true } : email
    ))
  }

  return (
    <div className="space-y-6">
      {/* Cabeçalho */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white mb-2">
            Sistema de Email
          </h1>
          <p className="text-orange-200">
            Comunicação interna do motoclube
          </p>
        </div>
        <Button 
          onClick={() => setMostrarComposer(true)}
          className="bg-orange-600 hover:bg-orange-700 text-white"
        >
          <Plus className="h-4 w-4 mr-2" />
          Novo Email
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar - Pastas */}
        <div className="lg:col-span-1">
          <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-white text-lg">Pastas</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {pastas.map((pasta) => {
                const Icon = pasta.icon
                return (
                  <button
                    key={pasta.id}
                    onClick={() => setPastaAtiva(pasta.id)}
                    className={`w-full flex items-center justify-between p-3 rounded-lg transition-colors ${
                      pastaAtiva === pasta.id
                        ? 'bg-orange-600 text-white'
                        : 'text-orange-200 hover:bg-orange-500/20 hover:text-white'
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <Icon className="h-4 w-4" />
                      <span>{pasta.nome}</span>
                    </div>
                    {pasta.count > 0 && (
                      <Badge variant="secondary" className="bg-orange-500 text-white">
                        {pasta.count}
                      </Badge>
                    )}
                  </button>
                )
              })}
            </CardContent>
          </Card>
        </div>

        {/* Lista de Emails */}
        <div className="lg:col-span-1">
          <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-white">
                  {pastas.find(p => p.id === pastaAtiva)?.nome}
                </CardTitle>
                <div className="flex items-center space-x-2">
                  <Button variant="ghost" size="sm" className="text-orange-400 hover:text-white">
                    <Search className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <div className="max-h-96 overflow-y-auto">
                {emails.length > 0 ? (
                  emails.map((email) => (
                    <div
                      key={email.id}
                      onClick={() => {
                        setEmailSelecionado(email)
                        marcarComoLido(email.id)
                      }}
                      className={`p-4 border-b border-orange-500/20 cursor-pointer transition-colors hover:bg-orange-500/10 ${
                        emailSelecionado?.id === email.id ? 'bg-orange-500/20' : ''
                      } ${!email.lido ? 'bg-orange-500/5' : ''}`}
                    >
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          <div className={`w-2 h-2 rounded-full ${email.importante ? 'bg-yellow-400' : 'bg-transparent'}`}></div>
                          <span className={`text-sm ${!email.lido ? 'font-bold text-white' : 'text-orange-200'}`}>
                            {pastaAtiva === 'sent' ? email.para : email.de}
                          </span>
                        </div>
                        <span className="text-xs text-orange-300">
                          {formatarData(email.data)}
                        </span>
                      </div>
                      <h4 className={`text-sm mb-1 ${!email.lido ? 'font-bold text-white' : 'text-orange-100'}`}>
                        {email.assunto}
                      </h4>
                      <p className="text-xs text-orange-300 truncate">
                        {email.preview}
                      </p>
                      {!email.lido && (
                        <div className="w-2 h-2 bg-orange-400 rounded-full mt-2"></div>
                      )}
                    </div>
                  ))
                ) : (
                  <div className="p-8 text-center">
                    <Mail className="h-12 w-12 text-orange-400 mx-auto mb-4" />
                    <p className="text-orange-200">Nenhum email nesta pasta</p>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Visualização do Email */}
        <div className="lg:col-span-2">
          <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
            {emailSelecionado ? (
              <>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="text-white">{emailSelecionado.assunto}</CardTitle>
                      <CardDescription className="text-orange-200">
                        De: {emailSelecionado.de} • {formatarData(emailSelecionado.data)}
                      </CardDescription>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Button variant="ghost" size="sm" className="text-orange-400 hover:text-white">
                        <Reply className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm" className="text-orange-400 hover:text-white">
                        <Forward className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm" className="text-orange-400 hover:text-white">
                        <Archive className="h-4 w-4" />
                      </Button>
                      <Button variant="ghost" size="sm" className="text-orange-400 hover:text-white">
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="prose prose-invert max-w-none">
                    <p className="text-orange-100 leading-relaxed">
                      {emailSelecionado.mensagem}
                    </p>
                  </div>
                </CardContent>
              </>
            ) : (
              <CardContent className="flex items-center justify-center h-96">
                <div className="text-center">
                  <Mail className="h-16 w-16 text-orange-400 mx-auto mb-4" />
                  <p className="text-orange-200 text-lg">Selecione um email para visualizar</p>
                </div>
              </CardContent>
            )}
          </Card>
        </div>
      </div>

      {/* Modal de Composição */}
      {mostrarComposer && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <Card className="bg-black/90 border-orange-500/30 backdrop-blur-sm w-full max-w-2xl">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-white">Novo Email</CardTitle>
                <Button 
                  variant="ghost" 
                  size="sm" 
                  onClick={() => setMostrarComposer(false)}
                  className="text-orange-400 hover:text-white"
                >
                  ✕
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-white text-sm font-medium">Para:</label>
                <Input
                  value={novoEmail.para}
                  onChange={(e) => setNovoEmail({...novoEmail, para: e.target.value})}
                  placeholder="destinatario@email.com"
                  className="mt-1 bg-black/30 border-orange-500/30 text-white"
                />
              </div>
              <div>
                <label className="text-white text-sm font-medium">Assunto:</label>
                <Input
                  value={novoEmail.assunto}
                  onChange={(e) => setNovoEmail({...novoEmail, assunto: e.target.value})}
                  placeholder="Assunto do email"
                  className="mt-1 bg-black/30 border-orange-500/30 text-white"
                />
              </div>
              <div>
                <label className="text-white text-sm font-medium">Mensagem:</label>
                <Textarea
                  value={novoEmail.mensagem}
                  onChange={(e) => setNovoEmail({...novoEmail, mensagem: e.target.value})}
                  placeholder="Digite sua mensagem aqui..."
                  rows={8}
                  className="mt-1 bg-black/30 border-orange-500/30 text-white"
                />
              </div>
              <div className="flex items-center justify-end space-x-3">
                <Button 
                  variant="outline" 
                  onClick={() => setMostrarComposer(false)}
                  className="border-orange-500/50 text-orange-400 hover:bg-orange-500 hover:text-white"
                >
                  Cancelar
                </Button>
                <Button 
                  onClick={enviarEmail}
                  className="bg-orange-600 hover:bg-orange-700 text-white"
                >
                  <Send className="h-4 w-4 mr-2" />
                  Enviar
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}

