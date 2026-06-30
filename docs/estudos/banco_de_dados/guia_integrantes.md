# Guia de Banco de Dados para Integrantes

Este guia apresenta o fluxo seguro para acessar o banco compartilhado do
LegisKids no Neon durante o desenvolvimento.

## Visão geral

O backend utiliza:

- PostgreSQL hospedado no Neon;
- SQLAlchemy para acesso aos dados;
- Flask-Migrate e Alembic para versionamento do schema;
- `DATABASE_URL` para configuração da conexão.

As credenciais ficam somente no arquivo local `.env`, que não deve ser
versionado.

## Preparar o ambiente

Clone o projeto e entre na pasta:

```bash
git clone https://github.com/unb-mds/2026-1-LegisKids.git
cd 2026-1-LegisKids
```

Crie e ative o ambiente virtual:

=== "Linux/macOS"

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

=== "Windows (PowerShell)"

    ```powershell
    py -m venv .venv
    .venv\Scripts\Activate.ps1
    ```

Instale as dependências:

```bash
python -m pip install -r requirements.txt
```

## Conectar ao Neon

Crie o `.env`:

```bash
cp .env.example .env
```

No Windows, use `copy .env.example .env`.

Solicite a connection string ao responsável pelo banco e preencha:

```env
DATABASE_URL=postgresql://<usuario>:<senha>@<host>.neon.tech/<banco>?sslmode=require&channel_binding=require
FLASK_ENV=testing
```

O modo `testing` é usado localmente para impedir que cada integrante inicie o
scheduler diário no banco compartilhado.

## Iniciar e verificar o backend

```bash
python -m flask --app src/backend/app.py run --debug
```

Acesse `http://127.0.0.1:5000/health`. A resposta esperada é:

```json
{
  "status": "ok",
  "database": "conectado"
}
```

## Regras para o banco compartilhado

- Nunca commite ou compartilhe publicamente a `DATABASE_URL`.
- Não execute migrations, seed ou sincronizações sem autorização.
- Não altere dados manualmente pelo painel do Neon sem combinar com a equipe.
- Confirme o ambiente antes de qualquer operação de escrita.
- Informe imediatamente o responsável caso uma credencial seja exposta.

## Migrations

As migrations ficam em `migrations/versions/` e devem acompanhar mudanças nos
models. A pessoa responsável pela alteração deve revisar o arquivo gerado e
combinar sua aplicação no Neon.

Comandos de manutenção, somente quando autorizados:

```bash
python -m flask --app src/backend/app.py db migrate -m "descricao da mudanca"
python -m flask --app src/backend/app.py db upgrade
```

## Modelos e documentação do schema

Os models SQLAlchemy estão em `src/backend/models.py`. A descrição das tabelas,
relacionamentos e o diagrama estão na
[documentação do schema](../../db/schema.md).

## Comandos do dia a dia

| Situação | Comando |
|---|---|
| Ativar o ambiente | `source .venv/bin/activate` |
| Instalar dependências | `python -m pip install -r requirements.txt` |
| Iniciar a API local | `python -m flask --app src/backend/app.py run --debug` |
| Verificar a conexão | acessar `http://127.0.0.1:5000/health` |

## Problemas comuns

### `DATABASE_URL não configurada`

Crie o `.env` a partir do exemplo e adicione a connection string fornecida
pela equipe.

### Falha de autenticação ou SSL

Copie novamente a connection string completa pelo painel do Neon. Não remova
os parâmetros `sslmode` e `channel_binding`.

### O healthcheck funciona, mas a API não retorna dados

O healthcheck verifica apenas a conexão. Comunique o responsável pelo banco
para conferir schema e dados; não execute migrations ou seed por conta própria.
