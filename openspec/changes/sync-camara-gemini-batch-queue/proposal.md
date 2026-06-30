## Why

O fluxo atual de `run_sync()` chama o Gemini **dentro do loop de páginas da API da Câmara**: a cada página, as proposições que passam pelo filtro de palavras-chave (geralmente 2 a 10 de 100) são imediatamente enviadas ao Gemini em lotes de `GEMINI_BATCH_SIZE`. Isso resulta em lotes menores do que o configurado na maioria dos casos — uma página que produz 3 proposições relevantes gera uma chamada ao Gemini com apenas 3 ementas, desperdiçando a capacidade do lote.

O problema é relevante porque o Gemini free tier tem limite de **20 requisições/dia** (`GenerateRequestsPerDayPerProjectPerModel-FreeTier`). Cada chamada subutilizada é cota perdida. Uma run que processa 10 páginas com 3 proposições relevantes cada faz 10 chamadas para classificar 30 proposições — o mesmo resultado poderia ser obtido com 3 chamadas de 10.

## What Changes

- **`camara_service.py` — `run_sync()`**: substituir o modelo "classifica por página" por uma fila acumulada. As proposições válidas e novas são coletadas de todas as páginas em uma lista. Quando essa lista atinge `GEMINI_BATCH_SIZE`, o lote completo é enviado ao Gemini e persistido. O restante que não completou um lote é processado ao final da paginação.

Nenhuma outra camada é afetada: repository, models, scheduler, frontend e banco de dados permanecem intactos.

## Capabilities

### Modified Capabilities

- `camara-sync-job`: o loop de paginação agora acumula DTOs em uma fila antes de enviar ao Gemini, em vez de classificar por página. O comportamento externo (proposições classificadas no banco, `SyncExecution` registrada) é idêntico; apenas a cadência das chamadas ao Gemini muda.

### Non-goals

- Não altera a lógica de retry de pendentes (`_retentar_pendentes`).
- Não altera o prompt do Gemini nem o parsing da resposta.
- Não introduz persistência assíncrona nem filas externas (Redis, Celery etc.).
- Não altera a lógica de early-stop por IDs já conhecidos.

## Impact

- **Backend**: mudança cirúrgica em `camara_service.py`, apenas no método `run_sync()`.
- **Banco de dados**: sem impacto — o comportamento do upsert e do vínculo de categorias é o mesmo.
- **Gemini**: redução do número de chamadas à API proporcional ao grau de esparsidade das proposições relevantes por página.
