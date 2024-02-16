# Configuração de Ambiente Docker Swarm

## Introdução

Nesse relatório vamos abordar o processo de implantação de uma pilha de aplicativos em um enxame usando o Docker Swarm. O Docker Swarm é uma ferramenta de orquestração que permite a criação e gerenciamento de clusters de containers. A implantação de uma pilha completa de aplicativos em um enxame é facilitada pelo comando docker stack deploy, que aceita uma descrição de pilha no formato de um arquivo Compose. Foram destacados os passos para configurar um registro Docker, criar um aplicativo de exemplo baseado em Python e Flask, e testar o aplicativo localmente usando o Docker Compose. Em seguida, a imagem do aplicativo foi enviada para o registro e finalmente, a pilha foi implantada no enxame.

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

### Docker Registry:
* Um serviço de registro Docker é iniciado como um serviço no enxame para distribuir imagens para todos os nós.
* É utilizado o Docker Hub ou um registro próprio, e no tutorial, é criado um registro temporário com o comando docker service create.

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
![docker swarm init --advertise-addr (IP)](https://github.com/MateusMarquesDias/swarm/blob/main/img/1.jpg)
### 2. Inicie o registro como um serviço no seu enxame
![docker service create](https://github.com/MateusMarquesDias/swarm/blob/main/img/2.jpg)
### 3. Verifique seu status com docker service ls
![docker service ls](https://github.com/MateusMarquesDias/swarm/blob/main/img/3.jpg)
### 4. Crie um repositório para o projeto
![mkdir ProjetoWeb, cd ProjetoWeb](https://github.com/MateusMarquesDias/swarm/blob/main/img/4.jpg)
### 5. Clonando o repositório para o diretório
![Clonando o repositório para o diretório](https://github.com/MateusMarquesDias/swarm/blob/main/img/5.jpg)
### 6. Acessando o diretório clonado
![Crie um diretório para o projeto](https://github.com/MateusMarquesDias/swarm/blob/main/img/6.jpg)
### 7. Inicie o aplicativo com docker compose up
![Inicie o aplicativo com docker compose up](https://github.com/MateusMarquesDias/swarm/blob/main/img/7.jpg)
![Inicie o aplicativo com docker compose up](https://github.com/MateusMarquesDias/swarm/blob/main/img/7.1.jpg)
### 8. Usando docker compose up -d
![Usando docker compose up -d](https://github.com/MateusMarquesDias/swarm/blob/main/img/8.jpg)
### 9. Verificando se o aplicativo está sendo executado com docker compose ps
![Verificando se o aplicativo está sendo executado com docker compose ps](https://github.com/MateusMarquesDias/swarm/blob/main/img/9.jpg)
### 10. Desativando o aplicativo
![Desativando o aplicativo](https://github.com/MateusMarquesDias/swarm/blob/main/img/10.jpg)
### 11. Enviar uma imagem gerada para registro
#### 11.1 Distribuindo a imagem do aplicativo Web pelo enxame usando docker compose push
![Distribuindo a imagem do aplicativo Web pelo enxame usando docker compose push](https://github.com/MateusMarquesDias/swarm/blob/main/img/11.jpg)
### 12. Implante a pilha no enxame 
#### 12.1 Criando a pilha com docker stack deploy
![Criando a pilha com docker stack deploy](https://github.com/MateusMarquesDias/swarm/blob/main/img/12.jpg)
#### 12.2 Verificando se está funcionando com docker stack services swarm
![Verificando se está funcionando com docker stack services swarm](https://github.com/MateusMarquesDias/swarm/blob/main/img/13.jpg)
#### 12.3 Derrubando a pilha com docker stack rm
![Derrubando a pilha com docker stack rm](https://github.com/MateusMarquesDias/swarm/blob/main/img/14.jpg)
#### 12.4 Desativando o registro com docker service rm
![Desativando o registro com docker service rm](https://github.com/MateusMarquesDias/swarm/blob/main/img/15.jpg)
#### 15.5 Tirando o Docker Engine do modo Swarm
![Tirando o Docker Engine do modo Swarm](https://github.com/MateusMarquesDias/swarm/blob/main/img/16.jpg)

## Conclusão
O Docker Swarm oferece uma solução robusta para a orquestração de containers em ambientes distribuídos. A capacidade de criar, distribuir e gerenciar aplicativos em um enxame facilita a escalabilidade e a manutenção de infraestruturas distribuídas. A combinação do Docker Compose para definição de pilhas de aplicativos e o Docker Swarm para orquestração fornece uma abordagem poderosa para implementações eficientes e dimensionáveis de aplicações containerizadas.

## Referências
* <https://labs.play-with-docker.com/#>

* <https://docs.docker.com/engine/swarm/stack-deploy/>
