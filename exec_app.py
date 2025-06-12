"""
Este script executa a aplicação na ordem correta, simplificando o processo de execução.
"""

import os
import platform
import sys
from pathlib import Path

def clear_terminal():
    """Limpa o terminal, dependendo do sistema operativo."""
    if platform.system() == "Windows":
        os.system('cls')
    else:  # Linux e macOS
        os.system('clear')

def executar_comando(comando: str, descricao: str):
    """Executa um comando e cancela tudo se houver erro."""
    print(f"\n[INFO] {descricao}...")
    resultado = os.system(comando)
    if resultado != 0:
        print(f"\n[ERRO] Falha ao executar: {descricao}.")
        sys.exit(1)

def main():
    """Função principal que executa a aplicação."""
    # Diretórios e ficheiros essenciais
    run_time_dir = Path("run_time")
    server_file = Path("server_data/cne_server.py")
    data_raw_dir = Path("data/raw")
    data_processed_dir = Path("data/processed")

    aquisition_script = 'python3 run_time/data_aquisition.py'
    cleaning_script = 'python3 run_time/data_cleaning_etc.py'
    tests_e_pylint = 'python3 unit_tests/run_all_tests.py'

    # Garante que os diretórios existem
    run_time_dir.mkdir(parents=True, exist_ok=True)
    data_raw_dir.mkdir(parents=True, exist_ok=True)
    data_processed_dir.mkdir(parents=True, exist_ok=True)

    # Etapas da execução
    executar_comando(aquisition_script, "Aquisição de dados")
    executar_comando(cleaning_script, "Limpeza e processamento de dados")

    clear_terminal()
    executar_comando(tests_e_pylint, "Testes e análise com pylint")

    input("\nPressione Enter para continuar...")

    clear_terminal()
    print("A iniciar o servidor... Aguarde um momento.")
    executar_comando(f'python3 {server_file}', "Inicialização do servidor")

if __name__ == "__main__":
    main()
