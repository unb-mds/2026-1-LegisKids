## Why

A change anterior (`sync-proposicoes-camara-ia`) construiu o pipeline de coleta: scheduler, retry, validação, upsert e tracking de execução. Porém, a integração com o Gemini está incompleta em dois aspectos críticos:

1. **Sem filtro de relevância**: o prompt atual pede ao Gemini que classifique qualquer proposição em uma das categorias fixas — mas não verifica se a proposição tem relação com proteção de crianças na internet. Proposições irrelevantes seriam persistidas sob a categoria "outros", poluindo o banco.

2. **Categoria perdida após classificação**: o nome da categoria retornado pelo Gemini é logado mas nunca persiste na junction table `proposicao_categoria`. O banco fica com `classificacao_status = 'classificado'` mas zero vínculos reais — inviabilizando filtros e gráficos por categoria no dashboard.

Além disso, a tabela `categorias` existe no schema mas nunca é populada, e proposições marcadas como `pendente_classificacao` não são retentadas.

## What Changes

- **`camara_service.py`**: redesign do prompt Gemini para uma única chamada que decide relevância e categoria simultaneamente. Proposições irrelevantes são descartadas — não persistidas. Fluxo de retry de pendentes a cada execução do scheduler.
- **`camara_repository.py`**: nova função `seed_categorias()` (idempotente) e `vincular_categoria(proposicao_id, categoria_nome)` para persistir o vínculo na junction table.
- **`app.py`**: chamar `seed_categorias()` no startup da aplicação.
- **Neon**: confirmar sslmode=require no `DATABASE_URL` e garantir que ambas as migrations estão aplicadas.

## Capabilities

### New Capabilities

- `gemini-relevance-filter`: o Gemini decide em uma chamada se a proposição é relevante para proteção infantil digital e, se sim, em qual categoria. Proposições irrelevantes são descartadas antes da persistência.
- `categoria-seed`: categorias fixas inseridas automaticamente no startup (idempotente), com nome, descrição, cor hex e ícone.
- `proposicao-categoria-link`: após upsert de proposição classificada, vínculo é persistido na junction table `proposicao_categoria`.
- `pending-retry`: proposições com `classificacao_status = 'pendente_classificacao'` são re-tentadas em cada run do scheduler.

### Modified Capabilities

- `camara-ai-categorization`: prompt redesenhado; agora filtra relevância além de classificar.
- `camara-sync-job`: passa a descartar proposições irrelevantes em vez de salvá-las como "outros".

## Impact

- **Backend**: mudanças em `camara_service.py`, `camara_repository.py` e `app.py`.
- **Banco de dados**: nenhuma mudança de schema — apenas seed de dados na tabela `categorias` e inserções em `proposicao_categoria`.
- **Sem impacto**: scheduler, rotas Flask, frontend, autenticação.
