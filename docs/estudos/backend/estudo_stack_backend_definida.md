# Estudo da Stack Back-end Definida

## Estrutura do Repositório

Este documento apresenta um estudo inicial da stack back-end escolhida para o projeto: **Python + Flask + PostgreSQL**. O foco está na compreensão da estrutura básica do framework Flask, no funcionamento das requisições HTTP e na organização recomendada para projetos.

### Material complementar

Vídeo introdutório sobre Flask:  
https://www.youtube.com/watch?v=e9EPb5AoMf8

---

## 1. Estrutura e Funcionamento do Flask

### O que é Flask?

O **Flask** é um framework web leve desenvolvido em Python, utilizado principalmente para criação de APIs e aplicações web. Sua principal característica é a simplicidade, oferecendo apenas os componentes essenciais para o desenvolvimento, o que proporciona maior flexibilidade ao programador.

### Exemplo básico

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Olá, mundo!"

app.run(debug=True)
```

### Conceitos-chave

- `app` → representa a aplicação principal.
- `@app.route()` → define uma rota (endpoint) acessível pela aplicação.
- `debug=True` → ativa o modo de desenvolvimento, exibindo erros detalhados e reiniciando automaticamente o servidor.

---

## 2. Requisições e Respostas HTTP

As APIs desenvolvidas com Flask normalmente seguem o padrão REST, utilizando métodos HTTP para comunicação entre cliente e servidor.

### Métodos principais

- **GET** → buscar dados
- **POST** → criar novos registros
- **PUT/PATCH** → atualizar informações existentes
- **DELETE** → remover registros

### Exemplo de requisição POST

```python
from flask import request

@app.route('/usuario', methods=['POST'])
def criar_usuario():
    dados = request.json
    return {"mensagem": "Usuário criado", "dados": dados}
```

### Conceitos-chave

- `request` → objeto responsável por acessar os dados enviados pelo cliente.
- `request.json` → permite obter dados no formato JSON.
- `return` → define a resposta enviada pela API.

---

## 3. Organização de Projetos Flask

Uma boa organização do projeto é essencial para facilitar manutenção, escalabilidade e colaboração entre desenvolvedores.

### Estrutura sugerida

```text
/projeto
  /app
    routes.py
    models.py
    services.py
  run.py
```

### Boas práticas

- Separar responsabilidades entre arquivos.
- Evitar concentrar toda a lógica em um único módulo.
- Criar estruturas modulares desde o início do projeto.

---

## 4. Exemplo de Estrutura Básica em Flask

A seguir, uma organização comum utilizada em projetos Flask reais.

### Estrutura de pastas

```text
/meu_projeto
  /app
    __init__.py
    routes.py
    models.py
  run.py
```

---

### `run.py` (ponto de entrada)

Arquivo responsável por iniciar a aplicação.

```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

---

### `app/__init__.py` (criação da aplicação)

Arquivo responsável por criar e configurar a aplicação Flask.

```python
from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import main
    app.register_blueprint(main)

    return app
```

---

### `app/routes.py` (rotas da API)

Arquivo onde são definidos os endpoints da aplicação.

```python
from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return jsonify({"mensagem": "API rodando"})

@main.route('/usuarios')
def listar_usuarios():
    return jsonify(["João", "Maria"])
```

---

### `app/models.py` (modelos e dados)

Arquivo utilizado para representar estruturas de dados ou modelos ligados ao banco de dados.

```python
# Exemplo simples (sem banco ainda)

usuarios = [
    {"id": 1, "nome": "João"},
    {"id": 2, "nome": "Maria"}
]
```

---

## Explicação Geral da Estrutura

Cada arquivo possui uma responsabilidade específica dentro do sistema:

- `run.py` → inicia a aplicação.
- `__init__.py` → cria e configura o app.
- `routes.py` → define as rotas e endpoints.
- `models.py` → representa os dados e futuras entidades do banco.

Essa separação permite:

- evitar desorganização;
- facilitar manutenção;
- permitir crescimento do sistema;
- tornar o código mais reutilizável.

---

## Resumo

A estrutura apresentada segue o fluxo:

**Entrada → Configuração → Rotas → Dados**

Esse padrão é amplamente utilizado em projetos Flask profissionais e serve como base sólida para o desenvolvimento da API do projeto.

---

## Objetivo

Compreender os fundamentos do Flask e estabelecer uma estrutura inicial organizada para o desenvolvimento do back-end, permitindo evolução gradual da aplicação com boas práticas desde o início.