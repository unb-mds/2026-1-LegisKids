## 1. CORS, debug e SECRET_KEY (app.py)

- [x] 1.1 Em `src/backend/app.py`, montar a lista de origins do `CORS()` a partir de `FRONTEND_URL` (aceitando múltiplas origens separadas por vírgula), incluindo os localhosts de dev somente quando `FLASK_ENV != "production"`
- [x] 1.2 Trocar `app.run(debug=True)` por `app.run(debug=(os.getenv("FLASK_ENV") == "development"))`
- [x] 1.3 Fazer `SECRET_KEY` falhar alto (`raise RuntimeError`) quando `FLASK_ENV == "production"` e a env var não estiver setada; manter fallback `"dev-secret"` fora de produção

## 2. Scheduler condicional (app.py, camara_scheduler.py)

- [x] 2.1 Em `app.py`, só chamar `start_scheduler(app)` quando `os.getenv("ENABLE_SCHEDULER", "false").lower() == "true"` (além da condição já existente de não rodar em `FLASK_ENV=testing`)
- [x] 2.2 Não alterar a lógica interna de `camara_scheduler.py` — só o ponto de chamada em `app.py`

## 3. Endpoint de sync sob demanda

- [x] 3.1 Criar rota `/api/cron/sync` (mesmo blueprint `proposicoes_bp` ou um novo blueprint dedicado a operações internas) que exige header de autorização comparado com `CRON_SECRET`
- [x] 3.2 Sem o secret correto, retornar 401 sem executar `CamaraService().run_sync()`
- [x] 3.3 Com o secret correto, chamar `CamaraService().run_sync()` e retornar o resumo (status, processados, inseridos, atualizados, erros) como JSON

## 4. Artefatos de deploy Vercel

- [x] 4.1 Adicionar `gunicorn` ao `requirements.txt` (para deploys tradicionais fora do Vercel)
- [x] 4.2 Criar `api/index.py` importando e expondo `app` de `src.backend.app`
- [x] 4.3 Criar `vercel.json` com build do backend Python (`api/index.py`), build estático do frontend (`src/frontend`, saída `dist`) e `crons` apontando para `/api/cron/sync` (documentando que o horário é UTC)

## 5. Configuração e documentação

- [x] 5.1 Atualizar `.env.example` com `FRONTEND_URL`, `ENABLE_SCHEDULER` e `CRON_SECRET`, com comentários explicando cada uma (incluindo o aviso de não usar `ENABLE_SCHEDULER` no Vercel)

## 6. Validação

- [x] 6.1 Rodar `pip install -r requirements.txt` localmente para alinhar o `.venv` com as dependências atuais (resolve o drift do `google-genai` visto nos testes)
- [x] 6.2 Rodar a suíte de testes (`pytest`) e confirmar que os testes do Gemini passam após o `pip install` — 42 passed (antes: 36 passed / 6 failed)
- [x] 6.3 Validado via Flask test client (equivalente a `flask run` local): com `FLASK_ENV` fora de produção, origem `http://localhost:5173` recebe `Access-Control-Allow-Origin`; com `FLASK_ENV=production`, `localhost` deixa de ser permitido e a origem de `FRONTEND_URL` passa a ser permitida
- [x] 6.4 Testado `/api/cron/sync` sem header (401) e com secret incorreto (401) via test client. **Não executado**: chamada com secret correto — dispararia `CamaraService().run_sync()` de verdade (API da Câmara + Gemini + escrita no Neon de produção), então o caminho feliz completo não foi acionado nesta sessão para evitar efeito colateral em produção; recomenda-se validar manualmente com `CRON_SECRET` de um ambiente de teste
- [ ] 6.5 **PENDENTE — validação manual**: build e deploy reais no Vercel (`vercel build`/`vercel dev` ou deploy de preview) não foram executados nesta sessão por falta de conta/CLI do Vercel configurada no ambiente — registrar como pendência para quem tiver acesso ao projeto Vercel
