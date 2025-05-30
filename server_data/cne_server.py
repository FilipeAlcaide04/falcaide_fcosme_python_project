from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Dados fictícios dos resultados
dados_regionais = "data\processed\dados_regionais_processed.csv"

dados = {
    "portugal": {
        "lisboa": {
            "Alvalade": {"PS": 5000, "PSD": 3000, "BE": 1500},
            "Benfica": {"PS": 4000, "PSD": 3500, "BE": 1200}
        },
        "porto": {
            "Bonfim": {"PS": 4500, "PSD": 2500, "BE": 1300},
            "Paranhos": {"PS": 4200, "PSD": 2800, "BE": 1100}
        }
    }
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/api/freguesias')
def get_freguesias():
    distrito = request.args.get('distrito')
    if distrito in dados["portugal"]:
        return jsonify(list(dados["portugal"][distrito].keys()))
    return jsonify([])

@app.route('/api/resultados')
def get_resultados():
    distrito = request.args.get('distrito')
    freguesia = request.args.get('freguesia')
    try:
        resultados = dados["portugal"][distrito][freguesia]
        return jsonify(resultados)
    except:
        return jsonify({})

if __name__ == '__main__':
    app.run(debug=True)
