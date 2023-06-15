from flask import Flask, request, jsonify
import requests
import xmltodict
import json

app = Flask(__name__)


@app.route('/')
def home():
    return 'Bem-vindo ao meu site!'


def convert_xml_to_json(xml_str):
    data_dict = xmltodict.parse(xml_str)
    json_data = json.dumps(data_dict)
    return json_data


@app.route('/consultacep', methods=['POST'])
def consulta_cep():
    dados = request.get_json()

    if 'cep' not in dados:
        return jsonify({'erro': 'CEP não fornecido'}), 400

    cep = dados['cep']

    response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')

    if response.status_code == 200:
        localidade = response.json()['localidade']
        response = requests.get(f'http://servicos.cptec.inpe.br/XML/listaCidades?city={localidade}')
        inpe_json_response = convert_xml_to_json(response.text)
        return jsonify(inpe_json_response), 200

    else:
        return jsonify({'erro': 'CEP inválido'}), 400


if __name__ == '__main__':
    app.run()
