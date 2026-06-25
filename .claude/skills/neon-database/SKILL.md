---
name: neon-database
description: Use this skill if/when the LegisKids project's PostgreSQL is hosted on Neon — covers Neon's branch-per-PR workflow, the serverless driver, and connection pooling differences from a standard self-hosted Postgres. Triggers on "Neon", neon.tech connection strings, @neondatabase/serverless, or questions about database branching for preview environments. For general Postgres schema/index design independent of the host, use postgresql-design; for SQLAlchemy code use sqlalchemy-orm.
---

# Neon — Banco de Dados Serverless do LegisKids

## O que torna Neon diferente de um Postgres comum

Neon separa armazenamento e computação e oferece **branching de banco de dados**: é possível criar uma branch do banco (com os dados de produção, instantaneamente, via copy-on-write) por Pull Request, rodar migrações nela isoladamente, e descartá-la quando o PR é mesclado/fechado — sem afetar produção. Para o fluxo de CI do LegisKids (ver skill `github-actions-ci`), isso é mais robusto que testar contra um Postgres genérico vazio, pois pode validar migrações contra um schema/dados realistas.

## Connection string

```bash
# .env (não commitado)
DATABASE_URL=postgresql://usuario:senha@ep-exemplo-123456.sa-east-1.aws.neon.tech/legiskids?sslmode=require
```

- `sslmode=require` é obrigatório no Neon — conexões sem TLS são rejeitadas.
- Use a connection string normal (não a "pooled") para migrações/scripts de longa duração; use a versão com `-pooler` no host para a aplicação web com muitas conexões curtas (ver seção de pooling abaixo).

## Uso com SQLAlchemy/Flask

A integração com SQLAlchemy/Flask-SQLAlchemy (ver skill `sqlalchemy-orm`) não muda — Neon é Postgres "de verdade" por baixo, então basta apontar `SQLALCHEMY_DATABASE_URI` para a connection string do Neon:

```python
# src/config.py
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,  # detecta conexões "mortas" antes de usá-las
    }
```

`pool_pre_ping: True` é especialmente importante com Neon: o compute pode "adormecer" automaticamente após inatividade (autosuspend) e a primeira conexão depois disso pode precisar reconectar — o pre-ping evita erros intermitentes de "conexão perdida" na aplicação.

## Pooling de conexões

O Postgres tem um limite relativamente baixo de conexões diretas simultâneas. Para o backend Flask em produção (potencialmente múltiplos workers do gunicorn), use o **endpoint com pooler** do Neon (PgBouncer gerenciado), identificável pelo `-pooler` no hostname da connection string, em vez do endpoint direto — isso evita esgotar o limite de conexões do banco quando há vários workers/processos abrindo conexões ao mesmo tempo.

## Branch por Pull Request (workflow recomendado)

1. Ao abrir um PR que altera schema (nova migração Alembic), criar uma branch Neon a partir da branch principal do banco.
2. Rodar `flask db upgrade` contra essa branch para validar que a migração aplica sem erro.
3. Rodar a suíte de testes do backend apontando `DATABASE_URL` para essa branch.
4. Ao mesclar/fechar o PR, descartar a branch do banco.

Isso pode ser automatizado no workflow de CI (ver skill `github-actions-ci`) usando a API/CLI do Neon para criar e remover branches de banco como parte do pipeline, em vez de depender só de um Postgres genérico no `services:` do GitHub Actions.

## Autosuspend e ambientes de desenvolvimento/teste

Branches de desenvolvimento no Neon podem ter autosuspend agressivo (compute desliga após minutos de inatividade) — isso é desejável para economizar custo em ambientes de dev/preview, mas pode introduzir uma latência perceptível na primeira query após um período ocioso. Não confunda essa latência com um problema de performance de query real ao fazer profiling.

## Checklist

1. `sslmode=require` presente em toda connection string do Neon.
2. `pool_pre_ping: True` configurado no SQLAlchemy para tolerar autosuspend/reconexões.
3. Endpoint com `-pooler` usado pela aplicação web; endpoint direto reservado para migrações/scripts administrativos.
4. Migrações de schema validadas em uma branch de banco isolada antes de aplicar na branch principal de produção.
5. Segredos de conexão (usuário/senha) nunca commitados, sempre via variável de ambiente.
