# Configuração do Ambiente e Banco de Dados — LegisKids

> Este documento cobre três issues:
> - [Issue #31](https://github.com/unb-mds/2026-1-LegisKids/issues/31) — Configuração do ambiente e conexão com PostgreSQL
> - Issue de Modelagem — Criação das tabelas principais do banco de dados
> - Issue de Migrations — Versionamento do schema com Flask-Migrate

---

## O que foi feito

### Issue #31 — Ambiente e conexão com PostgreSQL

| Arquivo | O que faz |
|---|---|
| `.env.example` | Documenta todas as variáveis de ambiente. Este arquivo **vai pro git**. |
| `.env` | Suas credenciais locais reais. Este arquivo **nunca vai pro git**. |
| `.gitignore` | Protege o `.env`, `venv/`, `site/` e outros artefatos. |
| `src/backend/app.py` | Entrypoint do Flask com SQLAlchemy configurado via variáveis de ambiente. Inclui rota `/health` para checar o banco. |
| `src/backend/database.py` | Instância isolada do `db` (SQLAlchemy). Separado do `app.py` para evitar importação circular. |
| `src/backend/controllers/` | Pasta da camada de controllers (arquitetura em camadas). |
| `src/backend/repository/` | Pasta da camada de repositório (arquitetura em camadas). |
| `test_db.py` | Valida se a conexão com o PostgreSQL está funcionando. |
| `requirements.txt` | Adicionados: `Flask`, `Flask-SQLAlchemy`, `psycopg2-binary`, `python-dotenv`, `Flask-Migrate`. |

### Issue de Modelagem — Tabelas do banco de dados

| Arquivo | O que faz |
|---|---|
| `src/backend/models.py` | Modelos SQLAlchemy de todas as tabelas — use para interagir com o banco via Python. |
| `src/backend/migrations/create_tables.sql` | SQL de referência das tabelas. Não usar para criar o banco — use `flask db upgrade`. |
| `src/backend/migrations/test_tables.py` | Testa a criação, inserção e relacionamentos de todas as tabelas. |

### Issue de Migrations — Flask-Migrate

| Arquivo/Pasta | O que faz |
|---|---|
| `migrations/` | Pasta gerada pelo Flask-Migrate com todo o histórico de versões do banco. |
| `migrations/versions/` | Arquivos de migration gerados automaticamente pelo Alembic. |
| `migrations/env.py` | Configuração do Alembic para detectar os models do projeto. |

---

## Por que Flask-Migrate?

Sem versionamento de banco, cada integrante precisaria rodar o SQL manualmente e qualquer mudança no schema precisaria ser comunicada por fora. Com o Flask-Migrate:

- O banco é **reproduzido do zero** com um único comando (`flask db upgrade`)
- Mudanças no schema viram **arquivos commitados** — rastreáveis pelo git
- É possível **reverter** alterações sem perder dados (`flask db downgrade`)
- Novos integrantes não precisam entender o SQL — só rodar o comando

---

## Por que o `database.py` existe?

O `db` (instância do SQLAlchemy) foi separado do `app.py` em um arquivo próprio (`database.py`) para evitar **importação circular**:

- `app.py` precisa importar `models.py` para o Flask-Migrate detectar as tabelas
- `models.py` precisa importar `db` para definir os modelos
- Se `db` ficasse no `app.py`, teríamos um ciclo: `app → models → app`

Com o `database.py` quebramos esse ciclo:

```
app.py    →  database.py  (importa db)
models.py →  database.py  (importa db)
app.py    →  models.py    (importa os modelos)
```

---

## Arquitetura do backend

```
src/backend/
├── app.py                  ← entrypoint Flask + configuração do banco
├── database.py             ← instância do db (SQLAlchemy) — separado para evitar ciclo
├── models.py               ← modelos SQLAlchemy (todas as tabelas)
├── main.py                 ← script CLI de consumo da API da Câmara (pré-existente)
├── migrations/
│   ├── create_tables.sql   ← SQL de referência (documentação)
│   └── test_tables.py      ← script de teste das tabelas
├── controllers/            ← recebe as requisições HTTP
│   └── __init__.py
├── services/               ← regras de negócio
│   └── camara_api.py
└── repository/             ← acesso ao banco de dados
    └── __init__.py

migrations/                 ← gerado pelo Flask-Migrate (na raiz do projeto)
├── env.py
├── alembic.ini
├── script.py.mako
└── versions/
    └── xxxx_initial_schema.py
```

---

## Tabelas criadas

| Tabela | Finalidade |
|---|---|
| `partidos` | Partidos políticos associados às proposições |
| `proposicoes` | Proposições legislativas coletadas da API da Câmara |
| `tramitacoes` | Histórico de tramitação de cada proposição |
| `usuarios` | Usuários autenticados via Google OAuth |
| `favoritos` | Proposições salvas por usuários |
| `historico_consultas` | Histórico de pesquisas dos usuários |
| `requisicoes_api` | Monitoramento e auditoria das coletas da API |

### Relacionamentos

```
partidos ──────────────── proposicoes          (1 para N)
proposicoes ──────────── tramitacoes           (1 para N)
proposicoes ──────────── favoritos             (1 para N)
usuarios ─────────────── favoritos             (1 para N)
usuarios ─────────────── historico_consultas   (1 para N)
```

---

## Pré-requisitos

Antes de começar, você precisa ter instalado:

- **Python 3.11+** — [python.org/downloads](https://python.org/downloads)
- **PostgreSQL** — [postgresql.org/download](https://postgresql.org/download)
- **Git** — [git-scm.com](https://git-scm.com)

---

## Passo a passo para novos integrantes

### 1. Clonar o repositório

```bash
git clone https://github.com/unb-mds/2026-1-LegisKids.git
cd 2026-1-LegisKids
```

### 2. Criar e ativar o ambiente virtual

> ⚠️ **Sempre que abrir o projeto, ative o venv antes de qualquer coisa.**

O ambiente virtual isola as dependências do projeto do Python do seu sistema — evita conflitos entre versões de bibliotecas.

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

O terminal deve mostrar `(venv)` no início da linha quando estiver ativado.

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar as variáveis de ambiente

```bash
cp .env.example .env
```

Abra o `.env` e altere os valores:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=legiskids
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui
FLASK_APP=src/backend/app.py
FLASK_ENV=development
SECRET_KEY=qualquer-string-longa-e-aleatoria
PYTHONPATH=/caminho/absoluto/para/2026-1-LegisKids
```

> O `PYTHONPATH` precisa apontar para a raiz do projeto. No Linux/macOS você pode usar `pwd` dentro da pasta para descobrir o caminho completo.

> O arquivo `.env` já está no `.gitignore` — suas credenciais nunca vão para o repositório.

### 5. Criar o banco de dados

Execute uma única vez:

**Linux/macOS:**
```bash
psql -U postgres -h localhost -c "CREATE DATABASE legiskids;"
```

**Windows (PowerShell como administrador):**
```bash
psql -U postgres -c "CREATE DATABASE legiskids;"
```

Para verificar se o banco foi criado:
```bash
psql -U postgres -h localhost -c "\l"
```

### 6. Criar as tabelas com Flask-Migrate

> ⚠️ **Não use mais o `create_tables.sql` para criar o banco.** O Flask-Migrate é agora o responsável por isso. O SQL existe apenas como referência/documentação.

```bash
flask db upgrade
```

Esse comando lê os arquivos de migration em `migrations/versions/` e cria todas as tabelas automaticamente. É o único comando necessário — funciona em banco zerado.

### 7. Validar a conexão com o banco

```bash
python test_db.py
```

Saída esperada:
```
✅  Conexão com o PostgreSQL estabelecida com sucesso!
```

### 8. Testar as tabelas

```bash
python src/backend/migrations/test_tables.py
```

Saída esperada:
```
═══════════════════════════════════════════════════════
  LegisKids — Teste de tabelas do banco de dados
═══════════════════════════════════════════════════════
  ✅ Conexão com o banco estabelecida
── 1. Verificando tabelas ───────────────────────────────
  ✅ Tabela 'favoritos' existe
  ✅ Tabela 'historico_consultas' existe
  ✅ Tabela 'partidos' existe
  ✅ Tabela 'proposicoes' existe
  ✅ Tabela 'requisicoes_api' existe
  ✅ Tabela 'tramitacoes' existe
  ✅ Tabela 'usuarios' existe
── 2. Verificando campo 'categoria' em proposicoes ─────
  ✅ Campo 'categoria' existe em 'proposicoes'
── 3. Testando inserção de dados ───────────────────────
  ✅ Inseriu partido
  ✅ Inseriu proposição com categoria
  ✅ Inseriu tramitação
  ✅ Inseriu usuário
  ✅ Inseriu favorito
  ✅ Inseriu histórico de consulta
  ✅ Inseriu requisição de API
── 4. Testando consultas e relacionamentos ──────────────
  ✅ Consultou proposição
  ✅ Campo categoria correto
  ✅ Relacionamento partido OK
  ✅ Relacionamento tramitações OK
  ✅ Relacionamento favoritos OK
  ✅ Relacionamento histórico OK
── 5. Limpando dados de teste ──────────────────────────
  ✅ Dados de teste descartados (rollback)
═══════════════════════════════════════════════════════
  RESULTADO: todos os testes passaram ✅
═══════════════════════════════════════════════════════
```

### 9. Subir o servidor Flask

```bash
flask run
```

Acesse **http://localhost:5000/health** no navegador. A resposta esperada é:

```json
{ "status": "ok", "database": "conectado" }
```

---

## Como trabalhar com migrations nas próximas issues

### Se você alterar um modelo existente ou criar um novo

Sempre que modificar o `models.py` (adicionar campo, tabela, mudar tipo), gere uma nova migration:

```bash
# 1. Gera o arquivo de migration automaticamente
flask db migrate -m "descricao da mudanca"

# 2. Revise o arquivo gerado em migrations/versions/
# Verifique se o que foi gerado faz sentido

# 3. Aplica a migration no banco
flask db upgrade
```

> ⚠️ **Sempre commite o arquivo de migration junto com a mudança no model.** Outros integrantes precisam dele para atualizar o banco local.

### Se você puxou mudanças do git e o banco está desatualizado

```bash
flask db upgrade
```

Esse comando detecta automaticamente quais migrations ainda não foram aplicadas e roda só as novas.

### Se precisar reverter uma migration

```bash
# Volta uma migration
flask db downgrade

# Volta até o início (banco zerado)
flask db downgrade base
```

### Ver o histórico de migrations

```bash
flask db history
```

---

## Como usar os modelos nas próximas issues

O `models.py` já está pronto para ser importado. O `db` deve ser importado de `database.py`, não de `app.py`.

### Inserir dados via Python

```python
from src.backend.app import app
from src.backend.database import db
from src.backend.models import Partido, Proposicao

with app.app_context():
    partido = Partido(id=36844, sigla="PT", nome="Partido dos Trabalhadores")
    db.session.add(partido)
    db.session.commit()
```

### Consultar dados

```python
from src.backend.app import app
from src.backend.models import Proposicao

with app.app_context():
    # Todas as proposições
    proposicoes = Proposicao.query.all()

    # Filtrar por categoria
    props_cyber = Proposicao.query.filter_by(categoria="cyberbullying").all()

    # Filtrar por ano
    props_2024 = Proposicao.query.filter_by(ano=2024).all()
```

### Usar no repository (camada de acesso ao banco)

```python
# src/backend/repository/proposicao_repository.py
from src.backend.database import db
from src.backend.models import Proposicao

def buscar_todas():
    return Proposicao.query.all()

def buscar_por_id(id):
    return Proposicao.query.get(id)

def inserir(proposicao: Proposicao):
    db.session.add(proposicao)
    db.session.commit()
    return proposicao
```

---

## Comandos do dia a dia

| Situação | Comando |
|---|---|
| Abrir o projeto | `source venv/bin/activate` (Linux/Mac) ou `venv\Scripts\activate` (Windows) |
| Alguém adicionou pacotes | `pip install -r requirements.txt` |
| Subir o servidor | `flask run` |
| Testar conexão com o banco | `python test_db.py` |
| Testar as tabelas | `python src/backend/migrations/test_tables.py` |
| Criar tabelas / atualizar banco | `flask db upgrade` |
| Reverter última migration | `flask db downgrade` |
| Gerar nova migration após mudar model | `flask db migrate -m "descricao"` |
| Ver histórico de migrations | `flask db history` |
| Visualizar a documentação | `mkdocs serve` |

---

## Problemas comuns

**`ModuleNotFoundError: No module named 'flask'`**
O venv não está ativado. Rode `source venv/bin/activate` e tente novamente.

**`externally-managed-environment`**
Você está tentando instalar pacotes fora do venv. Ative o venv primeiro.

**`python3 -m venv venv` falha**
Instale o pacote necessário: `sudo apt install python3-full python3-venv -y`

**`Peer authentication failed for user "postgres"`**
Adicione `-h localhost` ao comando psql: `psql -U postgres -h localhost ...`

**`Error: No such command 'db'`**
O Flask não está encontrando o app. Verifique se o `.env` tem `FLASK_APP=src/backend/app.py` e `PYTHONPATH` apontando para a raiz do projeto.

**`No changes in schema detected` ao rodar `flask db migrate`**
O Alembic não está enxergando os models. Verifique se o `PYTHONPATH` está configurado no `.env` e se o `app.py` importa os models corretamente.

**Erro de conexão com o banco**
Verifique se o PostgreSQL está rodando e se a senha no `.env` bate com a do seu usuário `postgres`.

**Banco desatualizado após puxar mudanças do git**
Rode `flask db upgrade` para aplicar as migrations novas.