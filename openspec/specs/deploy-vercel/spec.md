# deploy-vercel Specification

## Purpose
TBD - created by archiving change fix-backend-deploy-vercel. Update Purpose after archive.
## Requirements
### Requirement: CORS configurável por ambiente
A aplicação Flask SHALL determinar as origens permitidas por CORS a partir da variável de ambiente `FRONTEND_URL`, incluindo os localhosts de desenvolvimento (`http://localhost:5173`, `http://127.0.0.1:5173`) apenas quando `FLASK_ENV` não for `production`.

#### Scenario: Frontend de produção chama a API
- **WHEN** o frontend deployado em produção (origem definida em `FRONTEND_URL`) faz uma requisição à API
- **THEN** a resposta inclui os headers CORS liberando essa origem

#### Scenario: Frontend local chama a API em modo dev
- **WHEN** `FLASK_ENV` não é `production` e o frontend local (`http://localhost:5173`) faz uma requisição à API
- **THEN** a resposta inclui os headers CORS liberando `localhost:5173`, independentemente do valor de `FRONTEND_URL`

### Requirement: Debug mode desligado fora de desenvolvimento
O servidor Flask SHALL rodar com `debug=False` a menos que `FLASK_ENV` seja explicitamente `development`.

#### Scenario: App executado sem FLASK_ENV=development
- **WHEN** a aplicação é iniciada via `python src/backend/app.py` sem `FLASK_ENV=development` setado
- **THEN** o servidor sobe com o modo debug do Werkzeug desligado

### Requirement: SECRET_KEY obrigatório em produção
A aplicação SHALL falhar na inicialização com erro claro se `FLASK_ENV=production` e a variável de ambiente `SECRET_KEY` não estiver definida. Fora de produção, SHALL usar um valor de desenvolvimento como fallback.

#### Scenario: Produção sem SECRET_KEY configurada
- **WHEN** a aplicação inicia com `FLASK_ENV=production` e sem `SECRET_KEY` no ambiente
- **THEN** a inicialização falha com uma exceção indicando que `SECRET_KEY` é obrigatória

#### Scenario: Desenvolvimento sem SECRET_KEY configurada
- **WHEN** a aplicação inicia com `FLASK_ENV` diferente de `production` e sem `SECRET_KEY` no ambiente
- **THEN** a aplicação inicia normalmente usando um valor padrão de desenvolvimento

### Requirement: Scheduler in-process opcional e não usado no Vercel
O `BackgroundScheduler` SHALL só ser iniciado quando a variável de ambiente `ENABLE_SCHEDULER` estiver definida como `true`. O deploy no Vercel SHALL manter essa variável ausente ou falsa, dependendo do sync via Vercel Cron.

#### Scenario: Deploy serverless sem ENABLE_SCHEDULER
- **WHEN** a aplicação inicia numa função serverless sem `ENABLE_SCHEDULER=true`
- **THEN** nenhum `BackgroundScheduler` é iniciado

#### Scenario: Deploy tradicional com ENABLE_SCHEDULER=true
- **WHEN** a aplicação inicia num processo de longa duração com `ENABLE_SCHEDULER=true`
- **THEN** o `BackgroundScheduler` é iniciado normalmente, preservando o comportamento atual de sync diário

### Requirement: Endpoint de sync sob demanda protegido por secret
A aplicação SHALL expor um endpoint HTTP para disparar `CamaraService().run_sync()` sob demanda, exigindo um secret (`CRON_SECRET`) enviado pelo chamador; requisições sem o secret correto SHALL ser rejeitadas.

#### Scenario: Vercel Cron dispara o sync com secret correto
- **WHEN** uma requisição ao endpoint de sync chega com o secret correto configurado em `CRON_SECRET`
- **THEN** `CamaraService().run_sync()` é executado e um resumo da execução é retornado

#### Scenario: Requisição sem secret ou com secret incorreto
- **WHEN** uma requisição ao endpoint de sync chega sem o header de autorização ou com um secret que não bate com `CRON_SECRET`
- **THEN** a requisição é rejeitada com status 401 e `run_sync()` não é executado

### Requirement: Artefatos de build e cron do Vercel presentes
O repositório SHALL conter `api/index.py`, expondo o app Flask no formato esperado pelo runtime Python do Vercel, e `vercel.json`, configurando o build do backend, o build estático do frontend e um cron job diário apontando para o endpoint de sync.

#### Scenario: Vercel builda o projeto
- **WHEN** o Vercel processa o repositório usando `vercel.json`
- **THEN** encontra a definição de build para `api/index.py` (backend Python) e para o diretório do frontend (build estático), e a definição de `crons` apontando para o endpoint de sync

