# Configuração de Banco de Dados via DATABASE_URL — LegisKids

> Este documento cobre a issue de configuração unificada do banco de dados:
> substituição das 5 variáveis separadas por uma única `DATABASE_URL`, suporte a
> banco local Docker e banco remoto Neon, e criação do script de seed de dados iniciais.

---

## O que foi feito

### Mudança principal: de 5 variáveis para `DATABASE_URL`

O `app.py` costumava montar a URI do banco manualmente a partir de cinco variáveis separadas:

```env
# Formato antigo (não usar mais)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=legiskids
DB_USER=postgres
DB_PASSWORD=sua_senha
```

Agora o sistema usa uma única variável `DATABASE_URL` — o padrão adotado por praticamente todo ecossistema Python/PostgreSQL:

```env
# Formato atual
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/legiskids
```

Essa mudança permite trocar de banco (local → Neon → qualquer outro) alterando apenas um valor no `.env`, sem mexer em código.

### Arquivos criados ou alterados

| Arquivo | O que mudou |
|---|---|
| `src/backend/app.py` | Removida montagem manual de URI; lê `DATABASE_URL` via `os.getenv()`; levanta `RuntimeError` se não definida |
| `.env.example` | Atualizado com exemplos de `DATABASE_URL` para banco local Docker e banco Neon |
| `.env` | Atualizado para o novo formato (arquivo local, não vai pro git) |
| `docker-compose.yml` | Criado — sobe PostgreSQL 16 localmente via Docker sem instalar nada no sistema |
| `scripts/seed.py` | Criado — popula o banco com dados iniciais (partidos); idempotente |
| `README.md` | Seção "Configurar o banco de dados" atualizada com instruções para os dois ambientes |

---

## Os dois ambientes de banco

### Banco local com Docker (desenvolvimento diário)

Usado por padrão para desenvolvimento. O banco roda em container e não exige PostgreSQL instalado no sistema.

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/legiskids
```

**Validado:** migrations aplicadas e seed executado com sucesso (17 partidos inseridos).

### Banco Neon (homologação e produção)

Banco PostgreSQL gerenciado na nuvem, acessado via connection string com SSL obrigatório.

```env
DATABASE_URL=postgresql://<usuario>:<senha>@<host>.neon.tech/<banco>?sslmode=require&channel_binding=require
```

**Validado:** `flask db upgrade` e `python scripts/seed.py` executados com sucesso no banco remoto — tabelas criadas e 17 partidos inseridos no Neon.

> A connection string real do Neon **nunca deve ser commitada**. Obtenha-a no painel do
> [Neon](https://neon.tech) ou peça a um integrante do time via canal seguro.

---

## Passo a passo para novos integrantes

### 1. Clonar o repositório e criar o venv

```bash
git clone https://github.com/unb-mds/2026-1-LegisKids.git
cd 2026-1-LegisKids

# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar o `.env`

```bash
cp .env.example .env
```

O `.env` padrão já aponta para o banco Docker local. Não precisa alterar nada para começar:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/legiskids
FLASK_APP=src/backend/app.py
FLASK_ENV=development
SECRET_KEY=troque-por-uma-chave-secreta-longa-e-aleatoria
```

### 4. Subir o banco local com Docker

```bash
docker compose up -d
```

Aguarde o container ficar saudável (status `healthy`):

```bash
docker compose ps
```

> O volume `legiskids_db_data` persiste os dados entre reinicializações.
> Para apagar tudo e começar do zero: `docker compose down -v`

### 5. Aplicar o schema (migrations)

```bash
python -m flask --app src/backend/app.py db upgrade
```

Saída esperada:

```
INFO  [alembic.runtime.migration] Running upgrade  -> 7deb4eaf030e, initial schema
```

Se o banco já estiver atualizado, o comando não faz nada (seguro rodar sempre).

### 6. Popular o banco com dados iniciais

```bash
python scripts/seed.py
```

Saída esperada:

```
═══════════════════════════════════════════════════════
  LegisKids — Seed de dados iniciais
  Banco: localhost:5432/legiskids
