""" Módulo usado para ordenar e processar os ficheiros raw """
"""
import pandas as pd
import os
import sys
import numpy as np

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


def sec_main(i):
    if i == '2019':
        arquivo_excel = 'data/raw/elections/ar2019-quadro-resultados.xls'
        sheet_name = 'Quadro'
    elif i == '2024':
        arquivo_excel = 'data/raw/elections/2024_ar_quadro_resultados.xlsx'
        sheet_name = 'Mapa Oficial'
    else:
        print("Ano inválido! Use '2019' ou '2024'.")
        return

    arquivo_csv = 'data/processed/dados_regionais_processed.csv'
    
    # 1. Carrega planilha Excel com resultados por distrito
    eleicoes = pd.read_excel(arquivo_excel, sheet_name=sheet_name, header=None)

    if i == '2019':
        distritos = eleicoes.iloc[3, 2:].tolist()
        inscritos = eleicoes.iloc[4, 2:].astype(float).tolist()
        votantes = eleicoes.iloc[5, 2:].astype(float).tolist()
        brancos = eleicoes.iloc[8, 2:].astype(float).tolist()
        partidos = eleicoes.iloc[10:10+66, 1].tolist()
        votos_partidos = eleicoes.iloc[10:10+66, 2:]
    elif i == '2024':
        distritos = eleicoes.iloc[2, 2:].tolist()
        inscritos = eleicoes.iloc[3, 2:].astype(float).tolist()
        votantes = eleicoes.iloc[4, 2:].astype(float).tolist()
        brancos = eleicoes.iloc[7, 2:].astype(float).tolist()
        partidos = eleicoes.iloc[9:9+66, 1].tolist()
        votos_partidos = eleicoes.iloc[9:9+66, 2:]

    # Cria DataFrame com dados distritais
    df_distritos = pd.DataFrame({
        'distrito': distritos,
        'Inscritos': inscritos,
        'Votantes': votantes,
        'Brancos': brancos
    })

    votos_partidos.columns = distritos
    votos_partidos.index = partidos

    # Adiciona os votos dos partidos ao DataFrame de distritos
    for partido in votos_partidos.index:
        votos = votos_partidos.loc[partido]  # Series
        
        if isinstance(votos, pd.Series) and len(votos) == len(df_distritos):
            df_distritos[partido] = votos.values
        else:
            print(f"⚠️ Partido '{partido}' ignorado — valores incompatíveis: {type(votos)}, shape: {votos.shape}")

    # 2. Carrega dados regionais
    df_freguesias = pd.read_csv(arquivo_csv)
    df_freguesias.columns = df_freguesias.columns.str.strip().str.lower()
    df_freguesias['distrito'] = df_freguesias['distrito'].str.strip()

    # 3. Gera população plausível para cada freguesia
    np.random.seed(42)
    df_freguesias['populacao'] = np.random.randint(500, 5001, size=len(df_freguesias))

    # Trata valores infinitos ou NaN na população
    df_freguesias['populacao'] = df_freguesias['populacao'].replace([np.inf, -np.inf], np.nan)
    df_freguesias['populacao'] = df_freguesias['populacao'].fillna(0).round().astype(int)

    # 4. Junta distritos com freguesias
    df = df_freguesias.merge(df_distritos, on='distrito', how='left')

    # 5. Distribui resultados proporcionalmente
    distr_pop_total = df.groupby('distrito')['populacao'].transform('sum')
    df['inscritos_freguesia'] = (df['populacao'] / distr_pop_total) * df['Inscritos']
    df['votantes_freguesia'] = (df['populacao'] / distr_pop_total) * df['Votantes']
    df['brancos_freguesia'] = (df['populacao'] / distr_pop_total) * df['Brancos']

    # Distribui votos por partido
    for partido in partidos:
        if partido in df.columns:
            df[f'votos_{partido}'] = (df['populacao'] / distr_pop_total) * df[partido]

    # 6. Tratar NaNs e infinitos
    cols_to_clean = ['inscritos_freguesia', 'votantes_freguesia', 'brancos_freguesia'] + [f'votos_{p}' for p in partidos if p in df.columns]
    for col in cols_to_clean:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan).fillna(0).round().astype(int)

    # 7. Guarda resultado
    output_file = f"data/processed/resultados_por_freguesia_{i}.csv"
    df.to_csv(output_file, index=False)

    print(f"✅ Resultados por freguesia ({i}) gerados com sucesso!")

"""


