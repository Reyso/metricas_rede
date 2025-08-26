import csv
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
CSV_FILE = 'dados_rede.csv'

# Cria CSV com cabeçalho se não existir
try:
    with open(CSV_FILE, 'x', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'timestamp','SSID','BSSID','canal','IP_local',
            'RSSI','latencia_ms','perda_pct','pacotes_enviados','pacotes_recebidos','taxa_sucesso_pct'
        ])
except FileExistsError:
    pass

@app.route('/')
def index():
    return "Servidor Flask rodando!"

@app.route('/metrics', methods=['POST'])
def metrics():
    data = request.get_json()
    print("📡 Dados recebidos:", data)

    # Adiciona timestamp real se não enviado
    if 'timestamp' not in data or not data['timestamp']:
        data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            data.get('timestamp',''),
            data.get('SSID',''),
            data.get('BSSID',''),
            data.get('canal',''),
            data.get('IP_local',''),
            data.get('RSSI',''),
            data.get('latencia_ms',''),
            data.get('perda_pct',''),
            data.get('pacotes_enviados',''),
            data.get('pacotes_recebidos',''),
            data.get('taxa_sucesso_pct','')
        ])
    return jsonify({"status":"ok","message":"Métricas recebidas com sucesso!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
