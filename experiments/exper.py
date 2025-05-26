import pandas as pd
import numpy as np

# Arquivos
arquivo_excel = 'data/raw/elections/ar2019-quadro-resultados.xls'
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


