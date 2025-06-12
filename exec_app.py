""" 
Este script executa a aplicação na ordem correta simplificando o processo de execução
"""
# Os ficheiros que serão executados encontram-se nas pastas "run_time" e "server_data"

import os
import platform
from pathlib import Path

def clear_terminal():
    """Limpa o terminal, dependendo do sistema operativo."""
    if platform.system() == "Windows":
        os.system('cls')
    else:  # Linux e macOS
        os.system('clear')

def main():
    """ Função principal que executa a aplicação."""
    # Diretórios e ficheiros essenciais
    run_time_dir = Path("run_time")
    server_file = Path("server_data/cne_server.py")
    data_raw_dir = Path("data/raw")
    data_processed_dir = Path("data/processed")
    req = 'python3 run_time/requirements.py'
    aquisition_script = 'python3 run_time/data_aquisition.py'
    cleaning_script = 'python3 run_time/data_cleaning_etc.py'

    tests_e_pylint = 'python3 unit_tests/run_all_tests.py'

    # Garante que os diretórios existem
    run_time_dir.mkdir(parents=True, exist_ok=True)
    data_raw_dir.mkdir(parents=True, exist_ok=True)
    data_processed_dir.mkdir(parents=True, exist_ok=True)

    # Instala as dependências necessárias
    os.system(req)

    # Executa o script para ir buscar os dados
    os.system(aquisition_script)

    # Executa o script de limpeza e tratamento de dados
    os.system(cleaning_script)

    # Executa os testes e o pylint
    clear_terminal()
    os.system(tests_e_pylint)
      
    # Aguarda que o user pressione Enter para continuar
    input("Pressione Enter para continuar...")

    # Inicia o servidor
    clear_terminal()
    print("A iniciar o servidor... Aguarde um momento.")
    os.system('python3 ' + str(server_file))

if __name__ == "__main__":
    main()
