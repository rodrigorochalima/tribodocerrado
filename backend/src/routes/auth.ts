import express, { Request, Response } from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';
import { body, validationResult } from 'express-validator';
import prisma from '../utils/database';

const router = express.Router();

// Registrar usuário
router.post('/register', [
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 6 }),
  body('nomeCompleto').isLength({ min: 2 }).trim(),
], async (req: Request, res: Response) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        error: true,
        message: 'Dados inválidos',
        details: errors.array()
      });
    }

    const { email, password, nomeCompleto, telefone, cidade, estado } = req.body;

    // Verificar se usuário já existe
    const existingUser = await prisma.user.findUnique({
      where: { email }
    });

    if (existingUser) {
      return res.status(400).json({
        error: true,
        message: 'Email já cadastrado'
      });
    }

    // Hash da senha
    const hashedPassword = await bcrypt.hash(password, 12);

    // Criar usuário
    const user = await prisma.user.create({
      data: {
        email,
        password: hashedPassword,
        nomeCompleto,
        telefone,
        cidade,
        estado,
        tipoUsuario: 'MEMBRO'
      },
      select: {
        id: true,
        email: true,
        nomeCompleto: true,
        tipoUsuario: true,
        createdAt: true
      }
    });

    // Gerar token JWT
    const token = jwt.sign(
      { userId: user.id, email: user.email },
      process.env.JWT_SECRET as string,
      { expiresIn: '7d' }
    );

    return res.status(201).json({
      success: true,
      message: 'Usuário criado com sucesso',
      user,
      token
    });

  } catch (error) {
    console.error('Erro no registro:', error);
    return res.status(500).json({
      error: true,
      message: 'Erro interno do servidor'
    });
  }
});

// Login
router.post('/login', [
  body('email').isEmail().normalizeEmail(),
  body('password').exists(),
], async (req: Request, res: Response) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        error: true,
        message: 'Dados inválidos',
        details: errors.array()
      });
    }

    const { email, password } = req.body;

    // Buscar usuário
    const user = await prisma.user.findUnique({
      where: { email },
      include: {
        motos: true,
        familiares: true,
        premios: true
      }
    });

    if (!user) {
      return res.status(401).json({
        error: true,
        message: 'Email ou senha incorretos'
      });
    }

    // Verificar senha
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({
        error: true,
        message: 'Email ou senha incorretos'
      });
    }

    // Verificar se usuário está ativo
    if (!user.ativo) {
      return res.status(401).json({
        error: true,
        message: 'Conta desativada. Entre em contato com a administração.'
      });
    }

    // Gerar token JWT
    const token = jwt.sign(
      { userId: user.id, email: user.email, tipoUsuario: user.tipoUsuario },
      process.env.JWT_SECRET as string,
      { expiresIn: '7d' }
    );

    // Remover senha da resposta
    const { password: _, ...userWithoutPassword } = user;

    return res.json({
      success: true,
      message: 'Login realizado com sucesso',
      user: userWithoutPassword,
      token
    });

  } catch (error) {
    console.error('Erro no login:', error);
    return res.status(500).json({
      error: true,
      message: 'Erro interno do servidor'
    });
  }
});

// Verificar token
router.get('/verify', async (req: Request, res: Response) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');

    if (!token) {
      return res.status(401).json({
        error: true,
        message: 'Token não fornecido'
      });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET as string) as any;
    
    const user = await prisma.user.findUnique({
      where: { id: decoded.userId },
      select: {
        id: true,
        email: true,
        nomeCompleto: true,
        tipoUsuario: true,
        ativo: true,
        avatarUrl: true
      }
    });

    if (!user || !user.ativo) {
      return res.status(401).json({
        error: true,
        message: 'Token inválido ou usuário inativo'
      });
    }

    return res.json({
      success: true,
      user
    });

  } catch (error) {
    return res.status(401).json({
      error: true,
      message: 'Token inválido'
    });
  }
});

// Esqueci senha
router.post('/forgot-password', [
  body('email').isEmail().normalizeEmail(),
], async (req: Request, res: Response) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({
        error: true,
        message: 'Email inválido'
      });
    }

    const { email } = req.body;

    const user = await prisma.user.findUnique({
      where: { email }
    });

    // Por segurança, sempre retornar sucesso mesmo se email não existir
    return res.json({
      success: true,
      message: 'Se o email estiver cadastrado, você receberá instruções para redefinir sua senha.'
    });

    // TODO: Implementar envio de email com token de reset

  } catch (error) {
    console.error('Erro em esqueci senha:', error);
    return res.status(500).json({
      error: true,
      message: 'Erro interno do servidor'
    });
  }
});

export default router;

