## Why

Toda execução de `flask sync-camara` recomeça da página 1 da API da Câmara e re-processa proposições que já estão no banco — tanto as já classificadas quanto as pendentes. Isso desperdiça as 20 requisições diárias ao Gemini reclassificando dados que já existem no Neon.

O comportamento atual em um segundo run:

1. `_retentar_pendentes()` classifica corretamente as pendentes do DB ✓
2. O loop principal re-lê as mesmas páginas da API e manda as proposições já salvas para o Gemini de novo ✗

Com um limite de 20 req/dia × lote de 50 = 1.000 classificações/dia, gastar esse budget em proposições já processadas inviabiliza o escaneamento histórico.

## What Changes

Dois filtros complementares em `run_sync`:

**Filtro 1 — Early-stop de paginação:** após buscar cada página da API, verificar se todos os IDs brutos (antes do filtro de palavras-chave) já existem no banco. Se sim, interromper a paginação — proposições mais antigas (IDs menores, por ordenação DESC) também estarão no banco.

**Filtro 2 — Skip de Gemini para IDs já conhecidos:** após validar os DTOs da página, excluir do lote do Gemini qualquer proposição cujo ID já esteja no banco (seja `classificado` ou `pendente_classificacao`). As pendentes são tratadas por `_retentar_pendentes`.

- **`camara_repository.py`**: nova função `get_ids_existentes(ids: list[int]) -> set[int]` — consulta eficiente que retorna o subconjunto de IDs já presentes no banco.
- **`camara_service.py`**: dois pontos de uso de `get_ids_existentes` em `run_sync`.

## Capabilities

### New Capabilities

- `ids-existentes-lookup`: consulta O(1) por lote — verifica quais IDs de uma lista já existem no banco sem carregar os objetos completos.

### Modified Capabilities

- `camara-sync-job`: para paginação quando encontra página inteiramente conhecida; pula Gemini para proposições já no banco.

## Impact

- **Backend**: edições em `camara_repository.py` e `camara_service.py`.
- **Testes**: adicionar casos para o early-stop e o skip de IDs conhecidos.
- **Sem impacto**: scheduler, rotas Flask, frontend, modelos, migrações.
