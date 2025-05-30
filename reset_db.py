#!/usr/bin/env python3
"""
Script para reiniciar completamente o banco de dados do Tribo do Cerrado.
Este script remove o banco de dados existente e recria todas as tabelas do zero.
"""

import os
import sys
import shutil
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho absoluto para o banco de dados
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, 'src', 'instance')
DB_PATH = os.path.join(INSTANCE_DIR, 'tribo_cerrado.db')

def reset_database():
    """Remove o banco de dados existente e recria o diretório instance"""
    logger.info("Iniciando reset completo do banco de dados")
    
    # Verificar se o diretório instance existe
    if os.path.exists(INSTANCE_DIR):
        logger.info(f"Removendo diretório instance: {INSTANCE_DIR}")
        shutil.rmtree(INSTANCE_DIR)
    
    # Recriar o diretório instance
    logger.info(f"Recriando diretório instance: {INSTANCE_DIR}")
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    
    logger.info("Reset do banco de dados concluído com sucesso")
    logger.info("Execute o script de migração para criar as tabelas: python src/db_migration.py")

if __name__ == "__main__":
    # Confirmar com o usuário
    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        reset_database()
    else:
        confirm = input("ATENÇÃO: Este script irá remover completamente o banco de dados. Todos os dados serão perdidos. Continuar? (s/N): ")
        if confirm.lower() == 's':
            reset_database()
        else:
            logger.info("Operação cancelada pelo usuário")
