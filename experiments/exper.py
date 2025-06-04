import pandas as pd

# Carrega a planilha antiga .xls
df = pd.read_excel("data/raw/elections/ar2019-quadro-resultados.xls", sheet_name=None)

# Verifica os nomes das folhas
print("Folhas disponíveis:", df.keys())

# Exemplo: acessa a folha onde estão os dados principais
# Altere o nome conforme necessário
sheet = df['Quadro']  # ou outro nome real da aba

# Mostra as 20 primeiras linhas para identificar onde estão RA Madeira e RA Açores
print(sheet.head(20))

# Filtra as linhas com RA Madeira e RA Açores
ra_madeira = sheet[sheet.iloc[:, 0].str.contains("RA Madeira", na=False)]
ra_acores = sheet[sheet.iloc[:, 0].str.contains("RA Açores", na=False)]

# Exibe os dados encontrados
print("RA Madeira:\n", ra_madeira)
print("RA Açores:\n", ra_acores)
