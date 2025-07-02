import express, { Request, Response } from 'express';
import { body, validationResult } from 'express-validator';
import prisma from '../utils/database';
import { authMiddleware } from '../middleware/auth';

const router = express.Router();

// Listar eventos (público)
router.get('/', async (req: Request, res: Response) => {
  try {
    const { page = 1, limit = 10, upcoming = 'true' } = req.query;
    
    const skip = (Number(page) - 1) * Number(limit);
    const take = Number(limit);

    const where = {
      ativo: true,
      ...(upcoming === 'true' && {
        dataEvento: {
          gte: new Date()
        }
      })
    };

    const [eventos, total] = await Promise.all([
      prisma.evento.findMany({
        where,
        include: {
          participacoes: {
            where: { confirmado: true },
            include: {
              user: {
                select: {
                  id: true,
                  nomeCompleto: true,
                  avatarUrl: true
                }
              }
            }
          },
          comboios: {
            where: { ativo: true },
            include: {
              lider: {
                select: {
                  id: true,
                  nomeCompleto: true
                }
              }
            }
          }
        },
        orderBy: {
          dataEvento: 'asc'
        },
        skip,
        take
      }),
      prisma.evento.count({ where })
    ]);

    // Adicionar contadores
    const eventosComContadores = eventos.map(evento => ({
      ...evento,
      participantesConfirmados: evento.participacoes.length,
      comboiosOrganizados: evento.comboios.length
    }));

    res.json({
      success: true,
      eventos: eventosComContadores,
      pagination: {
        page: Number(page),
        limit: Number(limit),
        total,
        pages: Math.ceil(total / Number(limit))
      }
    });

  } catch (error) {
    console.error('Erro ao listar eventos:', error);
    res.status(500).json({
      error: true,
      message: 'Erro interno do servidor'
    });
  }
});

// Buscar evento por ID
router.get('/:id', async (req: Request, res: Response) => {
  try {
    const { id } = req.params;

    const evento = await prisma.evento.findUnique({
      where: { id },
      include: {
        participacoes: {
          include: {
            user: {
              select: {
                id: true,
                nomeCompleto: true,
                avatarUrl: true,
                cidade: true
              }
            }
          }
        },
        comboios: {
          include: {
            lider: {
              select: {
                id: true,
                nomeCompleto: true,
                telefone: true
              }
            }
          }
        }
      }
    });

    if (!evento) {
      return res.status(404).json({
        error: true,
        message: 'Evento não encontrado'
      });
    }

    res.json({
      success: true,
      evento: {
        ...evento,
        participantesConfirmados: evento.participacoes.filter(p => p.confirmado).length,
        comboiosOrganizados: evento.comboios.filter(c => c.ativo).length
      }
    });

  } catch (error) {
    console.error('Erro ao buscar evento:', error);
    res.status(500).json({
      error: true,
      message: 'Erro interno do servidor'
    });
  }
});

// Participar de evento (requer autenticação)
router.post('/:id/participar', authMiddleware, async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const userId = req.user!.userId;
    const { observacoes } = req.body;

    // Verificar se evento existe
    const evento = await prisma.evento.findUnique({
      where: { id },
      include: {
        participacoes: {
          where: { confirmado: true }
        }
      }
    });

    if (!evento) {
      return res.status(404).json({
        error: true,
        message: 'Evento não encontrado'
      });
    }

    // Verificar se evento já passou
    if (evento.dataEvento < new Date()) {
      return res.status(400).json({
        error: true,
        message: 'Não é possível participar de eventos que já aconteceram'
      });
    }

    // Verificar limite de participantes
    if (evento.participantesMaximo && evento.participacoes.length >= evento.participantesMaximo) {
      return res.status(400).json({
        error: true,
        message: 'Evento lotado'
      });
    }

    // Criar ou atualizar participação
    const participacao = await prisma.participacaoEvento.upsert({
      where: {
        userId_eventoId: {
          userId,
          eventoId: id
        }
      },
      update: {
        confirmado: true,
        dataConfirmacao: new Date(),
        observacoes
      },
      create: {
        userId,
        eventoId: id,
        confirmado: true,
        dataConfirmacao: new Date(),
        observacoes
      },
      include: {
        user: {
          select: {
            nomeCompleto: true,
            email: true
          }
        },
        evento: {
          select: {
            titulo: true,
            dataEvento: true
          }
        }
      }
    });

    res.json({
      success: true,
      message: 'Participação confirmada com sucesso!',
      participacao
    });

  } catch (error) {
    console.error('Erro ao participar do evento:', error);
    res.status(500).json({
      error: true,
      message: 'Erro interno do servidor'
    });
  }
});

// Cancelar participação
router.delete('/:id/participar', authMiddleware, async (req: Request, res: Response) => {
  try {
    const { id } = req.params;
    const userId = req.user!.userId;

    await prisma.participacaoEvento.delete({
      where: {
        userId_eventoId: {
          userId,
          eventoId: id
        }
      }
    });

    res.json({
      success: true,
      message: 'Participação cancelada com sucesso'
    });

  } catch (error) {
    console.error('Erro ao cancelar participação:', error);
    res.status(500).json({
      error: true,
      message: 'Erro interno do servidor'
    });
  }
});

// Criar comboio (requer autenticação)
router.post('/:id/comboios', authMiddleware, [
  body('nome').isLength({ min: 3 }).trim(),
  body('pontoEncontro').isLength({ min: 5 }).trim(),
  body('horarioSaida').isISO8601(),
  body('vagas').isInt({ min: 1, max: 50 })
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

    const { id } = req.params;
    const userId = req.user!.userId;
    const { nome, descricao, pontoEncontro, horarioSaida, vagas } = req.body;

    // Verificar se evento existe
    const evento = await prisma.evento.findUnique({
      where: { id }
    });

    if (!evento) {
      return res.status(404).json({
        error: true,
        message: 'Evento não encontrado'
      });
    }

    // Criar comboio
    const comboio = await prisma.comboioEvento.create({
      data: {
        nome,
        descricao,
        pontoEncontro,
        horarioSaida: new Date(horarioSaida),
        vagas: Number(vagas),
        eventoId: id,
        liderUserId: userId
      },
      include: {
        lider: {
          select: {
            nomeCompleto: true,
            telefone: true
          }
        },
        evento: {
          select: {
            titulo: true
          }
        }
      }
    });

    res.status(201).json({
      success: true,
      message: 'Comboio criado com sucesso!',
      comboio
    });

  } catch (error) {
    console.error('Erro ao criar comboio:', error);
    res.status(500).json({
      error: true,
      message: 'Erro interno do servidor'
    });
  }
});

export default router;

