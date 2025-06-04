""" Este script executa a aplicação na ordem correta, simplificando o processo de execução. """
import os
import platform
import subprocess
import sys
from pathlib import Path

def clear_terminal():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def run_script(script_path):
    """Executa um script Python e trata erros de execução."""
    try:
        result = subprocess.run(['python3', script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] Falha ao executar {script_path}: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print(f"[ERRO] Python3 não encontrado. Verifique se está instalado e no PATH.")
        sys.exit(1)

def main():
    try:
        # Verifica diretório 'run_time'
        if not os.path.exists('run_time'):
            print("[ERRO] O diretório 'run_time' não existe. Certifique-se de que está no diretório correto.")
            sys.exit(1)

        # Instala as dependências necessárias
        run_script('run_time/requirements.py')

        # Verifica diretório 'data/raw' e executa aquisição de dados
        if not os.path.exists('data/raw'):
            print("[ERRO GRAVE] O diretório 'data/raw' não existe. É realmente muito grave! Verifique o fluxo de dados.")
            sys.exit(1)
        run_script('run_time/1-data_aquisition.py')

        # Verifica diretório 'data/processed'
        if not os.path.exists('data/processed'):
            print("[INFO] Diretório 'data/processed' não encontrado. Criando diretório...")
            os.makedirs('data/processed', exist_ok=True)
        
        # Executa limpeza e tratamento de dados
        run_script('run_time/2-data_cleaning_etc.py')

        # Verifica se script do servidor existe
        server_script = 'server_data/cne_server.py'
        if not os.path.exists(server_script):
            print(f"[ERRO] O script '{server_script}' não foi encontrado.")
            sys.exit(1)

        clear_terminal()
        print("A iniciar o servidor... Aguarde um momento.")
        run_script(server_script)

    except Exception as e:
        print(f"[ERRO INESPERADO] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
