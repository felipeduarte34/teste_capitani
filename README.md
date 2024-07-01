# Projeto de Sistema Distribuído com FastAPI, Kafka e PostgreSQL

## Visão Geral

Este projeto é um sistema distribuído que realiza o consumo, transformação, persistência e produção de dados utilizando Kafka, FastAPI e PostgreSQL. O sistema é composto por duas aplicações distintas:

- **Scheduler**: Responsável por consumir dados do Kafka, realizar a transformação e enviar os dados transformados via um endpoint REST.
- **API**: Responsável por receber os dados transformados via o endpoint, persistir no banco de dados PostgreSQL e produzir os dados no Kafka.

## Arquitetura

A arquitetura do sistema é composta pelos seguintes componentes:

- **Kafka**: Utilizado para comunicação assíncrona entre os serviços.
- **Zookeeper**: Necessário para o funcionamento do Kafka.
- **PostgreSQL**: Banco de dados relacional para persistência dos dados.
- **Scheduler**: Serviço responsável por consumir mensagens do Kafka, transformar os dados e enviar para a API.
- **API**: Serviço responsável por receber dados via REST, persistir no PostgreSQL e produzir mensagens no Kafka.

### Estrutura de Pastas

```plaintext
.
├── api
│   ├── alembic
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── src
│       ├── __init__.py
│       ├── api
│       │   ├── __init__.py
│       │   └── controllers
│       │       └── product_controller.py
│       ├── core
│       │   ├── __init__.py
│       │   ├── config.py
│       │   └── database.py
│       ├── domain
│       │   ├── __init__.py
│       │   └── models
│       │       └── product.py
│       └── services
│           ├── __init__.py
│           ├── product_service.py
│           └── kafka_producer_service.py
├── scheduler
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── src
│       ├── __init__.py
│       ├── core
│       │   ├── __init__.py
│       │   └── config.py
│       ├── domain
│       │   ├── __init__.py
│       │   └── models
│       │       └── product.py
│       └── services
│           ├── __init__.py
│           ├── kafka_service.py
│           └── product_service.py
├── docker-compose.yml
└── README.md
```
## Como rodar o projeto

### Pré-requisitos

- Docker
- Docker Compose

### Passo a Passo

1. Clone o repositório:

```bash
git clone https://github.com/felipeduarte34/teste_capitani.git
cd seu-repositorio
```

2. Ajuste as variaveis de ambiente no arquivo `config.py` ( Já estão configuradas para rodar tudo dentro do container):

```python
API
DATABASE_URL = "postgresql+asyncpg://user:password@postgres/productsdb"
TRANSFORMED_TOPIC = "produtos-persistidos"
KAFKA_BROKER_URL = "kafka:9092"

Scheduler
KAFKA_BROKER_URL = "kafka:9092"
TOPIC_NAME = "cadastro-produtos"
TRANSFORMED_TOPIC = "produtos-persistidos"
API_URL = "http://api:8000/products/"
```

3. Execute o comando abaixo para subir os containers:

```bash
docker-compose up --build
```

4. Acesse a documentação da API em `http://localhost:8000/docs` e teste os endpoints.

### Como Testar

1. Produzir uma Mensagem no Kafka

Use o script em python na raiz do projeto produce_message.py
```bash
python produce_message.py
```

2. Verificar se a mensagem foi consumida pelo Scheduler
```bash
 kcat -b localhost:29092 -t cadastro-produtos -C -o beginning 
```
3. Verificar se a mensagem foi persistida no banco de dados

4. Verificar se a mensagem foi produzida no Kafka
```bash
 kcat -b localhost:29092 -t produtos-persistidos -C -o beginning
```