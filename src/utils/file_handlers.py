""" Módulo usado para ordernar e processar os ficheiros raw """
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

##############################################################################################################################

""" Aqui vamos limpar os dados das eleições de 2019 e 2024 """


def sec_main(i):

    if i == '2019':
        arquivo_excel = 'data/raw/elections/ar2019-quadro-resultados.xls'
    elif i == '2024':
        arquivo_excel = 'data/raw/elections/2024_ar_quadro_resultados.xlsx'

    # Arquivos
    arquivo_csv = 'data/processed/dados_regionais_processed.csv'

    # 1. Carrega planilha Excel com resultados por distrito
    eleicoes = pd.read_excel(arquivo_excel, sheet_name='Quadro', header=None)

    distritos = eleicoes.iloc[3, 2:].tolist()
    inscritos = eleicoes.iloc[4, 2:].astype(float).tolist()
    votantes = eleicoes.iloc[5, 2:].astype(float).tolist()
    brancos = eleicoes.iloc[8, 2:].astype(float).tolist()

    df_distritos = pd.DataFrame({
        'distrito': distritos,
        'Inscritos': inscritos,
        'Votantes': votantes,
        'Brancos': brancos
    })

    # 2. Carrega dados regionais (freguesias)
    df_freguesias = pd.read_csv(arquivo_csv)

    # Normaliza os nomes das colunas e remove espaços extras nos distritos
    df_freguesias.columns = df_freguesias.columns.str.strip().str.lower()
    df_freguesias['distrito'] = df_freguesias['distrito'].str.strip()

    # 3. Cria população aleatória plausível para cada freguesia
    np.random.seed(42)  # Para reprodutibilidade
    df_freguesias['populacao'] = np.random.randint(500, 5001, size=len(df_freguesias))

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

    # 8. Salva o resultado
    df.to_csv('data/processed/resultados_por_freguesia.csv', index=False)

    print("✅ Resultados por freguesia gerados com população aleatória plausível!")