import { Link } from 'react-router-dom'
import { Button } from './ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Users, Calendar, Camera, Shield, MapPin, Phone, Mail, Bike, Heart, Trophy } from 'lucide-react'
import logoTribo from '../assets/LogoTriboSite.png'
import fundoSite from '../assets/FundoSite.png'

export default function PaginaPublica() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-900 via-red-900 to-black">
      {/* Header com Logo */}
      <header className="relative z-10 p-4">
        <div className="container mx-auto flex justify-between items-center">
          <img src={logoTribo} alt="Tribo do Cerrado MC" className="h-16 w-auto" />
          <div className="flex gap-4">
            <Button asChild variant="outline" className="border-orange-500 text-orange-500 hover:bg-orange-500 hover:text-white">
              <Link to="/login">Área dos Membros</Link>
            </Button>
          </div>
        </div>
      </header>

      {/* Grid Principal 3x3 */}
      <main className="container mx-auto p-4 grid grid-cols-1 md:grid-cols-3 gap-6 min-h-screen">
        
        {/* Linha 1 */}
        {/* 1.1 - Hero Principal */}
        <div className="md:col-span-2 relative h-96 md:h-auto bg-cover bg-center bg-no-repeat rounded-lg overflow-hidden"
             style={{ backgroundImage: `url(${fundoSite})` }}>
          <div className="absolute inset-0 bg-black/60"></div>
          <div className="relative z-10 flex flex-col justify-center items-center h-full text-center p-8">
            <h1 className="text-4xl md:text-6xl font-bold text-white mb-4">
              TRIBO DO CERRADO MC
            </h1>
            <p className="text-lg md:text-xl text-orange-200 mb-6 max-w-lg">
              Mais que um motoclube, uma família unida pela paixão pelas duas rodas
            </p>
            <Button asChild size="lg" className="bg-orange-600 hover:bg-orange-700 text-white px-8 py-3">
              <Link to="/cadastro">Quero ser Membro</Link>
            </Button>
          </div>
        </div>

        {/* 1.3 - Próximos Eventos */}
        <Card className="bg-black/80 border-orange-500 text-white">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-400">
              <Calendar className="h-5 w-5" />
              Próximos Eventos
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="border-l-2 border-orange-500 pl-3">
                <p className="font-semibold">Encontro Mensal</p>
                <p className="text-sm text-gray-300">15 de Janeiro</p>
              </div>
              <div className="border-l-2 border-orange-500 pl-3">
                <p className="font-semibold">Viagem Chapada</p>
                <p className="text-sm text-gray-300">22-24 de Janeiro</p>
              </div>
              <div className="border-l-2 border-orange-500 pl-3">
                <p className="font-semibold">Aniversário MC</p>
                <p className="text-sm text-gray-300">5 de Fevereiro</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Linha 2 */}
        {/* 2.1 - Sobre Nós */}
        <Card className="bg-black/80 border-orange-500 text-white">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-400">
              <Shield className="h-5 w-5" />
              Nossa História
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-300 leading-relaxed">
              Fundado no coração do Brasil, somos um motoclube que valoriza a irmandade, 
              o respeito e a paixão pelas motocicletas. Nossa história é construída sobre 
              valores sólidos e tradições que passamos de geração em geração.
            </p>
          </CardContent>
        </Card>

        {/* 2.2 - Galeria de Fotos */}
        <Card className="bg-black/80 border-orange-500 text-white">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-400">
              <Camera className="h-5 w-5" />
              Galeria
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-2">
              <div className="bg-orange-600/20 h-20 rounded flex items-center justify-center">
                <Camera className="h-8 w-8 text-orange-400" />
              </div>
              <div className="bg-orange-600/20 h-20 rounded flex items-center justify-center">
                <Bike className="h-8 w-8 text-orange-400" />
              </div>
              <div className="bg-orange-600/20 h-20 rounded flex items-center justify-center">
                <Users className="h-8 w-8 text-orange-400" />
              </div>
              <div className="bg-orange-600/20 h-20 rounded flex items-center justify-center">
                <Trophy className="h-8 w-8 text-orange-400" />
              </div>
            </div>
            <p className="text-xs text-gray-400 mt-2 text-center">
              Momentos especiais da nossa jornada
            </p>
          </CardContent>
        </Card>

        {/* 2.3 - Nossos Valores */}
        <Card className="bg-black/80 border-orange-500 text-white">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-400">
              <Heart className="h-5 w-5" />
              Nossos Valores
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <Shield className="h-4 w-4 text-orange-400" />
                <span className="text-sm">Irmandade</span>
              </div>
              <div className="flex items-center gap-2">
                <Users className="h-4 w-4 text-orange-400" />
                <span className="text-sm">Respeito</span>
              </div>
              <div className="flex items-center gap-2">
                <Bike className="h-4 w-4 text-orange-400" />
                <span className="text-sm">Paixão</span>
              </div>
              <div className="flex items-center gap-2">
                <Trophy className="h-4 w-4 text-orange-400" />
                <span className="text-sm">Tradição</span>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Linha 3 */}
        {/* 3.1 - Membros Destacados */}
        <Card className="bg-black/80 border-orange-500 text-white">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-400">
              <Users className="h-5 w-5" />
              Membros
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-orange-600 rounded-full flex items-center justify-center">
                  <Users className="h-5 w-5 text-white" />
                </div>
                <div>
                  <p className="font-semibold text-sm">Presidente</p>
                  <p className="text-xs text-gray-400">Líder da Tribo</p>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-orange-600 rounded-full flex items-center justify-center">
                  <Shield className="h-5 w-5 text-white" />
                </div>
                <div>
                  <p className="font-semibold text-sm">Vice-Presidente</p>
                  <p className="text-xs text-gray-400">Braço direito</p>
                </div>
              </div>
              <div className="text-center mt-4">
                <p className="text-xs text-gray-400">+25 membros ativos</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* 3.2 - Estatísticas */}
        <Card className="bg-black/80 border-orange-500 text-white">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-400">
              <Trophy className="h-5 w-5" />
              Nossa Força
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 gap-4 text-center">
              <div>
                <p className="text-2xl font-bold text-orange-400">25+</p>
                <p className="text-xs text-gray-400">Membros</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-orange-400">5</p>
                <p className="text-xs text-gray-400">Anos</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-orange-400">50+</p>
                <p className="text-xs text-gray-400">Viagens</p>
              </div>
              <div>
                <p className="text-2xl font-bold text-orange-400">100+</p>
                <p className="text-xs text-gray-400">Eventos</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* 3.3 - Contato */}
        <Card className="bg-black/80 border-orange-500 text-white">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-orange-400">
              <Phone className="h-5 w-5" />
              Contato
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              <div className="flex items-center gap-2">
                <MapPin className="h-4 w-4 text-orange-400" />
                <span className="text-sm">Brasília - DF</span>
              </div>
              <div className="flex items-center gap-2">
                <Phone className="h-4 w-4 text-orange-400" />
                <span className="text-sm">(61) 99999-9999</span>
              </div>
              <div className="flex items-center gap-2">
                <Mail className="h-4 w-4 text-orange-400" />
                <span className="text-sm">contato@tribodocerrado.org</span>
              </div>
              <div className="mt-4">
                <Button asChild size="sm" className="w-full bg-orange-600 hover:bg-orange-700">
                  <Link to="/cadastro">Fale Conosco</Link>
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

      </main>

      {/* Footer */}
      <footer className="bg-black/90 text-white p-6 mt-8">
        <div className="container mx-auto text-center">
          <p className="text-sm text-gray-400">
            © 2024 Tribo do Cerrado MC. Todos os direitos reservados.
          </p>
          <p className="text-xs text-gray-500 mt-2">
            Mais que um motoclube, uma família unida pela paixão pelas duas rodas.
          </p>
        </div>
      </footer>
    </div>
  )
}
