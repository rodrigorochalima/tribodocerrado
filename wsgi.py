import sys
import os

# Adicionar o diretório atual e o diretório src ao PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.join(current_dir, 'src'))

# Executar migração do banco de dados
print("Executando migração do banco de dados...")
try:
    from src.db_migration import main
    main()
    print("Migração do banco de dados concluída com sucesso!")
except Exception as e:
    print(f"Erro na migração do banco de dados: {e}")

# Importar a aplicação Flask
from src.main import create_app

# Criar a aplicação
application = create_app()

# Para execução local
if __name__ == "__main__":
    application.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
