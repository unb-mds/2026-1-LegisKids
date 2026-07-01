# Tasks — pipeline-ci-qualidade

## T1 — Verificações pré-implementação

- [x] Confirmar que `backend/src/` continua sendo código morto (`find backend -name "*.py"` deve retornar vazio, só `__pycache__`)
- [x] Confirmar que nada importa `test_models` ou `test_db` fora deles mesmos: `grep -rn "import test_models\|import test_db" --include="*.py" .`
- [x] Rodar `pytest tests/ -v` localmente contra o Postgres do `docker-compose.yml` e anotar quantos testes passam hoje (baseline antes da reorganização) — **baseline: 46/46 passando**

## T2 — Backend: dependências de dev e config

- [x] Criar `requirements-dev.txt` na raiz com `pytest==9.1.1`, `pytest-cov==7.1.0`, `ruff==0.15.20` (versões instaladas no ambiente local)
- [x] Criar `pyproject.toml` na raiz com as seções `[tool.ruff]`, `[tool.ruff.lint]`, `[tool.pytest.ini_options]`, `[tool.coverage.run]`, `[tool.coverage.report]` conforme `design.md` seção 3 — `line-length` ajustado de 100 para 120 (o código existente usa alinhamento vertical deliberado em `models.py`; 100 gerava 39 achados triviais de `E501`)
- [x] Rodar `ruff check src/backend` localmente e corrigir (ou silenciar pontualmente com justificativa) os achados antes de ligar o gate no CI — resultado: **52 → 0 erros**. Auto-fix (`--fix`) resolveu 9 (imports desordenados, `except Exception as exc` não usado, newline final faltando). `E402` em `app.py` (4 imports após config do Flask) recebeu `# noqa: E402` — é padrão intencional já usado no arquivo (`# noqa: F401` preexistente) para evitar import circular. 7 `E501` remanescentes (linhas de `models.py`/`camara_repository.py` com alinhamento vertical ou string longa) receberam `# noqa: E501` pontual em vez de reformatar o arquivo.

## T3 — Reorganizar `tests/`

- [x] Criar `tests/unit/__init__.py` e `tests/integration/__init__.py`
- [x] Mover `tests/test_camara_service.py` → `tests/unit/test_camara_service.py`
- [x] Mover `tests/test_camara_repository.py` → `tests/integration/test_camara_repository.py`
- [x] Mover `tests/test_proposicoes_controller.py` → `tests/integration/test_proposicoes_controller.py`
- [x] Rodar `pytest tests/unit/` — 22 passando
- [x] Rodar `pytest tests/integration/` — 24 passando (contra o Postgres já configurado no `.env` local)
- [x] Rodar `pytest tests/` (tudo) — 46 passando, bate com o baseline do T1

## T4 — Migrar/remover scripts da raiz

- [x] Reescrever a asserção de `test_models.py` (serialização `to_dict()` de `Partido`/`Proposicao`/`Usuario`/`Favorito`) como teste de verdade com `assert` em `tests/integration/test_models.py` — segue o padrão `setUpClass`/`tearDownClass` com ID sentinela (`9999900`) e limpeza dos próprios dados, já usado em `test_proposicoes_controller.py`
- [x] Remover `test_models.py` e `test_db.py` da raiz
- [x] Confirmar que `pytest` rodado sem argumentos a partir da raiz não coleta mais nada fora de `tests/` — `pytest --collect-only -q` retorna 50 testes, todos sob `tests/` (`testpaths = ["tests"]` no `pyproject.toml`)

## T5 — Workflow `backend-ci.yml`

- [x] Criar `.github/workflows/backend-ci.yml` conforme `design.md` seção 1 (serviço Postgres, `flask db upgrade`, `ruff check`, `pytest --cov`)
- [x] Medir cobertura real localmente antes de travar o piso: `pytest tests/ --cov=src/backend --cov-report=term-missing` → **78% total** (`app.py` 66%, `cron_controller.py` 37%, `proposicoes_controller.py` 55%, `models.py` 90%, `camara_repository.py` 75%, `camara_service.py` 84%)
- [x] Definir `--cov-fail-under=75` no workflow — abaixo dos 78% medidos localmente (margem de segurança para variação natural entre execuções), muito acima de um piso "chutado". Meta de 90% da disciplina registrada como objetivo de médio prazo, não gate atual — `cron_controller.py` (37%) e `proposicoes_controller.py` (55%) são os maiores contribuintes para o gap e ficam como trabalho futuro de cobertura.
- [ ] **Pendente — requer ação do usuário**: abrir PR de teste (ou rodar via `workflow_dispatch` manual) para validar que o job passa de ponta a ponta com o Postgres do GitHub Actions. Não foi possível simular isso localmente — o ambiente de implementação não tem acesso ao socket do Docker (`permission denied` ao tentar subir um Postgres efêmero), e abrir um PR/push é uma ação visível a terceiros que requer confirmação explícita antes de ser executada.

## T6 — Frontend: ESLint

- [x] `cd src/frontend && npm install --save-dev eslint eslint-plugin-vue @eslint/js globals`
- [x] Criar `src/frontend/eslint.config.js` conforme `design.md` seção 6 — usando `flat/essential` (não `flat/recommended`, ver justificativa no design.md)
- [x] Adicionar script `"lint": "eslint src"` em `src/frontend/package.json`
- [x] Rodar `npm run lint` localmente e corrigir os achados antes de ligar o gate no CI — 3 achados reais corrigidos: `catch (e)` sem uso de `e` em `AnalisesView.vue` e `DashboardView.vue` (padronizado para `catch {}`, já era o padrão em `DetalheView.vue`); função `irParaProposicao` morta em `DetalheView.vue` removida, junto com o `useRouter()`/import que só ela usava. `npm run build` confirmado funcionando após as remoções.
- [x] Adicionar step `Lint` em `.github/workflows/frontend-ci.yml`, antes do `Build`

## T7 — Configuração de repositório (fora do código)

- [ ] **Pendente — ação manual de um mantenedor com permissão de admin**: habilitar branch protection em `main` e `develop` exigindo `backend-ci` e `frontend-ci` verdes antes de merge (Settings → Branches no GitHub). Não é uma ação de código — só é possível depois que os workflows rodarem ao menos uma vez no Actions (os status checks só aparecem como opção depois do primeiro run).

## T8 — Documentar decisão de práticas XP

- [x] Seção 7 do `design.md` escrita a partir de evidência real do repositório (`CONTRIBUTING.md`, histórico de commits, `openspec/changes/`), não inventada — pronta para revisão do time antes do archive
- [ ] Linkar essa seção a partir de algum doc de processo do time (ex.: `docs/padrao_organizacao/`) — **não feito nesta implementação**: nenhum lugar central óbvio foi identificado sem correr risco de scope creep; decisão fica para o time avaliar durante a revisão do PR

## T9 — Validação final

- [x] `pytest tests/ --cov=src/backend --cov-fail-under=75` passando localmente — 50/50 testes, cobertura 77.76%
- [x] `ruff check src/backend` sem erros
- [x] `npm run lint` sem erros em `src/frontend`
- [ ] **Pendente — requer `git push`**: confirmar que `backend-ci.yml` e `frontend-ci.yml` disparam e passam no GitHub Actions de verdade (não simulável localmente neste ambiente — sem acesso ao socket do Docker). Ação a ser feita pelo usuário ou por mim mediante autorização explícita, fora desta sessão de implementação local.
