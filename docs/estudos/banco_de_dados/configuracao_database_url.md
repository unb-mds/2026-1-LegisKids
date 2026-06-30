# Configuração da `DATABASE_URL`

O LegisKids utiliza o PostgreSQL gerenciado no Neon. O backend Flask lê a
conexão pela variável de ambiente `DATABASE_URL`.

## Pré-requisitos

- Python 3.10 ou superior
- Acesso à connection string do projeto no Neon
- Dependências de `requirements.txt` instaladas em um ambiente virtual

## Configuração

Na raiz do repositório, crie seu arquivo local:

```bash
cp .env.example .env
```

No Windows, use:

```powershell
copy .env.example .env
```

Solicite a connection string ao responsável pelo banco ou copie-a pelo botão
**Connect** no painel do Neon. Adicione o valor completo ao `.env`:

```env
DATABASE_URL=postgresql://<usuario>:<senha>@<host>.neon.tech/<banco>?sslmode=require&channel_binding=require
```

O arquivo `.env` está ignorado pelo Git. A connection string contém
credenciais e nunca deve ser publicada no repositório, em issues ou em canais
abertos.

## Execução local segura

Mantenha esta configuração durante o desenvolvimento local:

```env
FLASK_ENV=testing
```

O backend usa esse valor para não iniciar o scheduler diário de sincronização
em cada computador conectado ao banco compartilhado.

Inicie a API:

```bash
python -m flask --app src/backend/app.py run --debug
```

Verifique a conexão em:

```text
http://127.0.0.1:5000/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "database": "conectado"
}
```

## Migrations e seed

Não execute migrations, seed ou sincronizações manuais no banco compartilhado
sem autorização do responsável. Esses comandos podem alterar schema e dados
usados por toda a equipe.

Quando uma alteração for autorizada:

```bash
python -m flask --app src/backend/app.py db upgrade
python scripts/seed.py
```

Revise sempre se a `DATABASE_URL` aponta para o ambiente correto antes de
executá-los.

## Solução de problemas

### `DATABASE_URL não configurada`

Confira se o `.env` existe na raiz e se `DATABASE_URL` recebeu a connection
string completa.

### Erro de autenticação

Copie novamente a connection string pelo painel do Neon. Não tente corrigir
usuário, senha ou host manualmente.

### Erro de conexão segura

Use a connection string completa fornecida pelo Neon, incluindo os parâmetros
de segurança:

```text
?sslmode=require&channel_binding=require
```

### `/health` funciona, mas os endpoints não retornam dados

O healthcheck confirma a conexão, mas não garante que o schema e os dados
estejam disponíveis. Informe o responsável pelo banco antes de aplicar
migrations ou seed.
