from flask import Flask, request, jsonify

app = Flask(__name__)
@app.post("/enviar")
def enviar():

    json_post = request.get_json()

    if json_post is None:
        return jsonify({"erro": "Nenhum JSON enviado no POST."}), 400

    # Combina dados do GET com os do POST
    resposta = {
        "status": "POST recebido!",
        "dados_post_recebidos": json_post
    }

    return jsonify(resposta)
if __name__ == "__main__":
    app.run()