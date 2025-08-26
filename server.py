import csv
from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)
CSV_FILE = 'dados_rede.csv'

# Cria CSV com cabeçalho correto
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp','RSSI','latencia_ms','perda_pct'])

@app.route('/')
def index():
    return "Servidor Flask rodando!!"

@app.route('/metrics', methods=['POST'])
def metrics():
    data = request.get_json()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("📡 Dados recebidos:", data, "em", timestamp)

    # Salva no CSV
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, data['RSSI'], data['latencia_ms'], data['perda_pct']])

    return jsonify({"status": "ok", "message": "Métricas recebidas com sucesso!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


# import csv
# from flask import Flask, request, jsonify
# from datetime import datetime

# app = Flask(__name__)
# CSV_FILE = 'dados_rede.csv'

# # Cria CSV com cabeçalho se não existir
# try:
#     with open(CSV_FILE, 'x', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['timestamp','RSSI','latencia_ms','perda_pct'])
# except FileExistsError:
#     pass

# @app.route('/')
# def index():
#     return "Servidor Flask rodando!"

# @app.route('/metrics', methods=['POST'])
# def metrics():
#     data = request.get_json()
#     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     print("📡 Dados recebidos:", data, "em", timestamp)

#     # Salva no CSV
#     with open(CSV_FILE, 'a', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow([timestamp, data['RSSI'], data['latencia_ms'], data['perda_pct']])

#     print("💾 Linha salva no CSV:", data)
#     return jsonify({"status": "ok", "message": "Métricas recebidas com sucesso!"})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)
