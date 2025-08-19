from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

eventos = []

@app.route('/api/evento', methods=['POST'])
def crear_evento():
    data = request.json
    eventos.append(data)
    return jsonify({'status': 'ok', 'evento': data})

@app.route('/api/eventos', methods=['GET'])
def listar_eventos():
    return jsonify(eventos)

if __name__ == '__main__':
    app.run(debug=True)
