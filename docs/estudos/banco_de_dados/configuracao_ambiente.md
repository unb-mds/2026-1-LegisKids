# Configuração do Ambiente Backend — LegisKids

> Documento referente à [Issue #31](https://github.com/unb-mds/2026-1-LegisKids/issues/31) — Configuração do ambiente e conexão com PostgreSQL.

---

## O que foi feito

Esta issue garantiu que o ambiente de desenvolvimento do backend esteja corretamente configurado para rodar o Flask conectado ao PostgreSQL. Os seguintes arquivos foram criados ou modificados:

| Arquivo | O que faz |
|---|---|
| `.env.example` | Documenta todas as variáveis de ambiente necessárias. Este arquivo **vai pro git**. |
| `.env` | Suas credenciais locais reais. Este arquivo **nunca vai pro git**. |
| `.gitignore` | Protege o `.env`, `venv/`, `site/` e outros artefatos de serem commitados. |
| `src/backend/app.py` | Entrypoint do Flask com SQLAlchemy configurado via variáveis de ambiente. |
| `src/backend/controllers/` | Pasta criada para a camada de controllers (arquitetura em camadas). |
| `src/backend/repository/` | Pasta criada para a camada de repositório (arquitetura em camadas). |
| `test_db.py` | Script que valida se a conexão com o PostgreSQL está funcionando. |
| `requirements.txt` | Adicionados: `Flask`, `Flask-SQLAlchemy`, `psycopg2-binary`, `python-dotenv`. |

### Arquitetura do backend

O backend segue arquitetura em camadas dentro de `src/backend/`:

```
src/backend/
├── app.py              ← entrypoint Flask + configuração do banco
├── main.py             ← script CLI de consumo da API da Câmara (pré-existente)
├── controllers/        ← recebe as requisições HTTP
│   └── __init__.py
├── services/           ← regras de negócio
│   └── camara_api.py
└── repository/         ← acesso ao banco de dados
    └── __init__.py
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

> ⚠️ **Importante:** sempre que abrir o projeto, ative o venv antes de qualquer coisa.

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

Copie o arquivo de exemplo e preencha com suas credenciais locais:

```bash
cp .env.example .env
```

Abra o `.env` e altere os valores:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=guardioes_da_lei
DB_USER=postgres
DB_PASSWORD=sua_senha_aqui   ← altere este campo
FLASK_APP=src/backend/app.py
FLASK_ENV=development
SECRET_KEY=qualquer-string-longa-e-aleatoria
```

> O arquivo `.env` já está no `.gitignore` — suas credenciais nunca vão para o repositório.

### 5. Criar o banco de dados

Execute uma única vez para criar o banco local:

**Linux/macOS:**
```bash
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'sua_senha';"
sudo -u postgres createdb guardioes_da_lei
```

**Windows (no PowerShell como administrador):**
```bash
psql -U postgres -c "CREATE DATABASE guardioes_da_lei;"
```

### 6. Validar a conexão

```bash
python test_db.py
```

Se tudo estiver certo, você verá:

```
✅  Conexão com o PostgreSQL estabelecida com sucesso!
```

### 7. Subir o servidor Flask

```bash
flask run
```

Acesse **http://localhost:5000/health** no navegador. A resposta esperada é:

```json
{ "status": "ok", "database": "conectado" }
```

---

## Comandos do dia a dia

| Situação | Comando |
|---|---|
| Abrir o projeto | `source venv/bin/activate` (Linux/Mac) ou `venv\Scripts\activate` (Windows) |
| Alguém adicionou pacotes | `pip install -r requirements.txt` |
| Subir o servidor | `flask run` |
| Testar conexão com o banco | `python test_db.py` |
| Visualizar a documentação | `mkdocs serve` |

---

## Problemas comuns

**`ModuleNotFoundError: No module named 'flask'`**
O venv não está ativado. Rode `source venv/bin/activate` e tente novamente.

**`externally-managed-environment`**
Você está tentando instalar pacotes fora do venv. Ative o venv primeiro.

**`python3 -m venv venv` falha**
Instale o pacote necessário: `sudo apt install python3-full python3-venv -y`

**Erro de conexão com o banco**
Verifique se o PostgreSQL está rodando e se a senha no `.env` bate com a do seu usuário `postgres`.