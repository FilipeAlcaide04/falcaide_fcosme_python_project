""" Servidor Flask para consultar resultados eleitorais em Portugal"""

import json
import os
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def carregar_dados(ano):
    """Carrega os dados de votos por freguesia de um determinado ano."""
    caminho = f"data/processed/votos_freguesia_{ano}.json"
    if os.path.exists(caminho):
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

dados_2019 = carregar_dados("2019")
dados_2024 = carregar_dados("2024")

def calcular_resultados_nacionais(dados):
    """Calcula os resultados nacionais a partir dos dados de freguesias."""
    total_votos = {}
    total_eleitores = 0
    total_votantes = 0
    total_brancos = 0

    for freguesia in dados:
        total_eleitores += freguesia['inscritos']
        total_votantes += freguesia['votantes']
        total_brancos += freguesia['brancos']

        for partido, votos in freguesia['votos'].items():
            if partido in total_votos:
                total_votos[partido] += votos
            else:
                total_votos[partido] = votos

    # Calcular percentagens
    votos_validos = total_votantes - total_brancos
    resultados = {
        'total': total_votos,
        'percentagens': {partido: (votos/votos_validos)*100 for partido,\
                          votos in total_votos.items()},
        'vencedor': max(total_votos.items(), key=lambda x: x[1])[0],
        'estatisticas': {
            'total_eleitores': total_eleitores,
            'total_votantes': total_votantes,
            'abstencao': total_eleitores - total_votantes,
            'brancos': total_brancos,
            'votos_validos': votos_validos
        }
    }
    return resultados

resultados_nacionais_2019 = calcular_resultados_nacionais(dados_2019)
resultados_nacionais_2024 = calcular_resultados_nacionais(dados_2024)

@app.route('/')
def index():
    """Rota principal que renderiza a página inicial."""
    return render_template("index.html")

@app.route('/api/distritos')
def get_distritos():
    """Retorna a lista de distritos disponíveis nos dados de 2024."""
    distritos = set()
    for freguesia in dados_2024:
        distritos.add(freguesia['distrito'])
    return jsonify(sorted(list(distritos)))

@app.route('/api/freguesias')
def get_freguesias():
    """Retorna a lista de freguesias de um distrito específico."""
    distrito = request.args.get('distrito')
    freguesias = []
    for freguesia in dados_2024:
        if freguesia['distrito'].lower() == distrito.lower():
            freguesias.append(freguesia['freguesia'])
    return jsonify(freguesias)

@app.route('/api/resultados')
def get_resultados():
    """Retorna os resultados eleitorais de uma freguesia específica ou nacionais."""
    distrito = request.args.get('distrito')
    freguesia = request.args.get('freguesia')
    ano = request.args.get('ano', '2024')

    dados = dados_2024 if ano == "2024" else dados_2019
    resultados_nacionais = resultados_nacionais_2024 if ano == "2024" else resultados_nacionais_2019

    if not distrito and not freguesia:
        # Retornar resultados nacionais
        return jsonify({
            "tipo": "nacional",
            "vencedor": resultados_nacionais['vencedor'],
            "resultados": resultados_nacionais['total'],
            "percentagens": resultados_nacionais['percentagens'],
            "estatisticas": resultados_nacionais['estatisticas']
        })

    for f in dados:
        if f['distrito'].lower() == distrito.lower()\
              and f['freguesia'].lower() == freguesia.lower():
            votos_validos = f['votantes'] - f['brancos']
            percentagens = {partido: (votos/votos_validos)*100\
                             for partido, votos in f['votos'].items()}
            vencedor = max(f['votos'].items(), key=lambda x: x[1])[0]

            return jsonify({
                "tipo": "freguesia",
                "info": {
                    "freguesia": f['freguesia'],
                    "distrito": f['distrito'],
                    "municipio": f['municipio'],
                    "inscritos": f['inscritos'],
                    "votantes": f['votantes'],
                    "abstencao": f['Abstenção'],
                    "brancos": f['brancos'],
                    "votos_validos": votos_validos
                },
                "vencedor": vencedor,
                "votos": f['votos'],
                "percentagens": percentagens,
                "resultados_nacionais": {
                    "vencedor": resultados_nacionais['vencedor'],
                    "percentagens": resultados_nacionais['percentagens']
                }
            })
    return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)
