import express, { Request, Response } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
import rateLimit from 'express-rate-limit';

// Importar rotas
import authRoutes from './routes/auth';
import userRoutes from './routes/users';
import eventRoutes from './routes/events';
import uploadRoutes from './routes/upload';
import emailRoutes from './routes/email';

// Carregar variáveis de ambiente
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3001;

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutos
  max: 100, // máximo 100 requests por IP por janela
  message: 'Muitas tentativas. Tente novamente em 15 minutos.',
});

// Middlewares de segurança
app.use(helmet());
app.use(limiter);

// CORS configurado para frontend
app.use(cors({
  origin: [
    'http://localhost:3000',
    'https://tribodocerrado.org',
    'https://www.tribodocerrado.org'
  ],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Middlewares gerais
app.use(morgan('combined'));
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));

// Servir arquivos estáticos
app.use('/uploads', express.static('uploads'));

// Rotas da API
app.use('/api/auth', authRoutes);
app.use('/api/users', userRoutes);
app.use('/api/events', eventRoutes);
app.use('/api/upload', uploadRoutes);
app.use('/api/email', emailRoutes);

// Rota de health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'OK',
    message: 'Tribo do Cerrado API funcionando!',
    timestamp: new Date().toISOString(),
    environment: process.env.NODE_ENV
  });
});

// Rota raiz
app.get('/', (req, res) => {
  res.json({
    message: '🏍️ Tribo do Cerrado - API Backend',
    version: '2.0.0',
    documentation: '/api/docs',
    health: '/api/health'
  });
});

// Middleware de tratamento de erros
app.use((err: any, req: express.Request, res: express.Response, next: express.NextFunction) => {
  console.error('Erro:', err);
  
  res.status(err.status || 500).json({
    error: true,
    message: err.message || 'Erro interno do servidor',
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
});

// Middleware para rotas não encontradas
app.use('*', (req, res) => {
  res.status(404).json({
    error: true,
    message: 'Rota não encontrada',
    path: req.originalUrl
  });
});

// Iniciar servidor
app.listen(PORT, () => {
  console.log(`🚀 Servidor rodando na porta ${PORT}`);
  console.log(`🌍 Ambiente: ${process.env.NODE_ENV}`);
  console.log(`📡 API disponível em: http://localhost:${PORT}`);
  console.log(`🏥 Health check: http://localhost:${PORT}/api/health`);
});

export default app;

