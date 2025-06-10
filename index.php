<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tribo do Cerrado - Motoclube</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Arial Black', Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: #fff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .container {
            max-width: 800px;
            padding: 40px 20px;
            background: rgba(0,0,0,0.7);
            border-radius: 15px;
            border: 2px solid #ff4444;
            box-shadow: 0 0 30px rgba(255,68,68,0.3);
        }
        .logo {
            width: 150px;
            height: 150px;
            margin: 0 auto 30px;
            background: #ff4444;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 60px;
            font-weight: bold;
            color: #fff;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        h1 {
            font-size: 3em;
            color: #ff4444;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            letter-spacing: 2px;
        }
        .subtitle {
            font-size: 1.5em;
            margin-bottom: 15px;
            color: #ccc;
            font-style: italic;
        }
        .motto {
            font-size: 1.2em;
            margin-bottom: 40px;
            color: #fff;
            font-weight: bold;
        }
        .status {
            background: #28a745;
            color: #fff;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            font-weight: bold;
            margin: 20px 0;
            display: inline-block;
        }
        .links {
            margin-top: 30px;
        }
        .links a {
            color: #ff4444;
            text-decoration: none;
            margin: 0 15px;
            padding: 10px 20px;
            border: 2px solid #ff4444;
            border-radius: 25px;
            transition: all 0.3s;
            display: inline-block;
            margin-bottom: 10px;
        }
        .links a:hover {
            background: #ff4444;
            color: #fff;
            transform: scale(1.05);
        }
        .footer {
            margin-top: 40px;
            font-size: 0.9em;
            color: #888;
        }
        @media (max-width: 600px) {
            h1 { font-size: 2em; }
            .subtitle { font-size: 1.2em; }
            .motto { font-size: 1em; }
            .container { margin: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">TC</div>
        
        <h1>TRIBO DO CERRADO</h1>
        
        <div class="subtitle">Motoclube Goiânia-GO</div>
        
        <div class="motto">
            "Aqui, todas as tribos são uma só.<br>
            Bem-vindo à irmandade do motociclismo."
        </div>
        
        <div class="status">
            🏍️ SITE FUNCIONANDO! 🏍️
        </div>
        
        <div class="links">
            <a href="/health.php">Health Check</a>
            <a href="mailto:contato@tribodocerrado.com">Contato</a>
        </div>
        
        <div class="footer">
            <p>© 2024 Tribo do Cerrado - Todos os direitos reservados</p>
            <p>Desenvolvido com ❤️ para a irmandade motociclista</p>
        </div>
    </div>
</body>
</html>

