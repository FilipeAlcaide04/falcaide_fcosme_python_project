"""Módulo usado para ordenar e processar os ficheiros raw."""

import os
import json
import csv
from pathlib import Path
import pandas as pd
import numpy as np
import src.data_generator as generate


def carregar_csv(caminho):
    """Carrega um ficheiro CSV, com verificação de existência."""
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"O ficheiro '{caminho}' não existe.")
    try:
        return pd.read_csv(caminho)
    except Exception as e:
        raise RuntimeError(f"Erro ao carregar o ficheiro '{caminho}': {e}") from e


def main():
    """Processa os dados regionais e guarda em CSV e JSON."""
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    distritos = carregar_csv('data/raw/distritos.csv')
    municipios = carregar_csv('data/raw/municipios.csv')
    freguesias = carregar_csv('data/raw/freguesias.csv')

    distritos['ine_id'] = distritos['ine_id'].astype(str).str.zfill(2)
    municipios['ine_id'] = municipios['ine_id'].astype(str).str.zfill(4)
    freguesias['ine_id'] = freguesias['ine_id'].astype(str).str.zfill(6)

    distritos = distritos.rename(columns={'name': 'distrito'})
    municipios = municipios.rename(columns={'name': 'municipio'})
    freguesias = freguesias.rename(columns={'name': 'freguesia'})

    freguesias['distrito_id'] = freguesias['ine_id'].str[:2]
    freguesias['municipio_id'] = freguesias['ine_id'].str[:4]

    df = pd.merge(
        freguesias,
        municipios[['ine_id', 'municipio']],
        left_on='municipio_id',
        right_on='ine_id',
        how='left'
    ).drop(columns=['ine_id_y']).rename(columns={'ine_id_x': 'ine_id'})

    df = pd.merge(
        df,
        distritos[['ine_id', 'distrito']],
        left_on='distrito_id',
        right_on='ine_id',
        how='left'
    ).drop(columns=['ine_id_y']).rename(columns={'ine_id_x': 'ine_id'})

    df = df[['ine_id', 'distrito', 'municipio', 'freguesia']]
    df.to_csv('data/processed/dados_regionais_processed.csv', index=False)

    with open('data/processed/dados_regionais_processed.csv', mode='r', encoding='utf-8') as f:
        dados = list(csv.DictReader(f))

    with open('data/processed/dados_regionais_processed.json', mode='w', encoding='utf-8') as f_out:
        json.dump(dados, f_out, ensure_ascii=False, indent=4)

    print("✅ Dados regionais processados com sucesso!")


def sec_main(ano):
    """Gera votos por freguesia a partir de ficheiros de eleição."""
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    if ano == '2019':
        arquivo_excel = 'data/raw/elections/ar2019-quadro-resultados.xls'
        sheet_name = 'Quadro'
    elif ano == '2024':
        arquivo_excel = 'data/raw/elections/2024_ar_quadro_resultados.xlsx'
        sheet_name = 'Mapa Oficial'
    else:
        raise ValueError("Ano não suportado. Use '2019' ou '2024'.")

    arquivo_csv = 'data/processed/dados_regionais_processed.csv'
    eleicoes = pd.read_excel(arquivo_excel, sheet_name=sheet_name, header=None)

    if ano == '2019':
        distritos = eleicoes.iloc[3, 2:].tolist()
        inscritos = eleicoes.iloc[4, 2:].astype(float).tolist()
        votantes = eleicoes.iloc[5, 2:].astype(float).tolist()
        brancos = eleicoes.iloc[8, 2:].astype(float).tolist()
    elif ano == '2024':
        distritos = eleicoes.iloc[2, 2:].tolist()
        inscritos = eleicoes.iloc[3, 2:].astype(float).tolist()
        votantes = eleicoes.iloc[4, 2:].astype(float).tolist()
        brancos = eleicoes.iloc[7, 2:].astype(float).tolist()
    else:
        distritos = []
        inscritos = []
        votantes = []
        brancos = []

    df_distritos = pd.DataFrame({
        'distrito': distritos,
        'Inscritos': inscritos,
        'Votantes': votantes,
        'Brancos': brancos
    })
    df_freguesias = pd.read_csv(arquivo_csv)
    df_freguesias.columns = df_freguesias.columns.str.strip().str.lower()

    df_freguesias['distrito'] = df_freguesias['distrito'].replace({
        'Ilha da Madeira': 'RA Madeira',
        'Ilha de Porto Santo': 'RA Açores',
        'Ilha de São Miguel': 'RA Açores',
        'Ilha de Santa Maria': 'RA Açores',
        'Ilha Terceira': 'RA Açores',
        'Ilha de São Jorge': 'RA Açores',
        'Ilha do Pico': 'RA Açores',
        'Ilha das Flores': 'RA Açores',
        'Ilha do Faial': 'RA Açores',
        'Ilha Graciosa': 'RA Açores',
        'Ilha do Corvo': 'RA Açores'
    }).str.strip()

    df_freguesias['populacao'] = generate.gen_pop(df_freguesias)

    df = df_freguesias.merge(df_distritos, on='distrito', how='left')

    total_pop = df.groupby('distrito')['populacao'].transform('sum')
    df['inscritos_freguesia'] = (df['populacao'] / total_pop) * df['Inscritos']
    df['votantes_freguesia'] = (df['populacao'] / total_pop) * df['Votantes']
    df['brancos_freguesia'] = (df['populacao'] / total_pop) * df['Brancos']

    df.replace([np.inf, -np.inf], 0, inplace=True)
    df.fillna(0, inplace=True)

    for col in ['inscritos_freguesia', 'votantes_freguesia', 'brancos_freguesia']:
        df[col] = df[col].round().astype(int)

    df.to_csv(f'data/processed/data_votes_freg_{ano}.csv', index=False)
    print("✅ Resultados por freguesia gerados com população aleatória plausível!")

    votos_partido = generate.gen_votes_por_partido(df, ano=ano)

    for _, row in df.iterrows():
        for freg in votos_partido:
            if freg['ine_id'] == row['ine_id']:
                freg['Abstenção'] = int(row['inscritos_freguesia'] - row['votantes_freguesia'])
                break

    with open(f'data/processed/votos_freguesia_{ano}.json', 'w', encoding='utf-8') as f_out:
        json.dump(votos_partido, f_out, ensure_ascii=False, indent=4)
