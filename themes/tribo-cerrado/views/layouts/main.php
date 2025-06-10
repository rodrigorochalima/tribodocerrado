<?php
/**
 * Tema Tribo do Cerrado
 * Layout principal estilo Orkut para motociclistas
 */

use humhub\widgets\TopMenu;
use humhub\widgets\FooterMenu;
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title><?= Html::encode($this->title) ?> - Tribo do Cerrado</title>
    <link rel="icon" href="/static/img/favicon.ico" type="image/x-icon">
    <link rel="stylesheet" href="/themes/tribo-cerrado/css/theme.css">
    <?php $this->head() ?>
</head>
<body>
<?php $this->beginBody() ?>

<!-- Header estilo Orkut -->
<header class="navbar navbar-default">
    <div class="container">
        <div class="navbar-header">
            <a class="navbar-brand" href="/">
                <img src="/themes/tribo-cerrado/img/LogoTribodoCerrado.png" alt="Tribo do Cerrado">
            </a>
        </div>
        <?= TopMenu::widget() ?>
    </div>
</header>

<!-- Logo principal -->
<div class="logo-container">
    <img src="/themes/tribo-cerrado/img/LogoTribodoCerrado.png" alt="Tribo do Cerrado">
    <div class="motto">
        "Aqui, todas as tribos são uma só.<br>
        Bem-vindo à irmandade do motociclismo."
    </div>
</div>

<!-- Conteúdo principal -->
<div class="container">
    <div class="row">
        <div class="col-md-8">
            <?= $content ?>
        </div>
        <div class="col-md-4">
            <!-- Sidebar estilo Orkut -->
            <div class="sidebar">
                <h4>🏍️ Comunidade</h4>
                <p>Conecte-se com motociclistas de todo o Brasil!</p>
                
                <h4>📅 Eventos</h4>
                <p>Próximos encontros e trilhas</p>
                
                <h4>🛠️ Oficina</h4>
                <p>Dicas e manutenção</p>
            </div>
        </div>
    </div>
</div>

<!-- Footer -->
<footer class="footer">
    <div class="container">
        <p>&copy; 2024 Tribo do Cerrado - Motoclube Goiânia-GO</p>
        <p>Desenvolvido com ❤️ para a irmandade motociclista</p>
        <?= FooterMenu::widget() ?>
    </div>
</footer>

<?php $this->endBody() ?>
</body>
</html>

