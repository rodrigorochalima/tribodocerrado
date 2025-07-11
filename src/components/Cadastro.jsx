import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Input } from '../ui/input'
import { Label } from '../ui/label'
import { Alert, AlertDescription } from '../ui/alert'
import { auth, salvarDadosUsuario } from '../lib/supabase'

export default function Cadastro() {
  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    telefone: '',
    password: '',
    confirmPassword: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')
    setSuccess('')

    // Validações
    if (formData.password !== formData.confirmPassword) {
      setError('As senhas não coincidem')
      setLoading(false)
      return
    }

    if (formData.password.length < 6) {
      setError('A senha deve ter pelo menos 6 caracteres')
      setLoading(false)
      return
    }

    try {
      // 1. Criar usuário no Supabase Auth
      const authResult = await auth.signUp({
        email: formData.email,
        password: formData.password,
        options: {
          data: {
            nome: formData.nome,
            telefone: formData.telefone
          }
        }
      })

      if (!authResult.user) {
        setError('Erro ao criar conta: ' + (authResult.error?.message || 'Erro desconhecido'))
        setLoading(false)
        return
      }

      // 2. Salvar dados adicionais na tabela usuarios
      const userData = {
        nome: formData.nome,
        email: formData.email,
        telefone: formData.telefone,
        tipo: 'membro',
        status: 'ativo',
        auth_id: authResult.user.id
      }

      const dbResult = await salvarDadosUsuario(userData)

      if (dbResult.success) {
        setSuccess('Cadastro realizado com sucesso! Você pode fazer login agora.')
        setTimeout(() => {
          navigate('/login')
        }, 2000)
      } else {
        setError('Erro ao salvar dados do usuário: ' + (dbResult.error || 'Erro desconhecido'))
      }

    } catch (err) {
      setError('Erro inesperado. Tente novamente.')
      console.error('Erro no cadastro:', err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-400 via-blue-500 to-purple-600 flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl font-bold">📝 Cadastro</CardTitle>
          <CardDescription>
            Registre-se como novo membro do Tribo do Cerrado
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          {error && (
            <Alert className="border-red-200 bg-red-50">
              <AlertDescription className="text-red-800">
                {error}
              </AlertDescription>
            </Alert>
          )}
          
          {success && (
            <Alert className="border-green-200 bg-green-50">
              <AlertDescription className="text-green-800">
                {success}
              </AlertDescription>
            </Alert>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="nome">👤 Nome Completo</Label>
              <Input
                id="nome"
                name="nome"
                type="text"
                placeholder="Seu nome completo"
                value={formData.nome}
                onChange={handleChange}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email">📧 Email</Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="seu@email.com"
                value={formData.email}
                onChange={handleChange}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="telefone">📱 Telefone</Label>
              <Input
                id="telefone"
                name="telefone"
                type="tel"
                placeholder="(62) 99999-9999"
                value={formData.telefone}
                onChange={handleChange}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="password">🔒 Senha</Label>
              <Input
                id="password"
                name="password"
                type="password"
                placeholder="Mínimo 6 caracteres"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="confirmPassword">🔒 Confirmar Senha</Label>
              <Input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                placeholder="Digite a senha novamente"
                value={formData.confirmPassword}
                onChange={handleChange}
                required
              />
            </div>

            <Button 
              type="submit" 
              className="w-full bg-green-600 hover:bg-green-700"
              disabled={loading}
            >
              {loading ? '⏳ Criando...' : '📝 CRIAR CONTA'}
            </Button>
          </form>

          <div className="text-center space-y-2">
            <Button
              variant="outline"
              onClick={() => navigate('/login')}
              className="w-full"
            >
              🔐 Já tenho conta
            </Button>
            
            <Button
              variant="ghost"
              onClick={() => navigate('/')}
              className="w-full"
            >
              ⬅️ Voltar
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}


