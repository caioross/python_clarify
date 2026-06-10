from flask import Flask, request, jsonify
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Declara o objeto da aplicação
app = Flask(__name__)

@app.route("/consultar_ibge/<nome>",methods=["GET"])
def consultarIbge(nome):
    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/ranking?nome={nome}"
    resposta = requests.get(url)
    dados = resposta.json()
    tabela = pd.DataFrame(dados[0]["res"])
    fig, ax = plt.subplots()
    ax.bar(tabela["nome"], tabela["frequencia"])
    ax.set_xlabel("Nome")
    ax.set_ylabel("Frequencia")
    plt.show()

# Inici o servidor flask no endereço localhost
if __name__ == "__main__":
    app.run(debug=True)

# acesse por http://127.0.0.1:5000/consultar_ibge/caio