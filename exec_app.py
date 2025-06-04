""" Este script executa a aplição na ordem correta simplificando o processo de execução"""
# Os ficheiros que serão executados encontram-se nas pastas "run_time" e "server_data"

import os
import platform

def clear_terminal():
    if platform.system() == "Windows":
        os.system('cls')
    else:  # Linux e macOS 
        os.system('clear')

def main():
    
    # Verifica se o diretório 'run_time' existe
    if not os.path.exists('run_time'):
        print("O diretório 'run_time' não existe. Certifique-se de que está no diretório correto.")
        return

    # Instala as dependências necessárias
    os.system('python3 run_time/requirements.py')

    # Executa o script para ir buscar os dados
    if not os.path.exists('data/raw'):
        print("O diretório 'data/raw' não existe. ERRO GRAVE! mas mesmo muito grave! nem estás a entnder é mesmo MUITO grave!")
        return
    os.system('python3 run_time/1-data_aquisition.py')

    # Executa o script de limpeza e tratamento de dados
    if not os.path.exists('data/processed'):
        print("O diretório 'data/processed' não existe. Certifique-se de que o script de limpeza foi executado corretamente.")
        return
    os.system('python3 run_time/2-data_cleaning_etc.py')

    # Executa o script que vai começar o server para uma view mesmo bonita, algo que o utilizador vai gostar de ver (espero eu :)
    #
    if not os.path.exists('server_data/cne_server.py'):
        print("O script 'cne_server.py' não foi encontrado. Certifique-se de que está no diretório correto.")
        return
    #clear_terminal()
    print("A iniciar o servidor... Aguarde um momento.")
    os.system('python3 server_data/cne_server.py')

if __name__ == "__main__":
    main()