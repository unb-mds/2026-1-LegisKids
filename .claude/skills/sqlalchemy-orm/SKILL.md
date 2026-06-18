---
name: sqlalchemy-orm
description: Use this skill whenever writing or editing SQLAlchemy models, queries, sessions, or Alembic migrations in the LegisKids Flask backend. Triggers on db.Model, Column, relationship(), session.query, db.session, Alembic revisions, or any file under backend/src/models. Covers Flask-SQLAlchemy setup, model definitions, relationships, query patterns, session management, and migrations. For raw SQL/schema design reasoning use postgresql-design; for the Flask route layer use flask-backend.
---

# SQLAlchemy ORM — LegisKids

## Setup com Flask-SQLAlchemy

Centralize a instância do `db` em `extensions.py` para evitar import circular entre models e a app factory:

```python
# src/extensions.py
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
```

```python
# src/__init__.py
from .extensions import db

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    return app
```

## Definindo modelos

Use a sintaxe moderna do SQLAlchemy 2.0 (`Mapped`/`mapped_column`) quando a versão instalada suportar — é mais explícita com tipos e evita erros de runtime:

```python
# src/models/proposicao.py
from datetime import datetime
from src.extensions import db
from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Proposicao(db.Model):
    __tablename__ = "proposicoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    ementa: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="tramitando")
    autor_id: Mapped[int | None] = mapped_column(ForeignKey("autores.id"))
    criado_em: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    autor: Mapped["Autor"] = relationship(back_populates="proposicoes")
    temas: Mapped[list["Tema"]] = relationship(
        secondary="proposicoes_temas", back_populates="proposicoes"
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "ementa": self.ementa,
            "status": self.status,
            "autor": self.autor.nome if self.autor else None,
            "temas": [t.nome for t in self.temas],
        }
```

Sempre implemente `to_dict()` (ou um serializer separado) em cada modelo — evita serializar objetos SQLAlchemy direto com `jsonify`, o que falha ou expõe campos internos.

## Relacionamentos N:N

```python
proposicoes_temas = db.Table(
    "proposicoes_temas",
    db.Column("proposicao_id", db.ForeignKey("proposicoes.id"), primary_key=True),
    db.Column("tema_id", db.ForeignKey("temas.id"), primary_key=True),
)
```

## Consultas — evite N+1

Errado (uma query por proposição para buscar o autor):
```python
proposicoes = Proposicao.query.all()
for p in proposicoes:
    print(p.autor.nome)  # dispara uma query por iteração
```

Correto, com eager loading:
```python
from sqlalchemy.orm import joinedload, selectinload

proposicoes = (
    db.session.query(Proposicao)
    .options(joinedload(Proposicao.autor), selectinload(Proposicao.temas))
    .all()
)
```

- `joinedload` para relações 1:1/N:1 (poucos registros relacionados).
- `selectinload` para relações 1:N/N:N (evita explosão de linhas no JOIN).

## Filtros e paginação

```python
def listar_proposicoes(pagina: int = 1, tema: str | None = None, por_pagina: int = 20):
    query = db.session.query(Proposicao).options(selectinload(Proposicao.temas))
    if tema:
        query = query.join(Proposicao.temas).filter(Tema.nome == tema)
    paginado = query.order_by(Proposicao.criado_em.desc()).paginate(
        page=pagina, per_page=por_pagina, error_out=False
    )
    return {
        "data": [p.to_dict() for p in paginado.items],
        "total": paginado.total,
        "pagina": pagina,
        "paginas": paginado.pages,
    }
```

Nunca use `.all()` sem paginação em endpoints que listam proposições — a tabela cresce continuamente.

## Sessões e transações

- Nunca crie uma `Session` manual fora do ciclo de request do Flask-SQLAlchemy; use `db.session`.
- Agrupe múltiplas escritas relacionadas em uma única transação e só faça `db.session.commit()` ao final:

```python
def registrar_mudanca_status(proposicao_id: int, novo_status: str) -> None:
    proposicao = db.session.get(Proposicao, proposicao_id)
    if proposicao is None:
        raise ValueError("Proposição não encontrada")

    historico = HistoricoStatus(
        proposicao_id=proposicao.id,
        status_anterior=proposicao.status,
        status_novo=novo_status,
    )
    proposicao.status = novo_status

    db.session.add(historico)
    db.session.commit()
```

- Em caso de erro, faça `db.session.rollback()` explicitamente (ou deixe um `try/except` no nível do error handler da app cuidar disso) para não deixar a sessão "suja".

## Migrações com Alembic (Flask-Migrate)

```bash
flask db init        # uma única vez
flask db migrate -m "cria tabela proposicoes"
flask db upgrade
```

Regras:
- Toda mudança de modelo gera uma migração — nunca editar o schema do banco fora desse fluxo.
- Revise o arquivo de migração gerado automaticamente antes de aplicar; o autogenerate do Alembic não detecta tudo (ex.: renomear coluna aparece como drop+add).
- Rode `flask db upgrade` como parte do processo de deploy/CI, nunca manualmente em produção sem revisão.

## Checklist

1. Modelo com `to_dict()`/serializer próprio.
2. Relações usando `relationship()` com `back_populates` nos dois lados.
3. Consultas com `joinedload`/`selectinload` quando há relação a percorrer.
4. Toda listagem paginada.
5. Mudança de schema sempre via migração Alembic, com revisão manual do arquivo gerado.
