## Why

O LegisKids ainda não possui um mecanismo automatizado para coletar e atualizar proposições da Câmara dos Deputados — atualmente a ingestão é manual ou inexistente. É necessário um pipeline robusto e idempotente que mantenha o banco de dados sincronizado com a API da Câmara, com categorização automática via Gemini, para viabilizar todas as funcionalidades de busca, análise e alertas.

## What Changes

- Novo módulo `schedulers/camara_scheduler.py`: orquestra execuções periódicas (intervalo configurável) e disparo manual via CLI, sem acesso direto a banco ou regras de negócio.
- Novo módulo `services/camara_service.py`: consome a API da Câmara (`dadosabertos.camara.leg.br/api/v2`) com retry automático (mínimo 3 tentativas), valida e normaliza cada proposição, identifica registros novos vs. alterados, e categoriza via Gemini com rate limit configurável.
- Novo módulo `repositories/camara_repository.py`: realiza upsert transacional de proposições e categorias, garantindo idempotência e sem duplicidade.
- Nova entidade `sync_execution`: registra cada execução do job (início, fim, status, totais processados/inseridos/atualizados, mensagem de erro).
- Fallback de IA: proposições que excedem o timeout de categorização ou falham no Gemini são salvas com status `pendente_classificacao`, sem bloquear o pipeline.
- Logs estruturados em cada fase: início, progresso, erros individuais, resumo final.

## Capabilities

### New Capabilities

- `camara-sync-job`: job de sincronização agendado e manual — consome a API da Câmara, normaliza dados e persiste proposições novas/alteradas via repository.
- `camara-ai-categorization`: categorização automática de proposições via Gemini com categorias fixas, rate limit, timeout e fallback para `pendente_classificacao`.
- `sync-execution-tracking`: registro de metadados de cada execução do job (início, fim, status, contadores, erro) na tabela `sync_executions`.

### Modified Capabilities

- `schema-banco-de-dados`: adição das tabelas `sync_executions` e ajustes em `proposicoes`/`proposicao_categorias` para suportar o campo `pendente_classificacao` e rastreamento de origem da sincronização.

## Impact

- **Backend:** novos módulos em `backend/src/schedulers/`, `backend/src/services/`, `backend/src/repositories/`.
- **Banco de dados:** nova tabela `sync_executions`; coluna adicional em `proposicoes` para status de classificação IA.
- **Variáveis de ambiente:** `CAMARA_SYNC_INTERVAL_MINUTES`, `GEMINI_RATE_LIMIT_RPM` (já existe `GOOGLE_API_KEY`).
- **Dependências:** `APScheduler` (scheduler), `tenacity` (retry) — a adicionar em `requirements.txt`.
- **Sem impacto:** rotas existentes do Flask, frontend, autenticação.
