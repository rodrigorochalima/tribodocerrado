<?php
header('Content-Type: application/json');

$status = 'OK';
$checks = [];

// Verificar banco de dados
try {
    if ($db = getenv('DATABASE_URL')) {
        $pdo = new PDO($db);
        $checks['database'] = 'OK';
    } else {
        $checks['database'] = 'WARNING - No DATABASE_URL';
    }
} catch (Exception $e) {
    $checks['database'] = 'ERROR';
    $status = 'ERROR';
}

// Verificar diretórios
$dirs = ['uploads', 'protected/runtime', 'assets'];
foreach ($dirs as $dir) {
    $checks[$dir] = (is_dir($dir) && is_writable($dir)) ? 'OK' : 'ERROR';
    if ($checks[$dir] === 'ERROR') $status = 'ERROR';
}

// Verificar extensões PHP
$exts = ['pdo', 'pdo_pgsql', 'mbstring', 'intl', 'zip', 'gd'];
$missing = array_filter($exts, fn($ext) => !extension_loaded($ext));
$checks['php_extensions'] = empty($missing) ? 'OK' : 'MISSING: ' . implode(', ', $missing);
if (!empty($missing)) $status = 'ERROR';

// Resposta
echo json_encode([
    'status' => $status,
    'timestamp' => date('Y-m-d H:i:s'),
    'service' => 'Tribo do Cerrado',
    'checks' => $checks
], JSON_PRETTY_PRINT);

http_response_code($status === 'OK' ? 200 : 503);

