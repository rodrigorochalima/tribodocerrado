import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import prisma from '../utils/database';

export interface AuthRequest extends Request {
  user?: {
    userId: string;
    email: string;
    tipoUsuario: string;
  };
}

export const authMiddleware = async (req: AuthRequest, res: Response, next: NextFunction) => {
  try {
    const token = req.headers.authorization?.replace('Bearer ', '');

    if (!token) {
      return res.status(401).json({
        error: true,
        message: 'Token de acesso requerido'
      });
    }

    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as any;
    
    const user = await prisma.user.findUnique({
      where: { id: decoded.userId },
      select: {
        id: true,
        email: true,
        tipoUsuario: true,
        ativo: true
      }
    });

    if (!user || !user.ativo) {
      return res.status(401).json({
        error: true,
        message: 'Token inválido ou usuário inativo'
      });
    }

    req.user = {
      userId: user.id,
      email: user.email,
      tipoUsuario: user.tipoUsuario
    };

    next();
  } catch (error) {
    return res.status(401).json({
      error: true,
      message: 'Token inválido'
    });
  }
};

export const adminMiddleware = (req: AuthRequest, res: Response, next: NextFunction) => {
  if (!req.user) {
    return res.status(401).json({
      error: true,
      message: 'Acesso negado'
    });
  }

  if (req.user.tipoUsuario !== 'ADMINISTRADOR' && req.user.tipoUsuario !== 'DIRETOR') {
    return res.status(403).json({
      error: true,
      message: 'Acesso restrito a administradores'
    });
  }

  next();
};

