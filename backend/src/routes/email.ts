import express, { Request, Response } from 'express';
import nodemailer from 'nodemailer';
import { authMiddleware, AuthRequest } from '../middleware/auth';

const router = express.Router();

// Configurar transporter do Migadu
const transporter = nodemailer.createTransporter({
  host: process.env.EMAIL_HOST,
  port: Number(process.env.EMAIL_PORT),
  secure: process.env.EMAIL_SECURE === 'true',
  auth: {
    user: process.env.EMAIL_USER,
    pass: process.env.EMAIL_PASS
  }
});

// Enviar email
router.post('/send', authMiddleware, async (req: AuthRequest, res) => {
  try {
    const { to, subject, text, html } = req.body;

    if (!to || !subject || (!text && !html)) {
      return res.status(400).json({
        error: true,
        message: 'Destinatário, assunto e conteúdo são obrigatórios'
      });
    }

    const mailOptions = {
      from: `"Tribo do Cerrado" <${process.env.EMAIL_USER}>`,
      to,
      subject,
      text,
      html: html || text
    };

    const info = await transporter.sendMail(mailOptions);

    res.json({
      success: true,
      message: 'Email enviado com sucesso',
      messageId: info.messageId
    });

  } catch (error) {
    console.error('Erro ao enviar email:', error);
    res.status(500).json({
      error: true,
      message: 'Erro ao enviar email'
    });
  }
});

// Testar configuração de email
router.get('/test', authMiddleware, async (req: AuthRequest, res) => {
  try {
    if (req.user!.tipoUsuario !== 'ADMINISTRADOR') {
      return res.status(403).json({
        error: true,
        message: 'Acesso restrito a administradores'
      });
    }

    await transporter.verify();

    res.json({
      success: true,
      message: 'Configuração de email está funcionando'
    });

  } catch (error) {
    console.error('Erro na configuração de email:', error);
    res.status(500).json({
      error: true,
      message: 'Erro na configuração de email',
      details: error.message
    });
  }
});

export default router;

