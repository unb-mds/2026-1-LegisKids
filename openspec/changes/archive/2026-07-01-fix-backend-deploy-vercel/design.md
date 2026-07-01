## Context

O backend hoje (`src/backend/app.py`) foi escrito só para rodar localmente via `flask run`: CORS hardcoded para `localhost:5173`, `app.run(debug=True)` como único entrypoint, `SECRET_KEY` com fallback silencioso, e um `BackgroundScheduler` (APScheduler) iniciado no nível do módulo sempre que `FLASK_ENV != "testing"`. O alvo de deploy escolhido é o Vercel, que roda o backend Python como função serverless via `@vercel/python` (não via gunicorn — o runtime do Vercel importa o objeto WSGI diretamente) e o frontend Vue como build estático. Vercel também oferece Cron Jobs nativos (`vercel.json` → `crons`), que fazem uma requisição HTTP num horário definido — não existe "processo de fundo" persistente em funções serverless.

## Goals / Non-Goals

**Goals:**
- CORS funciona tanto em dev (`localhost`) quanto em produção (domínio real do Vercel), configurável por env var.
- Nenhum modo debug/insecure ligado por padrão fora de desenvolvimento.
- `SECRET_KEY` obrigatório em produção, com a mesma postura de "falha alto" que `DATABASE_URL` já tem.
- Sync diário da Câmara continua funcionando quando deployado no Vercel, via Vercel Cron + endpoint HTTP, sem depender de processo in-process.
- Backend também continua deployável de forma tradicional (Render/Railway/VM/Docker) com `gunicorn`, para quem não usa Vercel — sem duplicar o job do scheduler em múltiplos workers.
- `api/index.py` + `vercel.json` deixam o projeto com um caminho de deploy Vercel funcional de ponta a ponta (backend serverless + frontend estático).

**Non-Goals:**
- Não implementar autenticação/CSRF (fora do escopo da Release 1, já coberto pelo roadmap de R2).
- Não migrar o scheduler para uma fila/worker dedicado (ex: Celery) — o Vercel Cron + endpoint resolve o caso de uso atual.
- Não alterar o comportamento de negócio de `CamaraService.run_sync()`.
- Não configurar domínio customizado, variáveis de ambiente reais no painel do Vercel, ou segredos de produção — isso é operação, feita pelo time fora deste change.

## Decisions

