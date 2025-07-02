import express, { Request, Response } from 'express';
import { authMiddleware, AuthRequest } from '../middleware/auth';
import prisma from '../utils/database';

const router = express.Router();

// Buscar perfil do usuário logado
router.get('/profile', authMiddleware, async (req: AuthRequest, res) => {
  try {
    const userId = req.user!.userId;

    const user = await prisma.user.findUnique({
      where: { id: userId },
      include: {
        familiares: true,
        premios: true,
        motos: true,
        participacoes: {
          include: {
            evento: {
              select: {
                id: true,
                titulo: true,
                dataEvento: true,
                localEvento: true
              }
            }
          }
        }
      }
    });

    if (!user) {
      return res.status(404).json({
        error: true,
        message: 'Usuário não encontrado'
      });
    }

    // Remover senha da resposta
    const { password, ...userWithoutPassword } = user;

    res.json({
      success: true,
      user: userWithoutPassword
    });

  } catch (error) {
    console.error('Erro ao buscar perfil:', error);
    res.status(500).json({
      error: true,
      message: 'Erro interno do servidor'
    });
  }
});

// Atualizar perfil
router.put('/profile', authMiddleware, async (req: AuthRequest, res) => {
  try {
    const userId = req.user!.userId;
    const { nomeCompleto, telefone, cidade, estado, dataNascimento } = req.body;

    const user = await prisma.user.update({
      where: { id: userId },
      data: {
        nomeCompleto,
        telefone,
        cidade,
        estado,
        ...(dataNascimento && { dataNascimento: new Date(dataNascimento) })
      },
      select: {
        id: true,
        email: true,
        nomeCompleto: true,
        telefone: true,
        cidade: true,
        estado: true,
        dataNascimento: true,
        tipoUsuario: true,
        avatarUrl: true,
        updatedAt: true
      }
    });

    res.json({
      success: true,
      message: 'Perfil atualizado com sucesso',
      user
    });

  } catch (error) {
    console.error('Erro ao atualizar perfil:', error);
    res.status(500).json({
      error: true,
      message: 'Erro interno do servidor'
    });
  }
});

// Adicionar familiar
router.post('/familiares', authMiddleware, async (req: AuthRequest, res) => {
  try {
    const userId = req.user!.userId;
    const { nome, parentesco, idade, telefone } = req.body;

    const familiar = await prisma.familiar.create({
      data: {
        nome,
        parentesco,
        idade: idade ? Number(idade) : null,
        telefone,
        userId
      }
    });

    res.status(201).json({
      success: true,
      message: 'Familiar adicionado com sucesso',
      familiar
    });

  } catch (error) {
    console.error('Erro ao adicionar familiar:', error);
    res.status(500).json({
      error: true,
      message: 'Erro interno do servidor'
    });
  }
});

// Adicionar moto
router.post('/motos', authMiddleware, async (req: AuthRequest, res) => {
  try {
    const userId = req.user!.userId;
    const { marca, modelo, ano, cor, cilindrada, placa, principal } = req.body;

    // Se esta moto for principal, remover principal das outras
    if (principal) {
      await prisma.moto.updateMany({
        where: { userId },
        data: { principal: false }
      });
    }

    const moto = await prisma.moto.create({
      data: {
        marca,
        modelo,
        ano: Number(ano),
        cor,
        cilindrada,
        placa,
        principal: Boolean(principal),
        userId
      }
    });

    res.status(201).json({
      success: true,
      message: 'Moto adicionada com sucesso',
      moto
    });

  } catch (error) {
    console.error('Erro ao adicionar moto:', error);
    res.status(500).json({
      error: true,
      message: 'Erro interno do servidor'
    });
  }
});

// Adicionar prêmio
router.post('/premios', authMiddleware, async (req: AuthRequest, res) => {
  try {
    const userId = req.user!.userId;
    const { titulo, descricao, categoria, ano, posicao } = req.body;

    const premio = await prisma.premio.create({
      data: {
        titulo,
        descricao,
        categoria,
        ano: Number(ano),
        posicao,
        userId
      }
    });

    res.status(201).json({
      success: true,
      message: 'Prêmio adicionado com sucesso',
      premio
    });

  } catch (error) {
    console.error('Erro ao adicionar prêmio:', error);
    res.status(500).json({
      error: true,
      message: 'Erro interno do servidor'
    });
  }
});

export default router;

