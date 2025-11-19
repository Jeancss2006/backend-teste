from flask import Flask

app = Flask(__name__)

@app.get("/teste")
def teste():
    return {"mensagem": "API funcionando!"}

if __name__ == "__main__":
    app.run()