- **CORS via `FRONTEND_URL`**: `app.py` passa a montar a lista de origins a partir de `os.getenv("FRONTEND_URL")` (aceita uma URL, ou várias separadas por vírgula) e só inclui os localhosts de dev quando `FLASK_ENV` não é `production`. Alternativa descartada: `CORS(app, origins="*")` — rejeitada por abrir a API para qualquer origem, sem necessidade real (só o frontend do projeto consome a API).
- **Debug controlado por `FLASK_ENV`**: `app.run(debug=(os.getenv("FLASK_ENV") == "development"))`. Esse bloco só roda quando o arquivo é executado diretamente (`python app.py`); no Vercel e com `gunicorn`, esse `if __name__` nunca é atingido, mas corrigir evita risco caso alguém rode assim em produção por engano.
- **`SECRET_KEY` obrigatório em produção**: se `FLASK_ENV == "production"` e `SECRET_KEY` não estiver setada, `raise RuntimeError` (mesmo padrão do `DATABASE_URL`). Fora de produção, mantém fallback `"dev-secret"` para não quebrar onboarding local.
- **Scheduler atrás de `ENABLE_SCHEDULER`**: `start_scheduler(app)` só é chamado se `os.getenv("ENABLE_SCHEDULER", "false").lower() == "true"`. Documentado no `.env.example` como "não usar no Vercel". Isso resolve tanto o caso serverless (nunca liga) quanto o caso multi-worker tradicional (liga-se explicitamente em só um processo/serviço, ex: um dyno dedicado, se o time optar por isso no futuro).
- **Endpoint `/api/cron/sync` como gatilho do Vercel Cron**: novo endpoint (POST ou GET, decidido na implementação) que exige um header `Authorization: Bearer <CRON_SECRET>` (ou equivalente) batendo com a env var `CRON_SECRET`, e chama `CamaraService().run_sync()` de forma síncrona, retornando o mesmo resumo que o comando CLI `sync-camara` já imprime. Alternativa descartada: expor o endpoint sem autenticação — rejeitada porque disparar o sync é uma operação custosa (chamadas à API da Câmara + Gemini) que não deve ficar pública.
- **`gunicorn` em `requirements.txt`**: adicionado para deploys tradicionais fora do Vercel (Render/Railway/Docker/VM). No Vercel ele fica instalado mas não é invocado — o runtime `@vercel/python` importa `api/index.py` diretamente. Alternativa descartada: não adicionar gunicorn e documentar só o Vercel — rejeitada porque o backend deve continuar deployável fora do Vercel também (não é um "vercel-only project").
- **`api/index.py`**: módulo fino que importa `app` de `src.backend.app` e o expõe como `app` (convenção que o builder Python do Vercel espera para descobrir o objeto WSGI).
- **`vercel.json`**: define dois builds — `@vercel/python` para `api/index.py` (backend) e `@vercel/static-build` para `src/frontend` (build Vite, saída em `src/frontend/dist`) — e um `crons` apontando para `/api/cron/sync` no horário equivalente ao `CAMARA_SYNC_HOUR`/`CAMARA_SYNC_MINUTE` atuais (padrão 12:00 UTC, documentado como ponto de atenção de fuso horário).

## Risks / Trade-offs

- [Risco] `CRON_SECRET` vazar ou não ser configurado → Mitigação: endpoint retorna 401/403 sem o header correto; secret gerado como valor aleatório longo, nunca comitado (`.env.example` só documenta a variável, sem valor).
- [Risco] Vercel Cron roda em UTC, e `CAMARA_SYNC_HOUR`/`MINUTE` foram pensados para fuso do servidor local → Mitigação: documentar explicitamente no `.env.example` e no `vercel.json` que o horário do cron é UTC, e ajustar o valor manualmente na config do Vercel se for necessário horário local.
- [Risco] Alguém habilita `ENABLE_SCHEDULER=true` no Vercel por engano → Mitigação: como funções serverless não mantêm processo em background entre invocações, isso não causaria duplicação (o processo simplesmente não persiste), mas também não teria efeito útil — documentar claramente que essa env var é só para deploys não-serverless.
- [Risco] `vercel.json` com dois builds (`@vercel/python` + `@vercel/static-build`) pode exigir ajustes finos de rotas (`routes`/`rewrites`) não previstos aqui → Mitigação: tasks incluem validação manual do build local (`vercel build` ou `vercel dev`, se disponível) antes de considerar o item concluído; caso o ambiente não tenha a CLI do Vercel, isso fica registrado como validação pendente, igual ao que já ocorreu na migration anterior.

## Migration Plan

1. Ajustar `app.py` (CORS, debug, SECRET_KEY, guard do scheduler).
2. Criar endpoint `/api/cron/sync` protegido.
3. Adicionar `gunicorn` ao `requirements.txt`.
4. Criar `api/index.py` e `vercel.json`.
5. Atualizar `.env.example` com `FRONTEND_URL`, `ENABLE_SCHEDULER`, `CRON_SECRET`.
6. Validar localmente: app ainda sobe com `flask run` como antes (comportamento de dev inalterado), testes passam.
7. Validação de deploy real no Vercel fica fora deste change (requer conta/projeto configurado) — registrado como pendência.

Rollback: reverter os arquivos alterados/criados via git; nenhuma migração de dado ou estado externo envolvida.

## Open Questions

Nenhuma — decisões acima cobrem as ambiguidades identificadas; validação de deploy real no Vercel fica como pendência operacional, não bloqueia o merge do código.
