<?php
/**
 * Health Check para Tribo do Cerrado
 * Endpoint para verificação de saúde da aplicação
 */

header('Content-Type: application/json');

$health = [
    'status' => 'OK',
    'timestamp' => date('Y-m-d H:i:s'),
    'service' => 'Tribo do Cerrado',
    'version' => '1.0.0',
    'checks' => []
];

try {
    // Verificar conexão com banco de dados
    $dbConfig = require __DIR__ . '/protected/config/common.php';
    $dsn = $dbConfig['components']['db']['dsn'] ?? '';
    
    if (strpos($dsn, 'pgsql:') === 0) {
        // Extrair informações de conexão
        preg_match('/host=([^;]+)/', $dsn, $hostMatch);
        preg_match('/port=([^;]+)/', $dsn, $portMatch);
        preg_match('/dbname=([^;]+)/', $dsn, $dbnameMatch);
        
        $host = $hostMatch[1] ?? 'localhost';
        $port = $portMatch[1] ?? '5432';
        $dbname = $dbnameMatch[1] ?? '';
        
        $username = $dbConfig['components']['db']['username'] ?? '';
        $password = $dbConfig['components']['db']['password'] ?? '';
        
        try {
            $pdo = new PDO($dsn, $username, $password, [
                PDO::ATTR_TIMEOUT => 5,
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION
            ]);
            
            $stmt = $pdo->query('SELECT 1');
            $health['checks']['database'] = [
                'status' => 'OK',
                'message' => 'Database connection successful',
                'host' => $host,
                'port' => $port,
                'database' => $dbname
            ];
        } catch (PDOException $e) {
            $health['checks']['database'] = [
                'status' => 'ERROR',
                'message' => 'Database connection failed: ' . $e->getMessage(),
                'host' => $host,
                'port' => $port
            ];
            $health['status'] = 'ERROR';
        }
    } else {
        $health['checks']['database'] = [
            'status' => 'WARNING',
            'message' => 'Database configuration not found or invalid'
        ];
    }
    
    // Verificar diretórios de escrita
    $writableDirs = [
        'uploads' => __DIR__ . '/uploads',
        'runtime' => __DIR__ . '/protected/runtime',
        'assets' => __DIR__ . '/assets'
    ];
    
    foreach ($writableDirs as $name => $dir) {
        if (is_dir($dir) && is_writable($dir)) {
            $health['checks'][$name . '_directory'] = [
                'status' => 'OK',
                'message' => "Directory $dir is writable",
                'path' => $dir
            ];
        } else {
            $health['checks'][$name . '_directory'] = [
                'status' => 'ERROR',
                'message' => "Directory $dir is not writable or doesn't exist",
                'path' => $dir
            ];
            $health['status'] = 'ERROR';
        }
    }
    
    // Verificar extensões PHP necessárias
    $requiredExtensions = [
        'pdo', 'pdo_pgsql', 'pgsql', 'mbstring', 'xml', 'zip', 
        'bcmath', 'intl', 'gd', 'curl', 'json'
    ];
    
    $missingExtensions = [];
    foreach ($requiredExtensions as $ext) {
        if (!extension_loaded($ext)) {
            $missingExtensions[] = $ext;
        }
    }
    
    if (empty($missingExtensions)) {
        $health['checks']['php_extensions'] = [
            'status' => 'OK',
            'message' => 'All required PHP extensions are loaded',
            'extensions' => $requiredExtensions
        ];
    } else {
        $health['checks']['php_extensions'] = [
            'status' => 'ERROR',
            'message' => 'Missing required PHP extensions',
            'missing' => $missingExtensions,
            'required' => $requiredExtensions
        ];
        $health['status'] = 'ERROR';
    }
    
    // Verificar configurações críticas
    $criticalSettings = [
        'memory_limit' => ini_get('memory_limit'),
        'upload_max_filesize' => ini_get('upload_max_filesize'),
        'post_max_size' => ini_get('post_max_size'),
        'max_execution_time' => ini_get('max_execution_time')
    ];
    
    $health['checks']['php_settings'] = [
        'status' => 'OK',
        'message' => 'PHP settings',
        'settings' => $criticalSettings
    ];
    
    // Verificar espaço em disco
    $diskFree = disk_free_space(__DIR__);
    $diskTotal = disk_total_space(__DIR__);
    $diskUsed = $diskTotal - $diskFree;
    $diskUsagePercent = round(($diskUsed / $diskTotal) * 100, 2);
    
    $health['checks']['disk_space'] = [
        'status' => $diskUsagePercent > 90 ? 'WARNING' : 'OK',
        'message' => "Disk usage: {$diskUsagePercent}%",
        'free' => formatBytes($diskFree),
        'total' => formatBytes($diskTotal),
        'used' => formatBytes($diskUsed),
        'usage_percent' => $diskUsagePercent
    ];
    
    // Verificar memória
    $memoryUsage = memory_get_usage(true);
    $memoryPeak = memory_get_peak_usage(true);
    $memoryLimit = ini_get('memory_limit');
    
    $health['checks']['memory'] = [
        'status' => 'OK',
        'message' => 'Memory usage',
        'current' => formatBytes($memoryUsage),
        'peak' => formatBytes($memoryPeak),
        'limit' => $memoryLimit
    ];
    
    // Informações do sistema
    $health['system'] = [
        'php_version' => PHP_VERSION,
        'server_software' => $_SERVER['SERVER_SOFTWARE'] ?? 'Unknown',
        'operating_system' => PHP_OS,
        'server_time' => date('Y-m-d H:i:s'),
        'timezone' => date_default_timezone_get(),
        'load_average' => function_exists('sys_getloadavg') ? sys_getloadavg() : null
    ];
    
    // Verificar se há erros críticos
    $errorCount = 0;
    foreach ($health['checks'] as $check) {
        if ($check['status'] === 'ERROR') {
            $errorCount++;
        }
    }
    
    if ($errorCount > 0) {
        $health['status'] = 'ERROR';
        $health['error_count'] = $errorCount;
    }
    
} catch (Exception $e) {
    $health['status'] = 'ERROR';
    $health['error'] = $e->getMessage();
}

// Definir código de status HTTP baseado na saúde
http_response_code($health['status'] === 'OK' ? 200 : 503);

// Retornar resposta JSON
echo json_encode($health, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);

/**
 * Formatar bytes em formato legível
 */
function formatBytes($bytes, $precision = 2) {
    $units = array('B', 'KB', 'MB', 'GB', 'TB');
    
    for ($i = 0; $bytes > 1024 && $i < count($units) - 1; $i++) {
        $bytes /= 1024;
    }
    
    return round($bytes, $precision) . ' ' . $units[$i];
}

