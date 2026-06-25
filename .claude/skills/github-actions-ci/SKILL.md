---
name: github-actions-ci
description: Use this skill when creating or editing GitHub Actions workflows (.github/workflows/*.yml) for the LegisKids project — running backend/frontend tests, linting, building Docker images, or deploying. Triggers on .github/workflows files, "pipeline", "CI/CD", or "Github Actions". For Docker build details referenced inside a workflow, also consult docker-containers.
---

# GitHub Actions — CI/CD do LegisKids

## Estrutura recomendada de workflows

```
.github/workflows/
├── backend-ci.yml     # lint + testes do Flask
├── frontend-ci.yml    # lint + testes + build do Vue
└── docker-build.yml   # build/push de imagens (opcional, em branch principal)
```

Separar por área (backend/frontend) em vez de um workflow gigante facilita reexecutar só a parte relevante e dá feedback mais rápido em PRs que tocam só um lado.

## Workflow do backend (Flask + Postgres)

```yaml
# .github/workflows/backend-ci.yml
name: Backend CI

on:
  pull_request:
    paths:
      - "backend/**"
  push:
    branches: [main]
    paths:
      - "backend/**"

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: legiskids_test
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U test"
          --health-interval 5s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Instalar dependências
        working-directory: backend
        run: pip install -r requirements.txt -r requirements-dev.txt

      - name: Lint (ruff)
        working-directory: backend
        run: ruff check .

      - name: Rodar testes
        working-directory: backend
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/legiskids_test
          SECRET_KEY: chave-de-teste
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: pytest --cov=src --cov-report=term-missing
```

Pontos importantes:
- `services: postgres` sobe um Postgres real no runner, para os testes de integração rodarem contra o mesmo banco usado em produção, não SQLite.
- `paths:` filtra o workflow para só rodar quando arquivos relevantes mudam — evita queimar minutos de CI em PRs que só tocam frontend.
- `cache: "pip"` no `setup-python` acelera builds reaproveitando dependências já baixadas.
- Segredos (como `GEMINI_API_KEY` real, se algum teste de integração precisar) vêm de `secrets.*`, nunca hardcoded no YAML.

## Workflow do frontend (Vue/Vite)

```yaml
# .github/workflows/frontend-ci.yml
name: Frontend CI

on:
  pull_request:
    paths:
      - "frontend/**"
  push:
    branches: [main]
    paths:
      - "frontend/**"

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "npm"
          cache-dependency-path: frontend/package-lock.json

      - name: Instalar dependências
        working-directory: frontend
        run: npm ci

      - name: Lint
        working-directory: frontend
        run: npm run lint

      - name: Testes unitários
        working-directory: frontend
        run: npm run test:unit -- --run

      - name: Build de produção
        working-directory: frontend
        run: npm run build
```

`npm ci` (não `npm install`) em CI — instala exatamente o que está no `package-lock.json`, builds reprodutíveis e mais rápidos.

## Boas práticas gerais

- Sempre rode lint + testes em todo PR antes de permitir merge (configurar como **required status check** na branch `main` nas configurações do repositório).
- Use `concurrency` para cancelar execuções antigas do mesmo PR quando um novo commit chega, evitando gastar minutos de CI com código já obsoleto:

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

- Nunca exponha segredos via `echo` em steps de debug, e nunca passe segredos como argumento de linha de comando visível no log.
- Para deploy, separe em um workflow próprio acionado só em push para `main` (ou em tag de release), nunca em todo PR.

## Checklist

1. Workflows separados por área (backend/frontend), com `paths:` filtrando execução.
2. Serviço de Postgres real no job de testes do backend, não SQLite/mocks puros.
3. `npm ci`/cache de dependências configurados para builds rápidos e reprodutíveis.
4. Lint + testes obrigatórios antes de merge na branch principal.
5. Segredos sempre via `secrets.*`, nunca hardcoded ou logados.
