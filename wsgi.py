import sys
import os

# Adicionar o diretório atual ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar a aplicação Flask
from src.main import create_app

# Criar a aplicação
application = create_app()

# Para execução local
if __name__ == "__main__":
    application.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
