import { PrismaClient } from '@prisma/client';

// Singleton do Prisma Client
const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
});

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}

// Função para conectar ao banco
export async function connectDatabase() {
  try {
    await prisma.$connect();
    console.log('✅ Conectado ao banco PostgreSQL (Neon)');
  } catch (error) {
    console.error('❌ Erro ao conectar ao banco:', error);
    process.exit(1);
  }
}

// Função para desconectar do banco
export async function disconnectDatabase() {
  try {
    await prisma.$disconnect();
    console.log('✅ Desconectado do banco PostgreSQL');
  } catch (error) {
    console.error('❌ Erro ao desconectar do banco:', error);
  }
}

// Função para verificar saúde do banco
export async function checkDatabaseHealth() {
  try {
    await prisma.$queryRaw`SELECT 1`;
    return { status: 'healthy', message: 'Banco conectado e funcionando' };
  } catch (error) {
    return { status: 'unhealthy', message: 'Erro na conexão com o banco', error };
  }
}

export default prisma;

