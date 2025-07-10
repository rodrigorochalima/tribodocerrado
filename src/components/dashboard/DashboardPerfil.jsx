import { useState, useRef } from 'react'
import { supabase } from '../../lib/supabase'
import { uploadImageToCloudinary } from '../../lib/cloudinary'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card'
import { Button } from '../ui/button'
import { Input } from '../ui/input'
import { Label } from '../ui/label'
import { Alert, AlertDescription } from '../ui/alert'
import { Avatar, AvatarFallback, AvatarImage } from '../ui/avatar'
import { 
  User, 
  Mail, 
  Phone, 
  Camera, 
  Save, 
  Lock,
  Upload,
  X,
  Check
} from 'lucide-react'

export default function DashboardPerfil({ usuario, session, onUsuarioUpdate }) {
  const [dadosUsuario, setDadosUsuario] = useState({
    nome: usuario?.nome || '',
    email: usuario?.email || '',
    telefone: usuario?.telefone || '',
    foto_url: usuario?.foto_url || ''
  })
  const [senhas, setSenhas] = useState({
    senhaAtual: '',
    novaSenha: '',
    confirmarSenha: ''
  })
  const [loading, setLoading] = useState(false)
  const [uploadingPhoto, setUploadingPhoto] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })
  const [previewImage, setPreviewImage] = useState(null)
  const fileInputRef = useRef(null)

  const handleInputChange = (e) => {
    setDadosUsuario({
      ...dadosUsuario,
      [e.target.name]: e.target.value
    })
  }

  const handlePasswordChange = (e) => {
    setSenhas({
      ...senhas,
      [e.target.name]: e.target.value
    })
  }

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      // Validar tipo de arquivo
      if (!file.type.startsWith('image/')) {
        setMessage({ type: 'error', text: 'Por favor, selecione apenas arquivos de imagem.' })
        return
      }

      // Validar tamanho (máximo 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setMessage({ type: 'error', text: 'A imagem deve ter no máximo 5MB.' })
        return
      }

      // Criar preview
      const reader = new FileReader()
      reader.onload = (e) => {
        setPreviewImage(e.target.result)
      }
      reader.readAsDataURL(file)

      // Upload da imagem
      uploadPhoto(file)
    }
  }

  const uploadPhoto = async (file) => {
    setUploadingPhoto(true)
    setMessage({ type: '', text: '' })

    try {
      const result = await uploadImageToCloudinary(file)
      
      if (result.success) {
        setDadosUsuario({
          ...dadosUsuario,
          foto_url: result.url
        })
        setMessage({ type: 'success', text: 'Foto carregada com sucesso! Clique em "Salvar Alterações" para confirmar.' })
      } else {
        setMessage({ type: 'error', text: 'Erro ao fazer upload da foto: ' + result.error })
        setPreviewImage(null)
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Erro inesperado no upload da foto.' })
      setPreviewImage(null)
    } finally {
      setUploadingPhoto(false)
    }
  }

  const salvarDados = async () => {
    setLoading(true)
    setMessage({ type: '', text: '' })

    try {
      const { error } = await supabase
        .from('usuarios')
        .update({
          nome: dadosUsuario.nome,
          telefone: dadosUsuario.telefone,
          foto_url: dadosUsuario.foto_url
        })
        .eq('id', session.user.id)

      if (error) {
        setMessage({ type: 'error', text: 'Erro ao salvar dados: ' + error.message })
      } else {
        setMessage({ type: 'success', text: 'Dados salvos com sucesso!' })
        // Atualizar dados no componente pai
        onUsuarioUpdate({
          ...usuario,
          nome: dadosUsuario.nome,
          telefone: dadosUsuario.telefone,
          foto_url: dadosUsuario.foto_url
        })
        setPreviewImage(null)
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Erro inesperado ao salvar dados.' })
    } finally {
      setLoading(false)
    }
  }

  const alterarSenha = async () => {
    setLoading(true)
    setMessage({ type: '', text: '' })

    // Validações
    if (senhas.novaSenha !== senhas.confirmarSenha) {
      setMessage({ type: 'error', text: 'As senhas não coincidem.' })
      setLoading(false)
      return
    }

    if (senhas.novaSenha.length < 6) {
      setMessage({ type: 'error', text: 'A nova senha deve ter pelo menos 6 caracteres.' })
      setLoading(false)
      return
    }

    try {
      const { error } = await supabase.auth.updateUser({
        password: senhas.novaSenha
      })

      if (error) {
        setMessage({ type: 'error', text: 'Erro ao alterar senha: ' + error.message })
      } else {
        setMessage({ type: 'success', text: 'Senha alterada com sucesso!' })
        setSenhas({ senhaAtual: '', novaSenha: '', confirmarSenha: '' })
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Erro inesperado ao alterar senha.' })
    } finally {
      setLoading(false)
    }
  }

  const removePreview = () => {
    setPreviewImage(null)
    setDadosUsuario({
      ...dadosUsuario,
      foto_url: usuario?.foto_url || ''
    })
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  return (
    <div className="space-y-6">
      {/* Cabeçalho */}
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">
          Meu Perfil
        </h1>
        <p className="text-orange-200">
          Gerencie suas informações pessoais e configurações da conta
        </p>
      </div>

      {/* Mensagens */}
      {message.text && (
        <Alert className={`${message.type === 'error' ? 'border-red-500/50 bg-red-500/10' : 'border-green-500/50 bg-green-500/10'}`}>
          <AlertDescription className={message.type === 'error' ? 'text-red-200' : 'text-green-200'}>
            {message.text}
          </AlertDescription>
        </Alert>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Foto de Perfil */}
        <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <Camera className="h-5 w-5 mr-2 text-orange-400" />
              Foto de Perfil
            </CardTitle>
            <CardDescription className="text-orange-200">
              Clique na foto para alterar ou arraste uma nova imagem
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-col items-center space-y-4">
              <div className="relative">
                <Avatar className="h-32 w-32 cursor-pointer" onClick={() => fileInputRef.current?.click()}>
                  <AvatarImage src={previewImage || dadosUsuario.foto_url} />
                  <AvatarFallback className="bg-orange-600 text-white text-2xl">
                    {dadosUsuario.nome?.charAt(0) || session?.user?.email?.charAt(0)}
                  </AvatarFallback>
                </Avatar>
                {uploadingPhoto && (
                  <div className="absolute inset-0 bg-black/50 rounded-full flex items-center justify-center">
                    <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-400"></div>
                  </div>
                )}
                {previewImage && (
                  <button
                    onClick={removePreview}
                    className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600"
                  >
                    <X className="h-4 w-4" />
                  </button>
                )}
              </div>

              <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                onChange={handleFileSelect}
                className="hidden"
              />

              <Button
                onClick={() => fileInputRef.current?.click()}
                variant="outline"
                className="border-orange-500/50 text-orange-400 hover:bg-orange-500 hover:text-white"
                disabled={uploadingPhoto}
              >
                <Upload className="h-4 w-4 mr-2" />
                {uploadingPhoto ? 'Carregando...' : 'Escolher Foto'}
              </Button>

              <p className="text-xs text-orange-300 text-center">
                Formatos aceitos: JPG, PNG, GIF<br />
                Tamanho máximo: 5MB
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Informações Pessoais */}
        <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <User className="h-5 w-5 mr-2 text-orange-400" />
              Informações Pessoais
            </CardTitle>
            <CardDescription className="text-orange-200">
              Atualize seus dados pessoais
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="nome" className="text-white">Nome Completo</Label>
              <Input
                id="nome"
                name="nome"
                value={dadosUsuario.nome}
                onChange={handleInputChange}
                className="bg-black/30 border-orange-500/30 text-white"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="email" className="text-white">Email</Label>
              <Input
                id="email"
                name="email"
                value={dadosUsuario.email}
                disabled
                className="bg-black/30 border-orange-500/30 text-gray-400"
              />
              <p className="text-xs text-orange-300">
                O email não pode ser alterado
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="telefone" className="text-white">Telefone</Label>
              <Input
                id="telefone"
                name="telefone"
                value={dadosUsuario.telefone}
                onChange={handleInputChange}
                placeholder="(11) 99999-9999"
                className="bg-black/30 border-orange-500/30 text-white"
              />
            </div>

            <Button
              onClick={salvarDados}
              disabled={loading}
              className="w-full bg-orange-600 hover:bg-orange-700 text-white"
            >
              <Save className="h-4 w-4 mr-2" />
              {loading ? 'Salvando...' : 'Salvar Alterações'}
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Alterar Senha */}
      <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-white flex items-center">
            <Lock className="h-5 w-5 mr-2 text-orange-400" />
            Alterar Senha
          </CardTitle>
          <CardDescription className="text-orange-200">
            Mantenha sua conta segura com uma senha forte
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="space-y-2">
              <Label htmlFor="senhaAtual" className="text-white">Senha Atual</Label>
              <Input
                id="senhaAtual"
                name="senhaAtual"
                type="password"
                value={senhas.senhaAtual}
                onChange={handlePasswordChange}
                className="bg-black/30 border-orange-500/30 text-white"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="novaSenha" className="text-white">Nova Senha</Label>
              <Input
                id="novaSenha"
                name="novaSenha"
                type="password"
                value={senhas.novaSenha}
                onChange={handlePasswordChange}
                className="bg-black/30 border-orange-500/30 text-white"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="confirmarSenha" className="text-white">Confirmar Nova Senha</Label>
              <Input
                id="confirmarSenha"
                name="confirmarSenha"
                type="password"
                value={senhas.confirmarSenha}
                onChange={handlePasswordChange}
                className="bg-black/30 border-orange-500/30 text-white"
              />
            </div>
          </div>

          <div className="mt-6">
            <Button
              onClick={alterarSenha}
              disabled={loading || !senhas.novaSenha || !senhas.confirmarSenha}
              className="bg-orange-600 hover:bg-orange-700 text-white"
            >
              <Lock className="h-4 w-4 mr-2" />
              {loading ? 'Alterando...' : 'Alterar Senha'}
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Informações da Conta */}
      <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-white">Informações da Conta</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-orange-200">Tipo de Conta:</span>
              <span className="text-white ml-2 font-medium">
                {usuario?.tipo === 'admin' ? 'Administrador' : 'Membro'}
              </span>
            </div>
            <div>
              <span className="text-orange-200">Status:</span>
              <span className="text-green-400 ml-2 font-medium">
                {usuario?.ativo ? 'Ativo' : 'Inativo'}
              </span>
            </div>
            <div>
              <span className="text-orange-200">Membro desde:</span>
              <span className="text-white ml-2">
                {usuario?.created_at ? new Date(usuario.created_at).toLocaleDateString('pt-BR') : 'N/A'}
              </span>
            </div>
            <div>
              <span className="text-orange-200">Último acesso:</span>
              <span className="text-white ml-2">
                {session?.user?.last_sign_in_at ? new Date(session.user.last_sign_in_at).toLocaleDateString('pt-BR') : 'N/A'}
              </span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

