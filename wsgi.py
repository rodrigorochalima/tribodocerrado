import sys
import os

# Adicionar o diretório atual ao PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Executar migração do banco de dados
print("Executando migração do banco de dados...")
try:
    from src.db_migration import main as db_migration_main
    db_migration_main()
    print("Migração do banco de dados concluída com sucesso!")
except Exception as e:
    print(f"Erro na migração do banco de dados: {e}")

# Importar a aplicação Flask
try:
    from src.main import create_app
    # Criar a aplicação
    application = create_app()
    print("Aplicação Flask criada com sucesso!")
except Exception as e:
    print(f"Erro ao criar aplicação Flask: {e}")
    raise

# Para execução local
if __name__ == "__main__":
    application.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
