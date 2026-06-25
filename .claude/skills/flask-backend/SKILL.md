---
name: flask-backend
description: Use this skill whenever working on the LegisKids Flask backend — creating or editing routes/blueprints, request validation, error handling, app factory/config, or anything under backend/src that defines the API. Triggers on "rota", "endpoint", "blueprint", "Flask", "API", "backend", or any .py file that imports flask. Covers project structure, app factory pattern, blueprints, JSON responses, error handling, and integration with SQLAlchemy/PostgreSQL. Do NOT use for pure SQLAlchemy model/query work (use sqlalchemy-orm) or for the AI/Gemini layer (use gemini-ai-integration).
---

# Flask Backend — LegisKids

## Contexto do projeto

O LegisKids usa Flask como framework de backend, expondo uma API REST consumida pelo frontend (HTML/CSS/JS vanilla e/ou Vue.js) e armazenando dados em PostgreSQL via SQLAlchemy. O objetivo do sistema é monitorar, analisar e facilitar o acesso a proposições legislativas brasileiras.

## Estrutura recomendada

Sempre que criar ou reorganizar o backend, siga o padrão de **Application Factory + Blueprints**, que escala melhor que um único `app.py` monolítico:

```
backend/
├── src/
│   ├── __init__.py          # create_app() — application factory
│   ├── config.py            # classes Config / DevConfig / ProdConfig
│   ├── extensions.py        # db = SQLAlchemy(), instâncias compartilhadas
│   ├── models/               # modelos SQLAlchemy (ver skill sqlalchemy-orm)
│   ├── routes/                # um blueprint por recurso
│   │   ├── proposicoes.py
│   │   ├── usuarios.py
│   │   └── auth.py
│   ├── services/              # lógica de negócio (chamadas à API da Câmara, Gemini, etc.)
│   └── utils/                  # helpers, validadores, serializadores
├── tests/
├── requirements.txt
└── wsgi.py / app.py            # ponto de entrada
```

Nunca coloque lógica de negócio direto na função de rota além de orquestração simples: rota chama `service`, `service` chama `model`/`repository`.

## Application Factory

```python
# src/__init__.py
from flask import Flask
from .config import Config
from .extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    from .routes.proposicoes import proposicoes_bp
    from .routes.auth import auth_bp
    app.register_blueprint(proposicoes_bp, url_prefix="/api/proposicoes")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Recurso não encontrado"}, 404

    return app
```

Isso facilita testes (criar uma app por teste com config diferente) e evita import circular entre `db` e os modelos.

## Blueprints — padrão de rota

```python
# src/routes/proposicoes.py
from flask import Blueprint, jsonify, request
from src.services.proposicoes_service import listar_proposicoes, buscar_por_id

proposicoes_bp = Blueprint("proposicoes", __name__)

@proposicoes_bp.get("/")
def listar():
    pagina = request.args.get("pagina", default=1, type=int)
    tema = request.args.get("tema", type=str)
    resultado = listar_proposicoes(pagina=pagina, tema=tema)
    return jsonify(resultado), 200

@proposicoes_bp.get("/<int:proposicao_id>")
def detalhar(proposicao_id):
    proposicao = buscar_por_id(proposicao_id)
    if proposicao is None:
        return jsonify({"error": "Proposição não encontrada"}), 404
    return jsonify(proposicao), 200
```

Pontos importantes:
- Use os decoradores curtos `@bp.get`, `@bp.post` (Flask 2+) em vez de `methods=["GET"]`.
- Sempre valide e tipe os `request.args`/`request.json` antes de passar para a camada de serviço.
- Devolva sempre JSON consistente: `{"data": ...}` ou `{"error": ..., "details": ...}`, nunca strings cruas de erro.

## Validação de entrada

Para payloads de POST/PUT, prefira `marshmallow` ou `pydantic` em vez de validar campo a campo manualmente:

```python
from pydantic import BaseModel, ValidationError

class NovaProposicaoSchema(BaseModel):
    titulo: str
    ementa: str
    tema: str | None = None

@proposicoes_bp.post("/")
def criar():
    try:
        dados = NovaProposicaoSchema(**request.get_json(force=True))
    except ValidationError as e:
        return jsonify({"error": "Payload inválido", "details": e.errors()}), 400
    ...
```

## Tratamento de erros centralizado

Registre handlers globais na app factory em vez de `try/except` repetido em cada rota:

```python
from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    return jsonify({"error": e.description}), e.code

@app.errorhandler(Exception)
def handle_unexpected(e):
    app.logger.exception(e)
    return jsonify({"error": "Erro interno do servidor"}), 500
```

## CORS

Como o frontend (vanilla JS ou Vue) provavelmente roda em outra origem/porta durante o desenvolvimento, configure `flask-cors` explicitamente, restringindo origens em produção:

```python
from flask_cors import CORS
CORS(app, origins=app.config["ALLOWED_ORIGINS"])
```

## Configuração via ambiente

Nunca hardcode segredos. Use `python-dotenv` + classes de config:

```python
# src/config.py
import os

class Config:
    SECRET_KEY = os.environ["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
```

## Checklist antes de finalizar uma rota nova

1. Blueprint registrado com prefixo claro (`/api/...`).
2. Entrada validada (query params com `type=`, body com schema).
3. Resposta sempre em JSON com status HTTP correto (200/201/400/404/500).
4. Sem lógica de banco direto na função de rota — delega para `services`.
5. Erros tratados, nunca um stack trace exposto ao cliente.
6. Testado com `pytest` + `app.test_client()`.

## Testes

```python
def test_listar_proposicoes(client):
    resposta = client.get("/api/proposicoes/")
    assert resposta.status_code == 200
    assert "data" in resposta.get_json()
```

Use uma fixture `client` baseada em `create_app(TestConfig)` com banco SQLite em memória ou um schema de teste no Postgres.
