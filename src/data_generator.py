import numpy as np
import pandas as pd
import json

# Gera uma população aleatória para cada freguesia
def gen_pop(size, pop_tuga=10580000):
    return np.random.randint(500, 5001, size=len(size))

# Gera votos simulados por partido para cada freguesia
def gen_votes_por_partido(df_freguesias, ano='2019'):
    ano_sufixo = ano[-2:]  # '19' ou '24'
    caminho_partidos = f'data/raw/partidos_{ano_sufixo}.json'

    try:
        with open(caminho_partidos, encoding='utf-8') as f:
            partidos = json.load(f)
    except FileNotFoundError:
        print(f"❌ Arquivo de partidos não encontrado: {caminho_partidos}")
        return []

    resultados = []

    for _, row in df_freguesias.iterrows():
        total_votantes = row['votantes_freguesia']
        total_brancos = row['brancos_freguesia']
        votos_validos = max(0, total_votantes - total_brancos)

        # Gera pesos aleatórios para partidos
        pesos = np.random.dirichlet(np.ones(len(partidos)))
        votos = (pesos * votos_validos).round().astype(int)

        # Corrige diferença para somar exatamente os votos válidos
        diferenca = votos_validos - votos.sum()
        votos[0] += diferenca

        votos_por_partido = dict(zip(partidos, votos))

        resultado = {
            'ine_id': str(row['ine_id']),
            'freguesia': str(row['freguesia']),
            'distrito': str(row['distrito']),
            'municipio': str(row['municipio']),
            'inscritos': int(row['inscritos_freguesia']),
            'votantes': int(row['votantes_freguesia']),
            'brancos': int(row['brancos_freguesia']),
            'votos': {partido: int(v) for partido, v in votos_por_partido.items()}
        }

        resultados.append(resultado)

    return resultados
