## 1. Dependências e Configuração

- [x] 1.1 Adicionar `APScheduler` e `tenacity` ao `requirements.txt`
- [x] 1.2 Adicionar variáveis `CAMARA_SYNC_INTERVAL_MINUTES` e `GEMINI_RATE_LIMIT_RPM` ao `.env.example` com valores padrão comentados
- [x] 1.3 Criar estrutura de diretórios: `backend/src/schedulers/`, `backend/src/repositories/` (com `__init__.py`)

## 2. Migration do Banco de Dados

- [x] 2.1 Criar model SQLAlchemy `SyncExecution` em `backend/src/models/` com todas as colunas da spec (`sync_executions`)
- [x] 2.2 Adicionar coluna `classificacao_status` (VARCHAR(30) NOT NULL DEFAULT `'pendente_classificacao'`) ao model `Proposicao`
- [x] 2.3 Gerar migration via `flask db migrate -m "add sync_executions and classificacao_status"`
- [x] 2.4 Revisar migration gerada e confirmar que `sync_executions` é criada e `proposicoes.classificacao_status` é adicionada corretamente
- [ ] 2.5 Aplicar migration no banco local com `flask db upgrade`

## 3. Repository

- [x] 3.1 Criar `backend/src/repositories/camara_repository.py` com método `upsert_proposicao(dto)` usando `INSERT ... ON CONFLICT (id_camara) DO UPDATE SET ...`
- [x] 3.2 Implementar `upsert_proposicoes_lote(dtos)` com transação única por lote
- [x] 3.3 Implementar `criar_sync_execution()` — insere linha com `status='em_andamento'` e retorna o objeto
- [x] 3.4 Implementar `atualizar_sync_execution(id, **campos)` — atualiza `finalizado_em`, `status`, contadores e `mensagem_erro`
- [x] 3.5 Implementar `get_ultimas_execucoes(limite)` — retorna as N mais recentes ordenadas por `iniciado_em DESC`
- [x] 3.6 Garantir que o Repository não contém lógica de negócio — apenas SQL/ORM

## 4. Service

- [x] 4.1 Criar `backend/src/services/camara_service.py` com constante `CATEGORIAS_FIXAS` listando todas as categorias do LegisKids
- [x] 4.2 Implementar `_buscar_proposicoes_api(pagina)` com retry via `tenacity` (3 tentativas, backoff exponencial) para erros 5xx/timeout
- [x] 4.3 Implementar `_validar_proposicao(dado_bruto)` — verifica campos obrigatórios e normaliza datas para ISO 8601; retorna DTO ou `None` se inválido
- [x] 4.4 Implementar `_categorizar_via_gemini(ementa)` — chama Gemini com prompt estruturado contendo `CATEGORIAS_FIXAS`; retorna categoria ou lança exceção com timeout de 5s
- [x] 4.5 Implementar rate limiting em `_categorizar_via_gemini` respeitando `GEMINI_RATE_LIMIT_RPM`
- [x] 4.6 Implementar fallback de IA: capturar timeout/exceção do Gemini e retornar `pendente_classificacao` sem propagar o erro
- [x] 4.7 Implementar `run_sync()`: percorre páginas da API, valida, categoriza e chama Repository para upsert; emite logs de início, progresso e resumo
- [x] 4.8 Implementar abertura e fechamento do registro em `sync_executions` dentro de `run_sync()` (cria no início, atualiza no fim com status e contadores)
- [x] 4.9 Tratar `erro_api` (retry esgotado) e `erro_interno` (exceção inesperada) atualizando `sync_executions` com o status e `mensagem_erro` corretos

## 5. Scheduler

- [x] 5.1 Criar `backend/src/schedulers/camara_scheduler.py` com `BackgroundScheduler` do APScheduler configurado com `CAMARA_SYNC_INTERVAL_MINUTES`
- [x] 5.2 Implementar `start_scheduler(app)` que inicia o scheduler usando o contexto da aplicação Flask
- [x] 5.3 Adicionar `misfire_grace_time` e `coalesce=True` na configuração do job
- [x] 5.4 Registrar o scheduler no `create_app()` do app factory (`backend/src/main.py`)
- [x] 5.5 Implementar comando CLI `flask sync-camara` que chama `CamaraService.run_sync()` e imprime resumo no stdout

## 6. Testes

- [x] 6.1 Testar `upsert_proposicoes_lote` com proposição nova — verificar que `total_inseridos` incrementa
- [x] 6.2 Testar `upsert_proposicoes_lote` com proposição já existente e campos alterados — verificar que `total_atualizados` incrementa
- [x] 6.3 Testar idempotência: reprocessar mesmo lote — verificar que contadores permanecem zerados na segunda execução
- [x] 6.4 Testar `_validar_proposicao` com campo obrigatório ausente — verificar que retorna `None` e emite WARNING
- [x] 6.5 Testar fallback de IA: mockar Gemini para lançar timeout — verificar que `classificacao_status` fica `pendente_classificacao` e pipeline continua
- [x] 6.6 Testar fallback de IA: mockar Gemini para retornar categoria inválida — verificar `pendente_classificacao`
- [x] 6.7 Testar `run_sync()` com API da Câmara retornando erro 504 — verificar retry e status `erro_api` em `sync_executions`
- [x] 6.8 Testar `run_sync()` completo com sucesso — verificar `sync_executions` com `status='concluido'` e contadores corretos

## 7. Documentação do Schema

- [x] 7.1 Atualizar `docs/db/schema.md` com a tabela `sync_executions` (colunas, constraints, valores de status)
- [x] 7.2 Atualizar `docs/db/schema.md` com a coluna `classificacao_status` em `proposicoes`
- [x] 7.3 Atualizar `docs/db/erd.dbml` para incluir `sync_executions` e `classificacao_status`
- [ ] 7.4 Exportar novo `docs/db/erd.png` via dbdiagram.io
