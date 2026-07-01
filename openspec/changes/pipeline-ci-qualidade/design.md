# Design — pipeline-ci-qualidade

## Arquivos afetados

| Arquivo | Ação |
|---|---|
| `.github/workflows/backend-ci.yml` | Criar |
| `.github/workflows/frontend-ci.yml` | Editar — adiciona step de lint |
| `pyproject.toml` (raiz) | Criar — config do ruff, pytest, coverage |
| `requirements-dev.txt` (raiz) | Criar — `pytest`, `pytest-cov`, `ruff` |
| `src/frontend/eslint.config.js` | Criar |
| `src/frontend/package.json` | Editar — devDependencies + script `lint` |
| `tests/unit/` | Criar — move `test_camara_service.py` |
| `tests/integration/` | Criar — move `test_camara_repository.py`, `test_proposicoes_controller.py` |
| `test_models.py`, `test_db.py` (raiz) | Remover / migrar conteúdo útil para `tests/integration/` |
| `conftest.py` (raiz) | Manter — já centraliza `load_dotenv()` + `FLASK_ENV=testing` |

---

## 1. `backend-ci.yml`

Roda em push/PR para `main` e `develop`, escopado aos paths que afetam o backend (evita rodar em PRs que só tocam frontend/docs).

```yaml
name: Backend CI

on:
  push:
    branches: [main, develop]
    paths:
      - 'src/backend/**'
      - 'tests/**'
      - 'migrations/**'
      - 'requirements*.txt'
      - 'pyproject.toml'
  pull_request:
    branches: [main, develop]
    paths:
      - 'src/backend/**'
      - 'tests/**'
      - 'migrations/**'
      - 'requirements*.txt'
      - 'pyproject.toml'

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: legiskids_test
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
        options: >-
          --health-cmd "pg_isready -U postgres -d legiskids_test"
          --health-interval 5s
          --health-timeout 5s
          --health-retries 5

    env:
      DATABASE_URL: postgresql://postgres:postgres@localhost:5432/legiskids_test
      FLASK_APP: src/backend/app.py
      FLASK_ENV: testing

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint (ruff)
        run: ruff check src/backend

      - name: Apply migrations
        run: flask db upgrade

      - name: Run tests with coverage
        run: |
          pytest tests/ \
            --cov=src/backend \
            --cov-report=term-missing \
            --cov-report=xml \
            --cov-fail-under=${{ vars.COVERAGE_MIN || 60 }}
```

**Por que `--cov-fail-under` vem de uma variável com fallback:** a cobertura atual do projeto nunca foi medida. Ver seção "Piso de cobertura" abaixo — a tarefa de implementação inclui rodar isso uma vez, anotar o número real e travar o piso definitivo no workflow (não deixar como `vars.COVERAGE_MIN` indefinidamente).

**Por que só `src/backend` no lint/coverage:** `backend/src/` é código morto (só contém `__pycache__`, sem `.py` versionado) — não deve ser incluído em cobertura nem lint.

---

## 2. Piso de cobertura — medir antes de travar

A cobertura atual é desconhecida porque `pytest-cov` nunca rodou no projeto. Não é seguro travar `--cov-fail-under=90` de imediato — isso quebraria o CI no primeiro PR sem dar ao time uma base real para trabalhar.

**Sequência:**
1. Implementar o pipeline com `--cov-fail-under` frouxo (ex.: 60, valor de segurança conservador — ajustar depois de rodar).
2. Rodar `pytest tests/ --cov=src/backend --cov-report=term-missing` localmente (ou observar o primeiro run do CI) e anotar o número real.
3. Atualizar `--cov-fail-under` no workflow para o valor medido (arredondado para baixo), documentando em `tasks.md` o número encontrado.
4. Meta de 90% citada pela disciplina fica registrada como objetivo de médio prazo (não gate imediato) — subir o piso gradualmente em PRs futuros conforme a cobertura aumentar organicamente.

