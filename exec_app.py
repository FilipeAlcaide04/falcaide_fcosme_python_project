""" 
Este script executa a aplicação na ordem correta simplificando o processo de execução
"""
# Os ficheiros que serão executados encontram-se nas pastas "run_time" e "server_data"

import os
import platform
from pathlib import Path

def clear_terminal():
    if platform.system() == "Windows":
        os.system('cls')
    else:  # Linux e macOS 
        os.system('clear')

def create_dummy_file(path: Path, content: str = "# Dummy file\n"):
    """Cria um ficheiro com conteúdo básico se ele não existir."""
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)  # Garante que o diretório existe
        with open(path, 'w') as f:
            f.write(content)
        print(f"[INFO] Ficheiro criado: {path}")

def main():
    # Diretórios e ficheiros essenciais
    run_time_dir = Path("run_time")
    server_file = Path("server_data/cne_server.py")
    data_raw_dir = Path("data/raw")
    data_processed_dir = Path("data/processed")

    # Garante que os diretórios existem
    run_time_dir.mkdir(parents=True, exist_ok=True)
    data_raw_dir.mkdir(parents=True, exist_ok=True)
    data_processed_dir.mkdir(parents=True, exist_ok=True)

    # Garante que os ficheiros principais existem (cria dummy se necessário)
    create_dummy_file(run_time_dir / "requirements.py", "#!/usr/bin/env python3\nprint('Installing requirements...')")
    create_dummy_file(run_time_dir / "1-data_aquisition.py", "#!/usr/bin/env python3\nprint('Aquiring data...')")
    create_dummy_file(run_time_dir / "2-data_cleaning_etc.py", "#!/usr/bin/env python3\nprint('Cleaning data...')")
    create_dummy_file(server_file, "#!/usr/bin/env python3\nprint('Starting server...')")

    # Instala as dependências necessárias
    os.system('python3 run_time/requirements.py')

    # Executa o script para ir buscar os dados
    os.system('python3 run_time/1-data_aquisition.py')

    # Executa o script de limpeza e tratamento de dados
    os.system('python3 run_time/2-data_cleaning_etc.py')

    # Inicia o servidor
    clear_terminal()
    print("A iniciar o servidor... Aguarde um momento.")
    os.system('python3 server_data/cne_server.py')

if __name__ == "__main__":
    main()
