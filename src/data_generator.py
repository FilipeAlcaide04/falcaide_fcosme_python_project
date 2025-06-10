""" Gerador de dados sintéticos para freguesias em Portugal """
import json
import numpy as np

# Gera uma população aleatória para cada freguesia
def gen_pop(size):
    """ Gera uma população aleatória para cada freguesia."""
    return np.random.randint(500, 5001, size=len(size))

def gen_votes_por_partido(df_freguesias, ano='2019', partidos_path=None):
    """ Gera votos por partido para cada freguesia com base em um ano específico."""
    ano_sufixo = ano[-2:]
    caminho_partidos = partidos_path or f'data/raw/partidos_{ano_sufixo}.json'

    try:
        with open(caminho_partidos, encoding='utf-8') as f:
            partidos = json.load(f)
    except FileNotFoundError:
        print(f"❌ Arquivo de partidos não encontrado: {caminho_partidos}")
        return []

    preferencias_por_ano = {
        '2019': {
            "PS": 4, "PSD": 4, "BE": 2.5, "CDU": 2, "CDS-PP": 1.5, "PAN": 1, "IL": 1,
            "CHEGA": 1, "LIVRE": 0.5, "R.I.R.": 0.2, "PCTP/MRPP": 0.01, "MPT": 0.05,
            "PURP": 0.1, "PPM": 0.1, "JPP": 0.2, "PNR": 0.1, "Nós, Cidadãos!": 0.1, "Aliança": 0.2
        },
        '2024': {
            "PS": 4, "AD": 5, "CHEGA": 4, "IL": 2, "BE": 1, "LIVRE": 2, "PAN": 0.5, "CDU": 1,
            "R.I.R.": 0.1, "JPP": 0.4, "ADN": 0.3, "Volt": 0.3, "Ergue-te": 0.05, "MPT": 0.05,
            "PPM": 0.1, "NC": 0.1, "MAS": 0.05, "PTP": 0.05, "PCTP/MRPP": 0.01
        }
    }

    preferencias = preferencias_por_ano.get(ano, {})
    alfas = [preferencias.get(partido, 1) for partido in partidos]
    resultados = []

    for _, row in df_freguesias.iterrows():
        total_votantes = row['votantes_freguesia']
        total_brancos = row['brancos_freguesia']
        votos_validos = max(0, total_votantes - total_brancos)

        pesos = np.random.dirichlet(alfas)
        votos = (pesos * votos_validos).round().astype(int)
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
