import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Button } from './ui/button'
import { Input } from './ui/input'
import { Label } from './ui/label'
import { Alert, AlertDescription } from './ui/alert'
import { auth, database } from '../lib/supabase'

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
      const authResult = await auth.signUp(formData.email, formData.password, {
        nome: formData.nome,
        telefone: formData.telefone
      })

      if (!authResult.success) {
        setError(authResult.error)
        setLoading(false)
        return
      }

      // 2. Criar registro na tabela usuarios
      const userData = {
        nome: formData.nome,
        email: formData.email,
        telefone: formData.telefone,
        tipo: 'membro',
        status: 'ativo',
        auth_id: authResult.user.id
      }

      const dbResult = await database.createUser(userData)

      if (dbResult.success) {
        setSuccess('Cadastro realizado com sucesso! Você pode fazer login agora.')
        setTimeout(() => {
          navigate('/login')
        }, 2000)
      } else {
        setError('Erro ao salvar dados do usuário: ' + dbResult.error)
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
          <CardTitle className="text-2xl font-bold text-gray-800">
            📝 Cadastro
          </CardTitle>
          <CardDescription>
            Registre-se como novo membro do Tribo do Cerrado
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
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
                disabled={loading}
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
                disabled={loading}
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
                disabled={loading}
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
                disabled={loading}
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
                disabled={loading}
              />
            </div>
            
            <Button 
              type="submit" 
              className="w-full bg-green-500 hover:bg-green-600 text-white font-bold"
              disabled={loading}
            >
              {loading ? '⏳ Cadastrando...' : '📝 CRIAR CONTA'}
            </Button>
          </form>
          
          <div className="mt-6 text-center space-y-2">
            <Button 
              variant="link" 
              onClick={() => navigate('/login')}
              className="text-blue-600 hover:text-blue-800"
            >
              🔐 Já tenho conta
            </Button>
            <br />
            <Button 
              variant="link" 
              onClick={() => navigate('/')}
              className="text-gray-600 hover:text-gray-800"
            >
              ⬅️ Voltar
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

