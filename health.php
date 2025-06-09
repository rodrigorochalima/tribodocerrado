<?php
/**
 * Health Check para Tribo do Cerrado
 * Endpoint para verificar saúde da aplicação
 */

header('Content-Type: application/json');

$checks = [];
$overallStatus = 'OK';

// Verificar conexão com banco de dados
try {
    $databaseUrl = getenv('DATABASE_URL');
    if ($databaseUrl) {
        $pdo = new PDO($databaseUrl);
        $pdo->query('SELECT 1');
        $checks['database'] = [
            'status' => 'OK',
            'message' => 'Database connection successful'
        ];
    } else {
        $checks['database'] = [
            'status' => 'WARNING',
            'message' => 'DATABASE_URL not configured'
        ];
    }
} catch (Exception $e) {
    $checks['database'] = [
        'status' => 'ERROR',
        'message' => 'Database connection failed: ' . $e->getMessage()
    ];
    $overallStatus = 'ERROR';
}

// Verificar diretórios de upload
$uploadDir = __DIR__ . '/uploads';
if (is_dir($uploadDir) && is_writable($uploadDir)) {
    $checks['uploads_directory'] = [
        'status' => 'OK',
        'message' => 'Uploads directory is writable'
    ];
} else {
    $checks['uploads_directory'] = [
        'status' => 'ERROR',
        'message' => 'Uploads directory is not writable'
    ];
    $overallStatus = 'ERROR';
}

// Verificar diretório runtime
$runtimeDir = __DIR__ . '/protected/runtime';
if (is_dir($runtimeDir) && is_writable($runtimeDir)) {
    $checks['runtime_directory'] = [
        'status' => 'OK',
        'message' => 'Runtime directory is writable'
    ];
} else {
    $checks['runtime_directory'] = [
        'status' => 'ERROR',
        'message' => 'Runtime directory is not writable'
    ];
    $overallStatus = 'ERROR';
}

// Verificar extensões PHP necessárias
$requiredExtensions = ['pdo', 'pdo_pgsql', 'mbstring', 'intl', 'zip', 'gd'];
$missingExtensions = [];

foreach ($requiredExtensions as $ext) {
    if (!extension_loaded($ext)) {
        $missingExtensions[] = $ext;
    }
}

if (empty($missingExtensions)) {
    $checks['php_extensions'] = [
        'status' => 'OK',
        'message' => 'All required PHP extensions are loaded'
    ];
} else {
    $checks['php_extensions'] = [
        'status' => 'ERROR',
        'message' => 'Missing PHP extensions: ' . implode(', ', $missingExtensions)
    ];
    $overallStatus = 'ERROR';
}

// Verificar uso de memória
$memoryUsage = memory_get_usage(true);
$memoryLimit = ini_get('memory_limit');
$memoryLimitBytes = return_bytes($memoryLimit);
$memoryPercentage = ($memoryUsage / $memoryLimitBytes) * 100;

if ($memoryPercentage < 80) {
    $checks['memory_usage'] = [
        'status' => 'OK',
        'message' => sprintf('Memory usage: %.1f%% (%s / %s)', 
            $memoryPercentage, 
            format_bytes($memoryUsage), 
            $memoryLimit
        )
    ];
} else {
    $checks['memory_usage'] = [
        'status' => 'WARNING',
        'message' => sprintf('High memory usage: %.1f%% (%s / %s)', 
            $memoryPercentage, 
            format_bytes($memoryUsage), 
            $memoryLimit
        )
    ];
}

// Ler informações de build se disponível
$buildInfo = [];
if (file_exists(__DIR__ . '/build-info.json')) {
    $buildInfo = json_decode(file_get_contents(__DIR__ . '/build-info.json'), true);
}

// Resposta final
$response = [
    'status' => $overallStatus,
    'timestamp' => date('Y-m-d H:i:s'),
    'service' => 'Tribo do Cerrado',
    'version' => $buildInfo['version'] ?? '1.0.0',
    'build_time' => $buildInfo['build_time'] ?? 'unknown',
    'git_commit' => $buildInfo['git_commit'] ?? 'unknown',
    'environment' => getenv('ENVIRONMENT') ?: 'unknown',
    'checks' => $checks
];

// Definir código de status HTTP
http_response_code($overallStatus === 'OK' ? 200 : 503);

echo json_encode($response, JSON_PRETTY_PRINT);

/**
 * Converter string de tamanho para bytes
 */
function return_bytes($val) {
    $val = trim($val);
    $last = strtolower($val[strlen($val)-1]);
    $val = (int) $val;
    switch($last) {
        case 'g':
            $val *= 1024;
        case 'm':
            $val *= 1024;
        case 'k':
            $val *= 1024;
    }
    return $val;
}

/**
 * Formatar bytes para leitura humana
 */
function format_bytes($bytes, $precision = 2) {
    $units = array('B', 'KB', 'MB', 'GB', 'TB');
    
    for ($i = 0; $bytes > 1024 && $i < count($units) - 1; $i++) {
        $bytes /= 1024;
    }
    
    return round($bytes, $precision) . ' ' . $units[$i];
}

