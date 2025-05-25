""" Módulo usado para ordernar e processar os ficheiros raw """
import pandas as pd
import os
import sys

def carregar_csv(caminho):
    if not os.path.exists(caminho):
        print(f"Erro: o ficheiro '{caminho}' não existe.")
        sys.exit(1)
    try:
        return pd.read_csv(caminho)
    except Exception as e:
        print(f"Erro ao carregar o ficheiro '{caminho}': {e}")
        sys.exit(1)

def main():
    # Dar load ao CSVS com verificação de existência
    distritos = carregar_csv('data/raw/distritos.csv')
    municipios = carregar_csv('data/raw/municipios.csv')
    freguesias = carregar_csv('data/raw/freguesias.csv')

    # Garantir que todos os códigos têm os dígitos corretos (2, 4, 6)
    distritos['ine_id'] = distritos['ine_id'].astype(str).str.zfill(2)
    municipios['ine_id'] = municipios['ine_id'].astype(str).str.zfill(4)
    freguesias['ine_id'] = freguesias['ine_id'].astype(str).str.zfill(6)

    # Renomear colunas para evitar conflitos
    distritos = distritos.rename(columns={'name': 'distrito'})
    municipios = municipios.rename(columns={'name': 'municipio'})
    freguesias = freguesias.rename(columns={'name': 'freguesia'})

    # Junta o distrito e o município
    freguesias['distrito_id'] = freguesias['ine_id'].str[:2]
    freguesias['municipio_id'] = freguesias['ine_id'].str[:4]

    # Juntar os dados todos num data frame
    # Primeiro, juntar freguesias com municípios
    df = pd.merge(
        freguesias,
        municipios[['ine_id', 'municipio']],
        left_on='municipio_id',
        right_on='ine_id',
        how='left'
    ).drop(columns=['ine_id_y']).rename(columns={'ine_id_x': 'ine_id'})

    # Depois, juntar com distritos
    df = pd.merge(
        df,
        distritos[['ine_id', 'distrito']],
        left_on='distrito_id',
        right_on='ine_id',
        how='left'
    ).drop(columns=['ine_id_y']).rename(columns={'ine_id_x': 'ine_id'})

    # Ordenar colunas
    df = df[['ine_id', 'distrito', 'municipio', 'freguesia']]

    # Guardar em CSV com os dados já limpos
    df.to_csv('data/processed/dados_regionais_processed.csv', index=False)

##############################################################################################################################

""" Aqui vamos limpar os dados das eleições de 2019 e 2024 """


