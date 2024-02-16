# Configuração de Ambiente Docker Swarm

## Arquitetura do Ambiente
O Docker Swarm é uma ferramenta que permite criar e gerenciar clusters de containers. A arquitetura do Docker Swarm inclui vários componentes que colaboram para fornecer recursos de orquestração de containers. Aqui estão os principais componentes da arquitetura do Docker Swarm:

### Manager Nodes (Nós Gerenciadores):
* Os nós gerenciadores são responsáveis por coordenar as atividades do swarm e manter o estado do cluster.
* Eles gerenciam a aceitação de novos nós no cluster, distribuem tarefas (serviços) entre os nós e mantêm a consistência do estado do cluster.
* Pode haver vários nós gerenciadores para garantir alta disponibilidade e escalabilidade.

### Worker Nodes (Nós de Trabalho):
* Os nós de trabalho são responsáveis por executar as tarefas (containers) atribuídas pelo nó gerenciador.
* Eles executam as instâncias dos serviços distribuídos pelo swarm.

### Raft Consensus Algorithm:
* O Docker Swarm utiliza o algoritmo de consenso Raft para garantir a consistência do estado entre os nós gerenciadores.
* O Raft garante que um nó gerenciador (geralmente em um número ímpar para alcançar a maioria) seja eleito como líder e tenha a responsabilidade de tomar decisões sobre o estado do swarm.

### Overlay Network:
* O swarm cria automaticamente uma rede de sobreposição (overlay network) que permite a comunicação entre os containers em diferentes nós do swarm.
* Isso permite que os containers se vejam como se estivessem na mesma rede local, independentemente de onde estejam no cluster.

### Service Abstraction:
* Os serviços no Docker Swarm são a abstração que define a execução de containers no cluster.
* Eles podem ser escalados para vários nós, e o swarm gerencia a distribuição de tarefas (containers) para atender à escala desejada.

## Arquivo do Docker Compose

```
services:
    web:
      image: 127.0.0.1:5000/stackdemo
      deploy:
        replicas: 5
      build: .
      ports:
        - "8000:8000" 

    redis:
      image: redis:alpine

    mysql:
      image: mysql
      deploy:
        replicas: 2
      environment:
        MYSQL_ROOT_PASSWORD: ""
        MYSQL_DATABASE: "localhost"
        MYSQL_PASSWORD: ""
        MYSQL_ALLOW_EMPTY_PASSWORD: "yes"
      volumes:
        - ./mysql:/var/lib/mysql
```  
## Comando Utilizados:
### 1. inciar o docker swarm:
`$ docker swarm init --advertise-addr (IP)`
### 2. Inicie o registro como um serviço no seu enxame:
`$ docker service create --name registry --publish published=5000,target=5000 registry:2`
### 3. Verifique seu status com docker service ls:
`$  docker service ls`
### 4. Crie um diretório para o projeto:
`$ mkdir ProjetoWeb`

`$ cd ProjetoWeb`
### 5. Crie um arquivo chamado app.pyno diretório do projeto:
```
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
```
### 6. Crie um arquivo chamado requirements.txt:
```
flask
redis
mysql-connector-python
```
### 7. Crie um arquivo chamado Dockerfile:
```
# syntax=docker/dockerfile:1
FROM python:3.10-alpine
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```
### 8. Crie um arquivo chamado compose.yml:
```
services:
    web:
      image: 127.0.0.1:5000/stackdemo
      deploy:
        replicas: 5
      build: .
      ports:
        - "8000:8000"

    redis:
      image: redis:alpine

    mysql:
      image: mysql
      deploy:
        replicas: 2
      environment:
        MYSQL_ROOT_PASSWORD: ""
        MYSQL_DATABASE: "localhost"
        MYSQL_PASSWORD: ""
        MYSQL_ALLOW_EMPTY_PASSWORD: "yes"
      volumes:
        - ./mysql:/var/lib/mysql
```
### 9. Todos os arquivos acima já estavam no Git e foram apenas clonados para o diretório dentro do Docker Playground - ProjetoWeb
`git clone https://TOKEN@github.com/20232-ifba-saj-ads-tawii/trabalho-equipe.git`
### 10. Ir para diretório e realizar os teste:
`$ cd trabalho-equipe`

`$ cd swarm`
## Teste o aplicativo com compose
### 1. inciar o docker swarm
![docker swarm init --advertise-addr (IP)]()
### 2. Inicie o registro como um serviço no seu enxame
![docker service create](URL da imagem)
### 3. Verifique seu status com docker service ls
![docker service ls](URL da imagem)
### 4. Crie um diretório para o projeto
![mkdir ProjetoWeb, cd ProjetoWeb](URL da imagem)
