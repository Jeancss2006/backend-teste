from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import threading
import time
import os

app = Flask(__name__, static_folder="static", static_url_path="")
CORS(app)  # libera CORS (aceita requisições de outros computadores)

# Armazenamento seguro em memória para o último JSON recebido
_last_json_lock = threading.Lock()
_last_json = None
_last_received_at = None

@app.post("/receber")
def receber():
    """
    Rota para outro computador enviar JSON.
    Exemplo: curl -X POST -H "Content-Type: application/json" -d '{"nome":"Jean"}' https://seu-domínio/receber
    """
    global _last_json, _last_received_at
    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "Nenhum JSON enviado ou Content-Type incorreto."}), 400

    with _last_json_lock:
        _last_json = dados
        _last_received_at = time.time()

    return jsonify({"status": "JSON recebido com sucesso!"}), 200
@app.get("/latest")
def latest():
    """
    Rota para o front-end buscar o último JSON recebido.
    Retorna {"dados": <objeto ou null>, "received_at": <timestamp>} 
    """
    with _last_json_lock:
        if _last_json is None:
            return jsonify({"dados": None, "received_at": None})
        return jsonify({"dados": _last_json, "received_at": _last_received_at})

# Serve página estática (index.html) da pasta static para testes
@app.get("/")
def index():
    return send_from_directory("static", "index.html")

if __name__ == "__main__":
    # Em produção, use gunicorn: gunicorn app:app
    app.run(host="0.0.0.0", port=5000, debug=True)