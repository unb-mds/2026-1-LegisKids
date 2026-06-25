---
name: postgresql-design
description: Use this skill when designing PostgreSQL schemas, writing raw SQL, indexes, constraints, or migrations for the LegisKids project, or when reasoning about query performance and data modeling for legislative data (proposições, autores, votações, temas). Covers normalization, indexing strategy, constraints, and migration discipline at the database level, independent of the ORM. For SQLAlchemy-specific model/query code use sqlalchemy-orm. For Neon-specific branching workflow use neon-database.
---

# PostgreSQL — Modelagem de Dados do LegisKids

## Domínio de dados

O sistema lida com proposições legislativas: leis, projetos de lei, autores (deputados/senadores), temas, status de tramitação, e histórico de mudanças. Modele pensando em consultas de busca/filtro (por tema, autor, status, período) e em acompanhamento de mudanças ao longo do tempo.

## Modelagem relacional

Esboço de schema típico:

```sql
CREATE TABLE autores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    partido VARCHAR(50),
    estado CHAR(2),
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE temas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE proposicoes (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    ementa TEXT NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'tramitando',
    autor_id INTEGER REFERENCES autores(id) ON DELETE SET NULL,
    fonte_externa_id VARCHAR(100) UNIQUE,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT now(),
    atualizado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE proposicoes_temas (
    proposicao_id INTEGER REFERENCES proposicoes(id) ON DELETE CASCADE,
    tema_id INTEGER REFERENCES temas(id) ON DELETE CASCADE,
    PRIMARY KEY (proposicao_id, tema_id)
);

CREATE TABLE historico_status (
    id SERIAL PRIMARY KEY,
    proposicao_id INTEGER NOT NULL REFERENCES proposicoes(id) ON DELETE CASCADE,
    status_anterior VARCHAR(50),
    status_novo VARCHAR(50) NOT NULL,
    registrado_em TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

Princípios aplicados:
- **Normalização até 3FN** para entidades estáveis (autores, temas) — evita duplicação de "Maria Silva" escrito de formas diferentes.
- **Tabela de associação** (`proposicoes_temas`) para relação N:N entre proposições e temas, em vez de uma coluna `tema` repetida ou um array.
- **Histórico append-only** (`historico_status`) em vez de sobrescrever o status — essencial para a funcionalidade de "acompanhar mudanças" do produto.
- `fonte_externa_id` único para idempotência ao importar dados de uma API externa (evita duplicar a mesma proposição em re-imports).

## Índices

Crie índices pensando nos filtros mais comuns da aplicação (busca por tema, autor, status, texto):

```sql
CREATE INDEX idx_proposicoes_status ON proposicoes(status);
CREATE INDEX idx_proposicoes_autor_id ON proposicoes(autor_id);
CREATE INDEX idx_historico_proposicao_id ON historico_status(proposicao_id);

-- Busca textual em título/ementa
CREATE INDEX idx_proposicoes_titulo_trgm ON proposicoes USING gin (titulo gin_trgm_ops);
```

Para busca textual em português (ementa, título), considere `pg_trgm` (busca por similaridade/fuzzy) ou `tsvector`/`to_tsquery` com configuração `portuguese` se o volume de busca textual crescer.

```sql
ALTER TABLE proposicoes ADD COLUMN busca tsvector
    GENERATED ALWAYS AS (to_tsvector('portuguese', titulo || ' ' || ementa)) STORED;
CREATE INDEX idx_proposicoes_busca ON proposicoes USING gin(busca);
```

Não crie índice em toda coluna "porque pode ajudar" — cada índice tem custo de escrita. Indexe o que é de fato filtrado/ordenado com frequência.

## Constraints como documentação executável

Prefira impor regras no banco em vez de confiar só na aplicação:
- `NOT NULL` em campos obrigatórios.
- `UNIQUE` em identificadores naturais (`fonte_externa_id`).
- `CHECK` para enums informais: `CHECK (status IN ('tramitando', 'aprovada', 'rejeitada', 'arquivada'))`.
- `ON DELETE CASCADE`/`SET NULL` pensados deliberadamente, não copiados por padrão.

## Migrações

Nunca altere o schema de produção manualmente via `psql`. Toda alteração de schema deve passar por uma migração versionada (ver skill `sqlalchemy-orm` para Alembic, que é o caminho recomendado quando o projeto já usa SQLAlchemy). Cada migração deve ser:
- Idempotente quando possível.
- Reversível (`upgrade`/`downgrade`).
- Pequena e focada em uma mudança lógica.

## Performance

- Use `EXPLAIN ANALYZE` antes de assumir que uma query está lenta por falta de índice.
- Pagine sempre (`LIMIT`/`OFFSET` ou, melhor, keyset pagination por `id`/`criado_em`) — nunca devolva a tabela `proposicoes` inteira para o frontend.
- Evite N+1: ao listar proposições com autor e temas, use `JOIN`s explícitos ou `JOIN`-based eager loading na ORM, não uma query por linha.

## Backups e ambiente local

- Ambiente local: PostgreSQL via Docker (ver skill `docker-containers`) com volume persistente para não perder dados entre restarts.
- Sempre ter um `.env.example` documentando `DATABASE_URL` sem credenciais reais.

## Checklist de modelagem

1. Toda entidade central tem chave primária e timestamps (`criado_em`, `atualizado_em`).
2. Relações N:N usam tabela de associação, não colunas duplicadas.
3. Índices nos campos usados em `WHERE`/`ORDER BY` frequentes.
4. Mudanças de schema via migração, nunca SQL manual direto em produção.
5. Paginação obrigatória em qualquer listagem que pode crescer.
