## Why

Uma auditoria do projeto contra os critérios de engenharia da disciplina (Práticas XP, Pipeline CI, Qualidade de Código, Linter, Implantação de Software, Testes unitários com meta de cobertura, Testes de Integração) encontrou lacunas concretas:

1. **CI só cobre o frontend.** `.github/workflows/frontend-ci.yml` roda `npm install` + `npm run build`. Não existe nenhum workflow que rode os testes Python — nem os 46 testes em `tests/`, nem os scripts soltos na raiz (`test_models.py`, `test_db.py`).
2. **Sem medição de cobertura.** `pytest-cov`/`coverage` não estão instalados nem configurados. A meta de 90% citada na disciplina não pode ser verificada porque o número atual é desconhecido.
3. **Sem linter em nenhuma camada.** Não há ESLint no frontend (`package.json` não tem `eslint` nem script `lint`) nem ruff/flake8/black no backend — nenhum gate automático de estilo/qualidade.
4. **Testes de integração já existem, mas não rodam em CI.** `tests/test_camara_repository.py` e `tests/test_proposicoes_controller.py` já se declaram testes de integração (docstring própria: "requer BD PostgreSQL ativo") e sobem contexto Flask real contra um Postgres real via `unittest.setUpClass`. Eles nunca rodam automaticamente porque nenhum workflow provê um banco.
5. **Risco de efeito colateral em `test_models.py`.** O arquivo executa `db.create_all()` e `INSERT`s reais no nível do módulo (fora de qualquer função `test_*`). Se um workflow futuro rodar `pytest` sem escopo restrito a `tests/`, a coleta desse arquivo já dispara escrita no banco apontado por `DATABASE_URL` — antes de qualquer assert rodar.
6. **Nenhum registro formal de práticas XP.** O fluxo do time (GitFlow simplificado, PRs para `develop`) não está declarado como prática XP nem contrastado com o que falta adotar.

## What Changes

- Adiciona `.github/workflows/backend-ci.yml`: roda lint (ruff) + testes (`tests/`, unit e integração) contra um serviço Postgres do próprio GitHub Actions, aplica migrations antes dos testes, mede cobertura com `pytest-cov` e falha o build abaixo de um piso mínimo.
- Adiciona `ruff` ao backend, configurado em `pyproject.toml` (lint + format check, sem reformatar automaticamente nesta mudança).
- Adiciona ESLint (flat config, plugin Vue) ao frontend, com script `npm run lint`, plugado como novo step em `frontend-ci.yml`.
- Reorganiza `tests/` em `tests/unit/` e `tests/integration/`, deixando explícito o que já é mock (`test_camara_service.py`) vs o que exige Postgres real (`test_camara_repository.py`, `test_proposicoes_controller.py`) — sem alterar a lógica dos testes.
- Aposenta `test_models.py` e `test_db.py` da raiz (scripts manuais fora do pytest): o que ainda tem valor de asserção vira teste de verdade em `tests/integration/`; o resto é removido.
- Documenta em `design.md` quais práticas XP o time já segue informalmente hoje (branches curtas, PR para `develop`, revisão antes de merge) e quais passam a valer formalmente a partir desta mudança (CI obrigatório antes de merge, piso de cobertura, lint bloqueante).

## Capabilities

### Added
- `backend-ci`: pipeline que roda lint + testes unitários + testes de integração + relatório de cobertura no backend a cada push/PR para `main`/`develop`.
- `frontend-lint`: gate de lint (ESLint) no pipeline de frontend já existente.
- `coverage-gate`: piso mínimo de cobertura de testes do backend, medido e aplicado automaticamente pelo `backend-ci`.

### Changed
- `tests/` reorganizado em `unit/` e `integration/`; os testes de integração passam a rodar contra o Postgres provisionado pelo próprio workflow do GitHub Actions (não dependem mais de rodar só localmente).

### Removed
- `test_models.py` e `test_db.py` da raiz do repositório (scripts manuais substituídos por testes reais em `tests/integration/`, ou descartados quando redundantes).

## Impact

- **CI**: novo `backend-ci.yml`; `frontend-ci.yml` ganha um step de lint.
- **Backend**: `pyproject.toml` novo (config do ruff, pytest, coverage); `requirements.txt` ou um `requirements-dev.txt` novo com `pytest-cov` e `ruff`.
- **Frontend**: `package.json` ganha `eslint` + plugin Vue como devDependencies e script `"lint"`; `eslint.config.js` novo.
- **Testes**: `tests/` reorganizado em subpastas; 2 arquivos na raiz removidos/migrados.
- **Sem impacto**: estratégia de deploy (Vercel/`vercel.json`), schema do banco, lógica de negócio do backend e do frontend, `docker-compose.yml` (continua servindo só para dev local).
