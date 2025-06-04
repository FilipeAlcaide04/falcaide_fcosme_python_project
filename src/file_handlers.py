""" Módulo usado para ordenar e processar os ficheiros raw """

import pandas as pd
import os
import sys
import numpy as np
import src.data_generator as generate
import csv
import json

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

    arquivo_csv = 'data/processed/dados_regionais_processed.csv'
    arquivo_json = 'data/processed/dados_regionais_processed.json'

    # Ler CSV e converter para lista de dicionários
    with open(arquivo_csv, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        dados = [linha for linha in leitor]

    # Salvar a lista de dicionários em JSON
    with open(arquivo_json, mode='w', encoding='utf-8') as arquivo_json_out:
        json.dump(dados, arquivo_json_out, ensure_ascii=False, indent=4)

    print(f'Dados do CSV salvos no arquivo {arquivo_json} com sucesso!')



def sec_main(i):
    if i == '2019':
        arquivo_excel = 'data/raw/elections/ar2019-quadro-resultados.xls'
        sheet_name = 'Quadro'  # Sheet name for 2019
    elif i == '2024':
        arquivo_excel = 'data/raw/elections/2024_ar_quadro_resultados.xlsx'
        sheet_name = 'Mapa Oficial'  # Correct sheet name for 2024

    # Arquivos
    arquivo_csv = 'data/processed/dados_regionais_processed.csv'

    # 1. Carrega o Excel com resultados por distrito
    eleicoes = pd.read_excel(arquivo_excel, sheet_name=sheet_name, header=None)

    # For 2019 and 2024, the structure is similar but row indexes might differ
    if i == '2019':
        distritos = eleicoes.iloc[3, 2:].tolist()
        inscritos = eleicoes.iloc[4, 2:].astype(float).tolist()
        votantes = eleicoes.iloc[5, 2:].astype(float).tolist()
        brancos = eleicoes.iloc[8, 2:].astype(float).tolist()
    elif i == '2024':
        distritos = eleicoes.iloc[2, 2:].tolist()
        inscritos = eleicoes.iloc[3, 2:].astype(float).tolist()
        votantes = eleicoes.iloc[4, 2:].astype(float).tolist()  # This is the "Número" row for Votantes
        brancos = eleicoes.iloc[7, 2:].astype(float).tolist()

    df_distritos = pd.DataFrame({
        'distrito': distritos,
        'Inscritos': inscritos,
        'Votantes': votantes,
        'Brancos': brancos
    })

    # 2. Carrega dados regionais (freguesias)
    df_freguesias = pd.read_csv(arquivo_csv)

    # Normaliza os nomes das colunas e remove espaços extras nos distritos
    # Normaliza os nomes das colunas e remove espaços extras nos distritos
    df_freguesias.columns = df_freguesias.columns.str.strip().str.lower()

    # Substitui os nomes dos distritos das regiões autónomas
    df_freguesias['distrito'] = df_freguesias['distrito'].replace({
        'Ilha da Madeira': 'RA Madeira',
        'Ilha de Porto Santo': 'RA Açores',
        'Ilha de São Miguel': 'RA Açores',
        'Ilha de Santa Maria': 'RA Açores',
        'Ilha de Porto Santo': 'RA Açores',
        'Ilha Terceira': 'RA Açores',
        'Ilha de São Jorge': 'RA Açores',
        'Ilha do Pico': 'RA Açores',
        'Ilha das Flores': 'RA Açores',
        'Ilha do Faial': 'RA Açores',
        'Ilha Graciosa': 'RA Açores',
        'Ilha do Corvo': 'RA Açores'
    }).str.strip()


    # 3. Cria população aleatória plausível para cada freguesia
 
    df_freguesias['populacao'] = generate.gen_pop(df_freguesias)

    #np.random.randint(500, 5001, size=len(df_freguesias))

    # 4. Junta os dados distritais com as freguesias
    df = df_freguesias.merge(df_distritos, on='distrito', how='left')

    # 5. Distribui proporcionalmente os resultados eleitorais para cada freguesia
    df['inscritos_freguesia'] = (df['populacao'] / df.groupby('distrito')['populacao'].transform('sum')) * df['Inscritos']
    df['votantes_freguesia'] = (df['populacao'] / df.groupby('distrito')['populacao'].transform('sum')) * df['Votantes']
    df['brancos_freguesia'] = (df['populacao'] / df.groupby('distrito')['populacao'].transform('sum')) * df['Brancos']

    # 6. Tratar NaNs e infinitos antes da conversão
    df['inscritos_freguesia'] = df['inscritos_freguesia'].fillna(0)
    df['votantes_freguesia'] = df['votantes_freguesia'].fillna(0)
    df['brancos_freguesia'] = df['brancos_freguesia'].fillna(0)

    df.replace([np.inf, -np.inf], 0, inplace=True)

    # 7. Arredonda os resultados e converte para inteiro
    df['inscritos_freguesia'] = df['inscritos_freguesia'].round().astype(int)
    df['votantes_freguesia'] = df['votantes_freguesia'].round().astype(int)
    df['brancos_freguesia'] = df['brancos_freguesia'].round().astype(int)

    # 8. Salva o resultado (fixing the typo in '2019:')
    if i == '2019':
        df.to_csv('data/processed/data_votes_freg_2019.csv', index=False)
    elif i == '2024':
        df.to_csv('data/processed/data_votes_freg_2024.csv', index=False)

    print("✅ Resultados por freguesia gerados com população aleatória plausível!")

    arquivo_csv = 'data/processed/data_votes_freg_' + i + '.csv'
    arquivo_json = 'data/processed/dados_regionais_processed.json'

    # Ler CSV e converter para lista de dicionários
    with open(arquivo_csv, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        dados = [linha for linha in leitor]

        # 9. Gerar votos por partido para cada freguesia
    votos_partido = generate.gen_votes_por_partido(df, ano=i)
    
    # Obter os dados originais do DataFrame para calcular a abstenção
    for idx, row in df.iterrows():
        freguesia_id = row['ine_id']
        # Encontrar a freguesia correspondente no votos_partido
        for freg in votos_partido:
            if freg['ine_id'] == freguesia_id:
                inscritos = row['inscritos_freguesia']
                votantes = row['votantes_freguesia']
                freg['Abstenção'] = int(inscritos - votantes)
                break

    # 10. Salvar votos em arquivo JSON
    with open(f'data/processed/votos_freguesia_{i}.json', 'w', encoding='utf-8') as f_out:
        json.dump(votos_partido, f_out, ensure_ascii=False, indent=4)