Esse é o mesmo motivo pelo qual não travamos o número aqui: qualquer valor "chutado" nesta proposta ficaria desatualizado assim que o CI rodar pela primeira vez.

---

## 3. `pyproject.toml` — ruff + pytest + coverage

```toml
[tool.ruff]
line-length = 120
target-version = "py311"
exclude = ["backend", "migrations", "venv"]

[tool.ruff.lint]
select = ["E", "F", "I", "W"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]

[tool.coverage.run]
source = ["src/backend"]
omit = ["src/backend/schedulers/*"]

[tool.coverage.report]
exclude_lines = ["pragma: no cover", "if __name__ == .__main__.:"]
```

`testpaths = ["tests"]` é a peça que evita o risco descrito no `proposal.md`: `pytest` sem argumentos (ou rodado a partir da raiz num workflow futuro) nunca mais coleta `test_models.py`/`test_db.py` da raiz — porque esses arquivos deixam de existir ali (seção 5) e porque o escopo fica travado em `tests/`.

`exclude = ["backend", ...]` no ruff evita lint em `backend/src/` (código morto).

---

## 4. Reorganização de `tests/`

Estado atual → estado proposto:

| Arquivo atual | Destino | Motivo |
|---|---|---|
| `tests/test_camara_service.py` | `tests/unit/test_camara_service.py` | Já mockado (`unittest.mock.patch`), não toca banco real — é unitário de fato. |
| `tests/test_camara_repository.py` | `tests/integration/test_camara_repository.py` | Já se autodeclara "requer BD PostgreSQL ativo" na docstring; sobe `app_context()` real via `setUpClass`. |
| `tests/test_proposicoes_controller.py` | `tests/integration/test_proposicoes_controller.py` | Mesma situação — usa app + DB reais. |
| `tests/__init__.py` | `tests/__init__.py` (mantém) + `tests/unit/__init__.py` + `tests/integration/__init__.py` (novos) | Necessário para os módulos serem importáveis como pacote. |

Nenhuma lógica de teste muda — só localização, e o cabeçalho/docstring de cada arquivo já documentava corretamente qual categoria era. Isso também deixa explícito, para quem for rodar localmente, quais testes exigem `docker compose up db` antes:

```bash
pytest tests/unit/                          # não precisa de banco
docker compose up -d db && pytest tests/integration/   # precisa
pytest tests/                                # tudo (é o que o CI roda)
```

---

## 5. `test_models.py` e `test_db.py` (raiz)

**`test_db.py`**: script de smoke-test de conexão (`if __name__ == "__main__"`). Tem uma função `test_connection()` que o pytest colotaria por engano (nome com prefixo `test_`), mas ela só faz `print` e `return True/False` — nunca `assert` nem `raise` em caso de falha textual, então "passa" mesmo quando a conexão falha silenciosamente (só o `print` do ❌ denuncia, e isso não aparece como falha no relatório do pytest). **Remover**: não agrega cobertura real e o `pg_isready` do healthcheck do serviço Postgres no CI já cobre esse caso.

**`test_models.py`**: sem nenhuma função `test_*` — é um script que roda `db.create_all()` e insere dados reais no nível do módulo, executado hoje manualmente com `python test_models.py`. Risco: se um workflow futuro (ou um dev local) rodar `pytest` sem escopo restrito a `tests/`, o pytest **coleta o arquivo na fase de import** e o corpo do módulo executa como efeito colateral da coleta — escrevendo no banco apontado por `DATABASE_URL` antes de qualquer assert. Ação: reescrever a asserção útil (`to_dict()` de `Proposicao` serializa corretamente) como um teste de verdade em `tests/integration/test_models.py`, com `assert` e fixture de banco de teste; descartar o resto do script.

---

## 6. ESLint no frontend

`src/frontend/eslint.config.js` (flat config, compatível com ESLint 10 + Vite 5):

