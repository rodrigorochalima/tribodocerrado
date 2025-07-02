import express, { Request, Response } from 'express';
import multer from 'multer';
import { v2 as cloudinary } from 'cloudinary';
import { authMiddleware, AuthRequest } from '../middleware/auth';
import prisma from '../utils/database';

const router = express.Router();

// Configurar Cloudinary
cloudinary.config({
  cloud_name: process.env.CLOUDINARY_CLOUD_NAME,
  api_key: process.env.CLOUDINARY_API_KEY,
  api_secret: process.env.CLOUDINARY_API_SECRET
});

// Configurar multer para upload em memória
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 5 * 1024 * 1024 // 5MB
  },
  fileFilter: (req, file, cb) => {
    if (file.mimetype.startsWith('image/')) {
      cb(null, true);
    } else {
      cb(new Error('Apenas imagens são permitidas'));
    }
  }
});

// Upload de avatar
router.post('/avatar', authMiddleware, upload.single('avatar'), async (req: AuthRequest, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        error: true,
        message: 'Nenhum arquivo enviado'
      });
    }

    // Upload para Cloudinary
    const result = await new Promise((resolve, reject) => {
      cloudinary.uploader.upload_stream(
        {
          folder: 'tribodocerrado/avatars',
          public_id: `avatar_${req.user!.userId}`,
          transformation: [
            { width: 200, height: 200, crop: 'fill', gravity: 'face' },
            { quality: 'auto', fetch_format: 'auto' }
          ]
        },
        (error, result) => {
          if (error) reject(error);
          else resolve(result);
        }
      ).end(req.file!.buffer);
    }) as any;

    // Atualizar URL do avatar no banco
    await prisma.user.update({
      where: { id: req.user!.userId },
      data: { avatarUrl: result.secure_url }
    });

    res.json({
      success: true,
      message: 'Avatar atualizado com sucesso',
      avatarUrl: result.secure_url
    });

  } catch (error) {
    console.error('Erro no upload do avatar:', error);
    res.status(500).json({
      error: true,
      message: 'Erro no upload da imagem'
    });
  }
});

// Upload de imagem de evento (apenas admins)
router.post('/evento', authMiddleware, upload.single('imagem'), async (req: AuthRequest, res) => {
  try {
    if (req.user!.tipoUsuario !== 'ADMINISTRADOR' && req.user!.tipoUsuario !== 'DIRETOR') {
      return res.status(403).json({
        error: true,
        message: 'Acesso restrito a administradores'
      });
    }

    if (!req.file) {
      return res.status(400).json({
        error: true,
        message: 'Nenhum arquivo enviado'
      });
    }

    // Upload para Cloudinary
    const result = await new Promise((resolve, reject) => {
      cloudinary.uploader.upload_stream(
        {
          folder: 'tribodocerrado/eventos',
          transformation: [
            { width: 800, height: 600, crop: 'fill' },
            { quality: 'auto', fetch_format: 'auto' }
          ]
        },
        (error, result) => {
          if (error) reject(error);
          else resolve(result);
        }
      ).end(req.file!.buffer);
    }) as any;

    res.json({
      success: true,
      message: 'Imagem enviada com sucesso',
      imageUrl: result.secure_url,
      publicId: result.public_id
    });

  } catch (error) {
    console.error('Erro no upload da imagem:', error);
    res.status(500).json({
      error: true,
      message: 'Erro no upload da imagem'
    });
  }
});

export default router;

