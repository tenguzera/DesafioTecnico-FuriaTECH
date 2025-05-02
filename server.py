from flask import Flask, request, jsonify
from os import makedirs
app = Flask(__name__)

@app.route("/salvar", methods=["POST"])
def salvar_dados():
    data = request.get_json()

    # Simplesmente salvar os dados em um arquivo local
    makedirs("dados", exist_ok=True)
    nome_arquivo = f"dados/{data['cpf']}.json"

    with open(nome_arquivo, "w", encoding="utf-8") as f:
        import json
        json.dump(data, f, indent=4, ensure_ascii=False)

    return jsonify({"status": "ok", "mensagem": "Dados recebidos com sucesso!"})

if __name__ == "__main__":
    app.run(debug=True)