import pandas as pd

# Carrega o CSV
test = pd.read_csv('data/processed/resultados_por_freguesia.csv')

# Seleciona a coluna 'populacao' e calcula a soma
soma_populacao = test['populacao'].sum()

# Mostra o resultado
print("Soma da população:", soma_populacao)