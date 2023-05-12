from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


@app.route('/')
def home():
    return 'Bem-vindo ao meu site!'


@app.route('/consultacep', methods=['POST'])
def consulta_cep():
    dados = request.get_json()

    if 'cep' not in dados:
        return jsonify({'erro': 'CEP não fornecido'}), 400

    cep = dados['cep']

    response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({'erro': 'CEP inválido'}), 400

if __name__ == '__main__':
    app.run()
