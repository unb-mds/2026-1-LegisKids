# Tasks — pipeline-ci-qualidade

## T1 — Verificações pré-implementação

- [ ] Confirmar que `backend/src/` continua sendo código morto (`find backend -name "*.py"` deve retornar vazio, só `__pycache__`)
- [ ] Confirmar que nada importa `test_models` ou `test_db` fora deles mesmos: `grep -rn "import test_models\|import test_db" --include="*.py" .`
- [ ] Rodar `pytest tests/ -v` localmente contra o Postgres do `docker-compose.yml` e anotar quantos testes passam hoje (baseline antes da reorganização)

## T2 — Backend: dependências de dev e config

- [ ] Criar `requirements-dev.txt` na raiz com `pytest`, `pytest-cov`, `ruff` (versões fixadas, alinhadas ao Python usado no CI)
- [ ] Criar `pyproject.toml` na raiz com as seções `[tool.ruff]`, `[tool.ruff.lint]`, `[tool.pytest.ini_options]`, `[tool.coverage.run]`, `[tool.coverage.report]` conforme `design.md` seção 3
- [ ] Rodar `ruff check src/backend` localmente e corrigir (ou silenciar pontualmente com justificativa) os achados antes de ligar o gate no CI

## T3 — Reorganizar `tests/`

- [ ] Criar `tests/unit/__init__.py` e `tests/integration/__init__.py`
- [ ] Mover `tests/test_camara_service.py` → `tests/unit/test_camara_service.py`
- [ ] Mover `tests/test_camara_repository.py` → `tests/integration/test_camara_repository.py`
- [ ] Mover `tests/test_proposicoes_controller.py` → `tests/integration/test_proposicoes_controller.py`
- [ ] Rodar `pytest tests/unit/` sem banco ativo — deve passar
- [ ] Rodar `pytest tests/integration/` com `docker compose up -d db` — deve passar
- [ ] Rodar `pytest tests/` (tudo) e confirmar que o total bate com o baseline do T1

## T4 — Migrar/remover scripts da raiz

- [ ] Reescrever a asserção de `test_models.py` (serialização `to_dict()` de `Proposicao`) como teste de verdade com `assert` em `tests/integration/test_models.py`
- [ ] Remover `test_models.py` e `test_db.py` da raiz
- [ ] Confirmar que `pytest` rodado sem argumentos a partir da raiz não coleta mais nada fora de `tests/` (checar `testpaths` do `pyproject.toml`)

## T5 — Workflow `backend-ci.yml`

- [ ] Criar `.github/workflows/backend-ci.yml` conforme `design.md` seção 1 (serviço Postgres, `flask db upgrade`, `ruff check`, `pytest --cov`)
- [ ] Definir `--cov-fail-under` com valor conservador inicial (ex.: 60) — não travar em 90% sem medir antes
- [ ] Abrir PR de teste (ou rodar via `workflow_dispatch` manual) para validar que o job passa de ponta a ponta com banco real no Actions
- [ ] Anotar a cobertura real reportada pelo job e atualizar `--cov-fail-under` para esse valor (arredondado para baixo)
- [ ] Registrar no PR/description a meta de 90% como objetivo de médio prazo, não gate atual

## T6 — Frontend: ESLint

- [ ] `cd src/frontend && npm install --save-dev eslint eslint-plugin-vue`
- [ ] Criar `src/frontend/eslint.config.js` conforme `design.md` seção 6
- [ ] Adicionar script `"lint": "eslint src"` em `src/frontend/package.json`
- [ ] Rodar `npm run lint` localmente e corrigir os achados antes de ligar o gate no CI
- [ ] Adicionar step `Lint` em `.github/workflows/frontend-ci.yml`, antes do `Build`

## T7 — Configuração de repositório (fora do código)

- [ ] Habilitar branch protection em `main` e `develop` exigindo `backend-ci` e `frontend-ci` verdes antes de merge (Settings → Branches no GitHub — ação manual de um mantenedor com permissão de admin)

## T8 — Documentar decisão de práticas XP

- [ ] Confirmar que a seção 7 do `design.md` reflete a realidade do time (revisar com o time antes de arquivar a mudança — ajustar se alguma prática listada como "informal hoje" não for realmente seguida)
- [ ] Linkar essa seção a partir de algum doc de processo do time, se existir um lugar central para isso (ex.: `docs/padrao_organizacao/`) — opcional, só se não for scope creep

## T9 — Validação final

- [ ] `pytest tests/ --cov=src/backend --cov-report=term-missing` passando localmente com o piso definido em T5
- [ ] `ruff check src/backend` sem erros
- [ ] `npm run lint` sem erros em `src/frontend`
- [ ] Push de um commit trivial para confirmar que `backend-ci.yml` e `frontend-ci.yml` disparam e passam no GitHub Actions
