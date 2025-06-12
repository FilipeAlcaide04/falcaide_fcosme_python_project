""" Script para executar o servidor CNE e realizar a aquisição e limpeza de dados."""
import os
import sys
import shutil
import platform
from pathlib import Path

def clear_terminal():
    """
    Limpa o terminal.
    """
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def executar_comando(comando: str, descricao: str):
    """
    Executa um comando no terminal e verifica se foi bem-sucedido.
        """
    print(f"\n[INFO] {descricao}...")
    resultado = os.system(comando)
    if resultado != 0:
        print(f"\n[ERRO] Falha ao executar: {descricao}.")
        sys.exit(1)

def detectar_comando_python():
    """Detecta o melhor comando Python disponível no sistema."""
    if platform.system() == "Windows":
        for cmd in ["py", "python", "python3"]:
            if shutil.which(cmd):
                return cmd
    else:
        for cmd in ["python3", "python"]:
            if shutil.which(cmd):
                return cmd
    raise EnvironmentError("Nenhum comando Python válido encontrado no sistema.")

def main():
    """Função principal para executar o script de inicialização do servidor CNE."""
    python_cmd = detectar_comando_python()

    run_time_dir = Path("run_time")
    server_file = Path("server_data/cne_server.py")
    data_raw_dir = Path("data/raw")
    data_processed_dir = Path("data/processed")

    aquisition_script = f'{python_cmd} run_time/data_aquisition.py'
    cleaning_script = f'{python_cmd} run_time/data_cleaning_etc.py'
    tests_e_pylint = f'{python_cmd} unit_tests/run_all_tests.py'

    run_time_dir.mkdir(parents=True, exist_ok=True)
    data_raw_dir.mkdir(parents=True, exist_ok=True)
    data_processed_dir.mkdir(parents=True, exist_ok=True)

    executar_comando(aquisition_script, "Aquisição de dados")
    executar_comando(cleaning_script, "Limpeza e processamento de dados")

    clear_terminal()
    executar_comando(tests_e_pylint, "Testes e análise com pylint")

    input("\nPressione Enter para continuar...")

    clear_terminal()
    print("A iniciar o servidor... Aguarde um momento.")
    executar_comando(f'{python_cmd} {server_file.as_posix()}', "Inicialização do servidor")

if __name__ == "__main__":
    main()
