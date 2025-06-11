<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tribo do Cerrado - Rede Social Motociclista</title>
    <link rel="icon" type="image/png" href="/static/img/favicon.ico">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Cinzel', 'Times New Roman', serif;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 50%, #1a1a1a 100%);
            background-image: 
                radial-gradient(circle at 20% 80%, rgba(255, 69, 0, 0.3) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 140, 0, 0.2) 0%, transparent 50%),
                url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="%23333" opacity="0.3"/><circle cx="75" cy="75" r="1" fill="%23333" opacity="0.3"/><circle cx="50" cy="10" r="0.5" fill="%23444" opacity="0.4"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }

        body::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(ellipse at center, transparent 30%, rgba(0,0,0,0.8) 100%),
                linear-gradient(45deg, transparent 40%, rgba(139, 69, 19, 0.1) 50%, transparent 60%);
            pointer-events: none;
        }

        .login-container {
            background: rgba(0, 0, 0, 0.9);
            border: 3px solid #8B4513;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 
                0 0 50px rgba(255, 69, 0, 0.5),
                inset 0 0 30px rgba(139, 69, 19, 0.3),
                0 0 100px rgba(0, 0, 0, 0.8);
            text-align: center;
            max-width: 500px;
            width: 90%;
            position: relative;
            backdrop-filter: blur(10px);
        }

        .login-container::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            background: linear-gradient(45deg, #FF4500, #8B4513, #FF6347, #8B4513);
            border-radius: 22px;
            z-index: -1;
            animation: borderGlow 3s ease-in-out infinite alternate;
        }

        @keyframes borderGlow {
            0% { opacity: 0.7; }
            100% { opacity: 1; }
        }

        .title {
            color: #D4AF37;
            font-size: 2.5rem;
            font-weight: bold;
            text-shadow: 
                3px 3px 6px rgba(0, 0, 0, 0.8),
                0 0 20px rgba(212, 175, 55, 0.5);
            margin-bottom: 10px;
            letter-spacing: 2px;
            text-transform: uppercase;
        }

        .subtitle {
            color: #D4AF37;
            font-size: 3rem;
            font-weight: bold;
            text-shadow: 
                3px 3px 6px rgba(0, 0, 0, 0.8),
                0 0 25px rgba(212, 175, 55, 0.6);
            margin-bottom: 30px;
            letter-spacing: 3px;
            text-transform: uppercase;
        }

        .logo-container {
            margin: 30px 0;
            position: relative;
        }

        .logo {
            width: 200px;
            height: 200px;
            border-radius: 50%;
            border: 4px solid #8B4513;
            box-shadow: 
                0 0 30px rgba(255, 69, 0, 0.7),
                inset 0 0 20px rgba(139, 69, 19, 0.3);
            animation: logoGlow 2s ease-in-out infinite alternate;
            background: linear-gradient(135deg, #D4AF37 0%, #FFD700 50%, #D4AF37 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            position: relative;
        }

        @keyframes logoGlow {
            0% { box-shadow: 0 0 30px rgba(255, 69, 0, 0.7), inset 0 0 20px rgba(139, 69, 19, 0.3); }
            100% { box-shadow: 0 0 50px rgba(255, 69, 0, 1), inset 0 0 30px rgba(139, 69, 19, 0.5); }
        }

        .logo-text {
            color: #8B4513;
            font-size: 1.2rem;
            font-weight: bold;
            text-align: center;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
        }

        .form-group {
            margin-bottom: 20px;
            text-align: left;
        }

        .form-group input {
            width: 100%;
            padding: 15px;
            background: rgba(0, 0, 0, 0.8);
            border: 2px solid #8B4513;
            border-radius: 10px;
            color: #D4AF37;
            font-size: 1.1rem;
            transition: all 0.3s ease;
        }

        .form-group input:focus {
            outline: none;
            border-color: #FF4500;
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.5);
            background: rgba(0, 0, 0, 0.9);
        }

        .form-group input::placeholder {
            color: #888;
        }

        .checkbox-container {
            display: flex;
            align-items: center;
            margin: 20px 0;
            color: #D4AF37;
        }

        .checkbox-container input[type="checkbox"] {
            width: auto;
            margin-right: 10px;
            transform: scale(1.2);
        }

        .btn-entrar {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #8B4513 0%, #A0522D 50%, #8B4513 100%);
            border: 2px solid #D4AF37;
            border-radius: 10px;
            color: #D4AF37;
            font-size: 1.3rem;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.8);
        }

        .btn-entrar:hover {
            background: linear-gradient(135deg, #A0522D 0%, #CD853F 50%, #A0522D 100%);
            box-shadow: 0 0 20px rgba(212, 175, 55, 0.6);
            transform: translateY(-2px);
        }

        .welcome-text {
            color: #D4AF37;
            font-size: 1.2rem;
            margin-top: 30px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
            line-height: 1.6;
        }

        .skulls {
            position: absolute;
            width: 60px;
            height: 60px;
            opacity: 0.3;
        }

        .skull-left {
            top: 20px;
            left: -30px;
            transform: rotate(-15deg);
        }

        .skull-right {
            top: 20px;
            right: -30px;
            transform: rotate(15deg);
        }

        @media (max-width: 768px) {
            .title { font-size: 1.8rem; }
            .subtitle { font-size: 2.2rem; }
            .logo { width: 150px; height: 150px; }
            .login-container { padding: 30px 20px; }
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h1 class="title">Bem-vindo à</h1>
        <h2 class="subtitle">Tribo do Cerrado</h2>
        
        <div class="logo-container">
            <div class="logo">
                <div class="logo-text">
                    Tribo do<br>
                    Cerrado<br>
                    <small>M &nbsp;&nbsp;&nbsp;&nbsp; C</small><br>
                    <small>GOIÂNIA-GO</small>
                </div>
            </div>
        </div>

        <form method="POST" action="/login">
            <div class="form-group">
                <input type="email" name="email" placeholder="E-mail" required>
            </div>
            
            <div class="form-group">
                <input type="password" name="password" placeholder="Senha" required>
            </div>
            
            <div class="checkbox-container">
                <input type="checkbox" name="remember" id="remember">
                <label for="remember">Lembrar de mim</label>
            </div>
            
            <button type="submit" class="btn-entrar">Entrar</button>
        </form>

        <div class="welcome-text">
            A Tribo do Cerrado recebe todas<br>
            as tribos do motociclismo.<br>
            Sejam bem-vindos.
        </div>
    </div>
</body>
</html>

