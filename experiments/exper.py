""" Python Script used to test some functions and other things :) """
"""
import pandas as pd

df = pd.read_csv('data/processed/portugal_administrative_divisions.csv')

# aveiro = df[df.distrito == 'Aveiro'] Aqui filtra todas as colunas com o Distrito aveiro

# loures = df[df.municipio == 'Loures'] 

print(loures)
"""

import pandas as pd

# Carrega os dados eleitorais
eleicoes = pd.read_excel('data/raw/elections/ar2019-quadro-resultados.xls', sheet_name='Quadro')

# Carrega os dados regionais das freguesias
dados_regionais = pd.read_csv('data/processed/dados_regionais_processed.csv')

print(eleicoes)

