import csv
import json

arquivo_csv = 'data\processed\dados_regionais_processed.csv'
arquivo_json = 'dados.json'

# Ler CSV e converter para lista de dicionários
with open(arquivo_csv, mode='r', encoding='utf-8') as arquivo:
    leitor = csv.DictReader(arquivo)
    dados = [linha for linha in leitor]

# Salvar a lista de dicionários em JSON
with open(arquivo_json, mode='w', encoding='utf-8') as arquivo_json_out:
    json.dump(dados, arquivo_json_out, ensure_ascii=False, indent=4)

print(f'Dados do CSV salvos no arquivo {arquivo_json} com sucesso!')
