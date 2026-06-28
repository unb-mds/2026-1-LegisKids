# Proposal — auditoria-backend-pre-develop

## Objetivo

Corrigir bugs reais e lacunas de persistência identificados no backend antes do merge para `develop`. Não são refactors estéticos — cada item abaixo representa comportamento incorreto ou dado perdido silenciosamente.

---

## Contexto

O backend cobre o ciclo completo: leitura paginada da API da Câmara → filtro por palavras-chave → classificação em lote pelo Gemini (gemini-2.5-flash, grátis) → persistência no Neon (PostgreSQL) via upsert idempotente → scheduler cron diário ao meio-dia. Testes: 39/39 passando.

A auditoria revelou 4 problemas reais, nenhum deles cosmético:

---

## Problemas encontrados

### Bug 1 — `cota_gemini_esgotada` é código morto

`_classificar_lote()` captura **todas** as exceções do Gemini internamente e retorna `(dto, None)` — nunca lança. O bloco `except Exception` em `run_sync()` que seta `cota_gemini_esgotada = True` nunca é atingido. Consequências:
- Quando o Gemini falha, o loop continua chamando `_classificar_lote()` página após página desnecessariamente (cada vez voltando `None` para todos os itens).
- `STATUS_CONCLUIDO_PARC` nunca é registrado, mesmo quando todas as proposições ficam pendentes por falha do Gemini.

**Correção:** após cada lote processado, verificar se todos os resultados são `None` (Gemini falhou); se sim, setar `cota_gemini_esgotada = True` para evitar chamadas subsequentes neste run.

---

### Bug 2 — `total_descartados` nunca é persistido

`run_sync()` contabiliza `total_descartados` (proposições classificadas como irrelevantes e descartadas), mas:
- A coluna **não existe** em `sync_executions`.
- A chamada a `repo.atualizar_sync_execution(...)` não inclui o campo.
O contador morre no escopo da função a cada execução.

**Correção:** adicionar coluna `total_descartados` ao modelo `SyncExecution`, criar migration, e incluir o campo no `atualizar_sync_execution`.

---

### Bug 3 — Falta índice em `proposicoes.classificacao_status`

`get_proposicoes_pendentes()` faz `SELECT ... WHERE classificacao_status = 'pendente_classificacao'` a cada execução de `run_sync`. Sem índice, a query faz full table scan. À medida que o banco cresce, isso degrada o início de cada sync.

**Correção:** migration com `CREATE INDEX` na coluna `classificacao_status`.

---

### Limpeza — `testa_tabelas.py` no diretório de migrations

`src/backend/migrations/testa_tabelas.py` é um script de teste/debug que foi deixado no diretório de migrations do backend (não confundir com o diretório raiz `migrations/` do Alembic). Não é executado automaticamente, mas polui o módulo e pode causar confusão.

**Correção:** remover o arquivo.

---

## O que está correto e não precisa mudar

| Componente | Status |
|---|---|
| Scheduler cron 12:00 (APScheduler) | ✅ correto |
| Paginação DESC com early-stop | ✅ correto |
| Filtro por palavras-chave (client-side) | ✅ correto |
| `dataApresentacaoInicio=2022-01-01` | ✅ correto |
| Gemini batch (10/chamada, múltiplas categorias) | ✅ correto |
| Retry 429 (60s) e 503 (30s), 3 tentativas | ✅ correto |
| Upsert idempotente via `ON CONFLICT` | ✅ correto |
| Skip de IDs conhecidos + early-stop | ✅ correto |
| `_retentar_pendentes` no início de cada run | ✅ correto |
| 8 categorias fixas + seed idempotente | ✅ correto |
| Tabelas e relacionamentos N:N | ✅ correto |
| Migrations em cadeia (3 aplicadas) | ✅ correto |
| Testes 39/39 | ✅ passando |

---

## Restrições

- Não alterar a lógica de classificação ou o prompt do Gemini.
- Não mudar o schema de nenhuma tabela existente além de adicionar a coluna `total_descartados` e o índice.
- Não introduzir novas dependências.
- Os testes existentes devem continuar passando após as mudanças.
