import bcrypt from 'bcryptjs';
import prisma from './utils/database';

async function seed() {
  try {
    console.log('🌱 Iniciando seed do banco...');

    // Criar usuário administrador
    const hashedPassword = await bcrypt.hash('123456', 12);
    
    const admin = await prisma.user.upsert({
      where: { email: 'admin@tribodocerrado.org' },
      update: {},
      create: {
        email: 'admin@tribodocerrado.org',
        password: hashedPassword,
        nomeCompleto: 'Administrador Tribo do Cerrado',
        telefone: '(61) 99999-9999',
        cidade: 'Goiânia',
        estado: 'GO',
        tipoUsuario: 'ADMINISTRADOR',
        emailVerificado: true
      }
    });

    console.log('✅ Usuário administrador criado:', admin.email);

    // Criar eventos de exemplo
    const eventos = [
      {
        titulo: 'Encontro Mensal da Tribo',
        descricao: 'Encontro mensal para confraternização e planejamento de atividades',
        dataEvento: new Date('2025-01-15T19:00:00Z'),
        localEvento: 'Praça Central de Goiânia',
        endereco: 'Praça Cívica, Centro, Goiânia - GO',
        latitude: -16.6799,
        longitude: -49.2550,
        participantesMaximo: 50
      },
      {
        titulo: 'Trilha do Descoberto',
        descricao: 'Aventura de 3 dias pela Chapada dos Veadeiros com hospedagem organizada',
        dataEvento: new Date('2025-01-25T08:00:00Z'),
        localEvento: 'Alto Paraíso de Goiás',
        endereco: 'Alto Paraíso de Goiás - GO',
        latitude: -14.1319,
        longitude: -47.5156,
        participantesMaximo: 30
      },
      {
        titulo: 'Happy Hour da Tribo',
        descricao: 'Encontro descontraído para networking e diversão',
        dataEvento: new Date('2025-02-05T18:00:00Z'),
        localEvento: 'Bar do Motoqueiro',
        endereco: 'Setor Bueno, Goiânia - GO',
        latitude: -16.7014,
        longitude: -49.2558,
        participantesMaximo: 40
      }
    ];

    // Verificar se eventos já existem
    const eventosExistentes = await prisma.evento.findMany();
    
    if (eventosExistentes.length === 0) {
      await prisma.evento.createMany({
        data: eventos
      });
      console.log('✅ Eventos criados com sucesso');
    } else {
      console.log('✅ Eventos já existem no banco');
    }

    console.log('🎉 Seed concluído com sucesso!');
  } catch (error) {
    console.error('❌ Erro no seed:', error);
  } finally {
    await prisma.$disconnect();
  }
}

seed();
