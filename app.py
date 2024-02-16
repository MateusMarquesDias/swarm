import socket
import redis
import logging
from flask import Flask
import mysql.connector

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_ip():
    try:
        nome_host = socket.gethostname()
        endereco_ip = socket.gethostbyname(nome_host)
        mysql.connector.connect(
          host="localhost",
          user="root",
          password=""
        )
    except socket.gaierror:
        logging.error("Falha ao recuperar o endereço IP: Nome do host não pôde ser resolvido")
        endereco_ip = 'Não foi possível recuperar o endereço IP'
    except mysql.connector.Error as err:
        logging.error(f"Erro ao conectar com o banco de dados: {err.msg}")
    except socket.error as e:
        logging.error(f"Ocorreu um erro de soquete: {e}")
        endereco_ip = 'Não foi possível recuperar o endereço IP'
    return endereco_ip

@app.route('/')
def hello():
    return get_ip()

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    app.run(host='0.0.0.0', port=8000)
