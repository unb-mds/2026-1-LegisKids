## Why

A configuração de banco de dados do projeto usa variáveis separadas (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`), gerando inconsistência entre os ambientes dos membros do time. Padronizar em `DATABASE_URL` simplifica a configuração local, habilita conexão segura com o banco remoto Neon e prepara o projeto para CI/CD.

## What Changes

- Atualizar `.env.example` com exemplos seguros de `DATABASE_URL` para Docker local e Neon
- Atualizar `app.py` para usar `DATABASE_URL` em `SQLALCHEMY_DATABASE_URI` com validação de ausência da variável
- Garantir que `.env` esteja listado no `.gitignore`
- Documentar os dois modos de banco (Docker local e Neon) no README
- Aplicar as migrations existentes no banco Neon com `flask db upgrade`
- Popular o banco Neon com `python scripts/seed.py`
- Configurar o GitHub Secret `DATABASE_URL` com a connection string real do Neon

## Capabilities

### New Capabilities

- `database-url-config`: Configuração centralizada de conexão ao banco via variável `DATABASE_URL`, suportando PostgreSQL local (Docker) e Neon remoto com `sslmode=require`

### Modified Capabilities

(nenhuma — as regras de negócio e requisitos de nível de spec não mudam, apenas a configuração de infraestrutura)

## Impact

- `backend/src/main.py` (ou `app.py`): leitura de `DATABASE_URL` para `SQLALCHEMY_DATABASE_URI`
- `.env.example`: novos exemplos padronizados
- `.gitignore`: verificação/adição de `.env`
- `README.md`: nova seção de configuração do banco de dados
- Banco Neon (externo): recebe migrations e dados iniciais via seed
- GitHub repository secrets: adição de `DATABASE_URL`
