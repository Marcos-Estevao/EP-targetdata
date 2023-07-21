from flask import Flask, request, jsonify
import requests
import xmltodict
import json
import urllib.parse
from unidecode import unidecode

app = Flask(__name__)


@app.route('/')
def home():
    return 'Bem-vindo ao meu site!'


def convert_xml_to_json(xml_str):
    data_dict = xmltodict.parse(xml_str)
    json_data = json.dumps(data_dict)
    return json.loads(json_data)


@app.route('/consultacep', methods=['POST'])
def consulta_cep():
    dados = request.get_json()

    if 'cep' not in dados:
        return jsonify({'erro': 'CEP não fornecido'}), 400

    cep = dados['cep']

    response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')

    if response.status_code == 200:
        localidade = response.json()['localidade']
        localidade = unidecode(localidade)
        localidade_encode = urllib.parse.quote(localidade)
        response = requests.get(f'http://servicos.cptec.inpe.br/XML/listaCidades?city={localidade_encode}')
        inpe_json_response = convert_xml_to_json(response.text)
        if isinstance(inpe_json_response['cidades']['cidade'], list):
            id_cidade = inpe_json_response['cidades']['cidade'][0]['id']
        else:
            id_cidade = inpe_json_response['cidades']['cidade']['id']

        response = requests.get(f'http://servicos.cptec.inpe.br/XML/cidade/{id_cidade}/previsao.xml')
        inpe_json_response = convert_xml_to_json(response.text)

        return inpe_json_response


    else:
        return jsonify({'erro': 'CEP inválido'}), 400


if __name__ == '__main__':
    app.run()
