from flask import Flask


app = Flask(__name__)


@app.route('/')
def home():
    return 'Bem-vindo ao meu site!'


@app.route('/contato')
def contato():
    return 'Entre em contato conosco!'


@app.route('/consultarEndereco')
def consultar_endereco():
    return 'Consultar endereço'


if __name__ == '__main__':
    app.run()