```js
import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import globals from 'globals'

export default [
  { ignores: ['dist/**', 'node_modules/**'] },
  js.configs.recommended,
  ...pluginVue.configs['flat/essential'],
  {
    languageOptions: {
      globals: { ...globals.browser },
    },
    rules: {
      'vue/multi-word-component-names': 'off',
    },
  },
]
```

`package.json` ganha:

```json
"scripts": {
  "lint": "eslint src"
},
"devDependencies": {
  "@eslint/js": "^10.0.1",
  "eslint": "^10.6.0",
  "eslint-plugin-vue": "^10.9.2",
  "globals": "^17.7.0"
}
```

**Por que `flat/essential` e não `flat/recommended`:** `flat/recommended` inclui as camadas "strongly-recommended" do eslint-plugin-vue, que são regras de formatação (quebra de linha por atributo, self-closing tags, espaçamento em fechamento de tag) — ao rodar contra o código já existente, gerou **1076 problemas**, quase todos estéticos, sem relação com corretude. Retrofitar isso significaria reformatar dezenas de arquivos `.vue` já revisados visualmente, o que contraria a diretriz do projeto de não alterar identidade visual/formatação sem necessidade. `flat/essential` mantém só as regras de corretude do Vue (chaves de `v-for`, uso correto de diretivas, side-effects em computed) — rodando junto com `js.configs.recommended` (que cobre `no-unused-vars`, `no-undef` etc.), reduziu para **3 problemas reais**, todos corrigidos durante a implementação (dois `catch (e)` com variável não usada, uma função `irParaProposicao` morta em `DetalheView.vue` que arrastava um `useRouter()` também não usado).

`globals.browser` é necessário porque `js.configs.recommended` sozinho não declara `window`/`navigator`/`setTimeout` como globais conhecidos — sem isso, todo uso desses objetos no `<script setup>` dispara falso-positivo de `no-undef`.

`vue/multi-word-component-names` desligado porque o projeto já tem views nomeadas em uma palavra só (`SobreView.vue`, `BuscaView.vue` etc. são compostos, mas convém não travar nomes de componente a essa convenção sem alinhar com o time antes).

`frontend-ci.yml` ganha um step entre "Install dependencies" e "Build":

```yaml
      - name: Lint
        run: npm run lint
        working-directory: src/frontend
```

---

## 7. Práticas XP — o que já é seguido vs o que passa a ser formal

Não é código — é registro de decisão de processo do time, para constar como resposta ao critério de avaliação.

**Já seguido informalmente hoje** (evidência no repo, não inventado):
- **Small releases / branches curtas**: `CONTRIBUTING.md` já define fluxo de branch por issue (`feature/numero-issue-nome`) e PRs pequenos e objetivos.
- **Coding standards**: convenção de commits (`feat:`, `fix:`, etc.) e padrão de nome de branch já documentados e seguidos (ver histórico de commits).
- **Continuous integration (parcial)**: já existe build automático do frontend a cada PR — só faltava cobrir o backend, o que esta mudança resolve.
- **Collective code ownership**: múltiplos arquivos em `openspec/changes/` mostram mudanças de features diferentes por partes distintas do time, sem dono fixo de módulo.

**Passa a valer formalmente a partir desta mudança:**
- **CI obrigatório antes de merge**: PR para `main`/`develop` só pode ser mergeado com `backend-ci` e `frontend-ci` verdes (configurar branch protection no GitHub — ação manual fora do escopo de código desta proposta, listada em `tasks.md` como item de configuração do repositório).
- **Sustainable pace / testing discipline**: testes (unitários + integração) rodando a cada push, não só quando alguém lembra de rodar localmente.
- **Refactoring com rede de segurança**: com CI + cobertura mínima, fica seguro fazer limpezas como `limpeza-backend` (já feita anteriormente) com menos risco de regressão silenciosa.

**Não adotado, e não fingir que é**: pair programming e TDD estrito não são práticas formalizadas neste projeto acadêmico — o time já escreve testes, mas não necessariamente antes do código de produção. Não vamos declarar isso como adotado; fica registrado como lacuna real, não fechada por esta mudança.