═══════════════════════════════════════════════════════

── Partidos ─────────────────────────────────────────────
  17 inserido(s) | 0 atualizado(s) | 0 sem alteração

═══════════════════════════════════════════════════════
  Seed concluído com sucesso.
═══════════════════════════════════════════════════════
```

O seed é **idempotente**: pode ser rodado mais de uma vez sem criar duplicatas.

### 7. Verificar que o Flask sobe corretamente

```bash
python -m flask --app src/backend/app.py run
```

Acesse **http://localhost:5000/health**. Resposta esperada:

```json
{ "status": "ok", "database": "conectado" }
```

---

## Como testar no banco Neon

Quando precisar validar migrations ou dados no banco remoto (Neon), siga os passos abaixo.
Isso é necessário uma vez por integrante ou sempre que houver nova migration.

### 1. Trocar o `DATABASE_URL` no `.env` para o Neon

Abra o `.env` e substitua a linha do `DATABASE_URL`:

```env
# Temporário — aponta para o Neon
DATABASE_URL=postgresql://<usuario>:<senha>@<host>.neon.tech/<banco>?sslmode=require&channel_binding=require
```

> Obtenha a connection string real com um colega do time ou no painel do Neon.
> **Não commite** esse valor.

### 2. Aplicar migrations no Neon

```bash
python -m flask --app src/backend/app.py db upgrade
```

### 3. Executar o seed no Neon

```bash
python scripts/seed.py
```

A saída deve mostrar o host do Neon e os dados inseridos.

### 4. Restaurar o `.env` para banco local

```bash
# Abra o .env e volte para:
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/legiskids
```

---

## O script `scripts/seed.py`

O seed popula o banco com dados fixos necessários para a aplicação funcionar — atualmente os 17 partidos registrados na API da Câmara.

**Características:**
- Idempotente: verifica existência pela PK antes de inserir (nunca duplica)
- Atualiza campos se o registro existe mas os dados mudaram (sigla ou nome)
- Nunca apaga registros existentes
- Extensível: há comentários indicando onde adicionar novas tabelas

Para adicionar dados de uma nova tabela ao seed, abra `scripts/seed.py` e siga o padrão das funções `seed_partidos()` já existentes.

---

## Comandos do dia a dia

| Situação | Comando |
|---|---|
| Subir o banco Docker | `docker compose up -d` |
| Parar o banco Docker | `docker compose down` |
| Aplicar migrations / atualizar banco | `python -m flask --app src/backend/app.py db upgrade` |
| Popular banco com dados iniciais | `python scripts/seed.py` |
| Subir o servidor Flask | `python -m flask --app src/backend/app.py run` |
| Gerar nova migration após mudar model | `flask db migrate -m "descricao"` |
| Reverter última migration | `flask db downgrade` |
| Ver histórico de migrations | `flask db history` |

---

## Problemas comuns

**`RuntimeError: DATABASE_URL não configurada no ambiente.`**
O arquivo `.env` não foi criado ou a variável está ausente. Execute `cp .env.example .env` e verifique o conteúdo.

**`connection refused` na porta 5432**
O container Docker não está rodando. Execute `docker compose up -d` e aguarde o status `healthy`.

**`No module named 'flask_migrate'`**
O venv não está ativado ou as dependências não foram instaladas.
Execute `source .venv/bin/activate` e depois `pip install -r requirements.txt`.

**`Error: No such command 'db'`**
O Flask não encontrou o app. Verifique se `FLASK_APP=src/backend/app.py` está no `.env` e use
`python -m flask --app src/backend/app.py db upgrade` em vez de só `flask db upgrade`.

**`SSL connection required` ao conectar no Neon**
A connection string do Neon precisa de `?sslmode=require`. Verifique o `DATABASE_URL` no `.env`.

**Banco desatualizado após puxar mudanças do git**
Execute `python -m flask --app src/backend/app.py db upgrade`. O Alembic aplica só as migrations novas.

**Seed rodou mas não aparece nada no banco**
Verifique se o `DATABASE_URL` no `.env` aponta para o banco correto (local ou Neon) antes de rodar.
