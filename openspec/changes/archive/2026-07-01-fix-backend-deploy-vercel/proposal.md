## Why

O backend Flask atual não roda corretamente em produção no Vercel: CORS está hardcoded para `localhost`, não existe entrypoint serverless (`api/index.py` + `vercel.json`), não há servidor WSGI de produção nas dependências, o `BackgroundScheduler` do APScheduler é iniciado in-process (incompatível com funções serverless efêmeras e duplicado em ambientes multi-worker tradicionais), o modo debug do Flask fica ligado por padrão, e o `SECRET_KEY` cai silenciosamente para um valor de desenvolvimento se a env var não estiver setada. Sem esses ajustes, o deploy no Vercel simplesmente não funciona ou expõe riscos de segurança.

## What Changes

- CORS passa a ler as origens permitidas de uma env var (`FRONTEND_URL`), com fallback aos localhosts de dev apenas fora de produção.
- `debug` do Flask deixa de ser `True` fixo; passa a ser controlado por `FLASK_ENV`/`FLASK_DEBUG`, desligado por padrão.
- `SECRET_KEY` passa a exigir env var explícita em produção (falha alto como `DATABASE_URL`), com fallback de dev apenas fora de produção.
- O `BackgroundScheduler` in-process só inicia quando explicitamente habilitado (`ENABLE_SCHEDULER=true`), pensado para deploys tradicionais (Render/Railway/VM) — nunca no Vercel.
- **Novo endpoint** `/api/cron/sync` protegido por secret (`CRON_SECRET`), que dispara `CamaraService().run_sync()` sob demanda — alvo do Vercel Cron Jobs.
- `gunicorn` adicionado a `requirements.txt` como servidor WSGI de produção para deploys tradicionais (fora do Vercel, que usa seu próprio runtime Python serverless e não invoca gunicorn).
- Novo `api/index.py`, expondo a instância `app` do Flask no formato que o runtime Python do Vercel espera.
- Novo `vercel.json` configurando build do backend Python, build/servimento do frontend estático (`src/frontend`) e um `crons` entry chamando `/api/cron/sync` diariamente.
- `.env.example` atualizado com as novas variáveis: `FRONTEND_URL`, `ENABLE_SCHEDULER`, `CRON_SECRET`.

## Capabilities

### New Capabilities
- `deploy-vercel`: cobre os requisitos para o backend Flask + frontend Vue funcionarem corretamente quando deployados no Vercel — CORS configurável, ausência de debug mode em produção, SECRET_KEY obrigatório em produção, sync da Câmara via Vercel Cron em vez de scheduler in-process, e os artefatos de configuração (`api/index.py`, `vercel.json`) necessários para o build.

### Modified Capabilities
(nenhuma — não há spec existente cobrindo configuração de deploy/CORS/scheduler)

## Impact

- Arquivos afetados: `src/backend/app.py`, `src/backend/schedulers/camara_scheduler.py`, `requirements.txt`, `.env.example`
- Arquivos novos: `api/index.py`, `vercel.json`, novo controller/rota para `/api/cron/sync`
- Nenhuma mudança de schema de banco ou de comportamento das rotas `/api/proposicoes`, `/api/estatisticas`, `/api/temas` existentes
- Ambientes de desenvolvimento local continuam funcionando como hoje (CORS libera localhost por padrão fora de produção, scheduler in-process permanece disponível via env var para quem não usa Vercel)
