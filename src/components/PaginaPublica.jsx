import { Link } from 'react-router-dom'
import { Button } from './ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card'
import { Users, Calendar, Camera, Shield, MapPin, Phone, Mail } from 'lucide-react'
import logoTribo from '../assets/LogoTriboSite.png'
import fundoSite from '../assets/FundoSite.png'

export default function PaginaPublica() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div 
        className="relative h-screen bg-cover bg-center bg-no-repeat"
        style={{ backgroundImage: `url(${fundoSite})` }}
      >
        <div className="absolute inset-0 bg-black/60"></div>
        <div className="relative z-10 flex flex-col items-center justify-center h-full text-center px-4">
          <img 
            src={logoTribo} 
            alt="Tribo do Cerrado MC" 
            className="h-32 w-auto mb-8"
          />
          <h1 className="text-5xl md:text-7xl font-bold text-white mb-4">
            TRIBO DO CERRADO MC
          </h1>
          <p className="text-xl md:text-2xl text-orange-200 mb-8 max-w-2xl">
            Mais que um motoclube, uma família unida pela paixão pelas duas rodas
          </p>
          <div className="flex flex-col sm:flex-row gap-4">
            <Button 
              asChild
              size="lg"
              className="bg-orange-600 hover:bg-orange-700 text-white px-8 py-3"
            >
              <Link to="/cadastro">Quero ser Membro</Link>
            </Button>
            <Button 
              asChild
              variant="outline"
              size="lg"
              className="border-orange-500 text-orange-400 hover:bg-orange-500 hover:text-white px-8 py-3"
            >
              <Link to="/login">Área dos Membros</Link>
            </Button>
          </div>
        </div>
      </div>

      {/* Sobre o Motoclube */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Sobre a Tribo do Cerrado MC
            </h2>
            <p className="text-xl text-orange-200 max-w-3xl mx-auto">
              Fundado no coração do Brasil, somos um motoclube que valoriza a irmandade, 
              o respeito e a paixão pelas motocicletas. Nossa história é construída sobre 
              valores sólidos e experiências inesquecíveis.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
              <CardHeader className="text-center">
                <Users className="h-12 w-12 text-orange-400 mx-auto mb-4" />
                <CardTitle className="text-white">Irmandade</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-orange-200 text-center">
                  Uma família unida pelos valores de respeito, lealdade e companheirismo
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
              <CardHeader className="text-center">
                <Calendar className="h-12 w-12 text-orange-400 mx-auto mb-4" />
                <CardTitle className="text-white">Eventos</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-orange-200 text-center">
                  Encontros, viagens e eventos que fortalecem nossos laços
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
              <CardHeader className="text-center">
                <Camera className="h-12 w-12 text-orange-400 mx-auto mb-4" />
                <CardTitle className="text-white">Memórias</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-orange-200 text-center">
                  Registramos cada momento especial da nossa jornada
                </CardDescription>
              </CardContent>
            </Card>

            <Card className="bg-black/50 border-orange-500/30 backdrop-blur-sm">
              <CardHeader className="text-center">
                <Shield className="h-12 w-12 text-orange-400 mx-auto mb-4" />
                <CardTitle className="text-white">Tradição</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-orange-200 text-center">
                  Preservamos e honramos as tradições do motociclismo
                </CardDescription>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Nossos Valores */}
      <section className="py-20 px-4 bg-black/30">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-8">
            Nossos Valores
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-2xl font-bold text-orange-400 mb-4">Respeito</h3>
              <p className="text-orange-200">
                Respeitamos todos os membros, suas diferenças e opiniões, 
                criando um ambiente de harmonia e compreensão.
              </p>
            </div>
            <div>
              <h3 className="text-2xl font-bold text-orange-400 mb-4">Lealdade</h3>
              <p className="text-orange-200">
                A lealdade entre os membros é fundamental. Estamos sempre 
                prontos para apoiar nossos irmãos em qualquer situação.
              </p>
            </div>
            <div>
              <h3 className="text-2xl font-bold text-orange-400 mb-4">Paixão</h3>
              <p className="text-orange-200">
                Nossa paixão pelas motocicletas e pela estrada nos une 
                e nos motiva a viver cada aventura intensamente.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Contato */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Entre em Contato
            </h2>
            <p className="text-xl text-orange-200">
              Quer saber mais sobre o motoclube? Entre em contato conosco!
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div className="flex flex-col items-center">
              <MapPin className="h-12 w-12 text-orange-400 mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">Localização</h3>
              <p className="text-orange-200">
                Brasília - DF<br />
                Região do Cerrado
              </p>
            </div>

            <div className="flex flex-col items-center">
              <Phone className="h-12 w-12 text-orange-400 mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">Telefone</h3>
              <p className="text-orange-200">
                (61) 99999-9999
              </p>
            </div>

            <div className="flex flex-col items-center">
              <Mail className="h-12 w-12 text-orange-400 mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">Email</h3>
              <p className="text-orange-200">
                contato@tribodocerrado.org
              </p>
            </div>
          </div>

          <div className="text-center mt-12">
            <Button 
              asChild
              size="lg"
              className="bg-orange-600 hover:bg-orange-700 text-white px-8 py-3"
            >
              <Link to="/cadastro">Quero Fazer Parte da Tribo</Link>
            </Button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-4 bg-black/50 border-t border-orange-500/30">
        <div className="max-w-6xl mx-auto text-center">
          <p className="text-orange-200">
            © 2024 Tribo do Cerrado MC. Todos os direitos reservados.
          </p>
          <p className="text-orange-300 mt-2">
            Mais que um motoclube, uma família.
          </p>
        </div>
      </footer>
    </div>
  )
}

