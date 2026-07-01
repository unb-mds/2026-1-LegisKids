## Why

O schema do banco modela `categorias` como relação muitos-para-muitos com `proposicoes` (via `proposicao_categorias`), mas o serializer do backend (`_serializar_proposicao`) hoje só expõe a **primeira** categoria como campo singular `subtema`, descartando silenciosamente qualquer subtema adicional atribuído pela classificação por IA.

## What Changes

- Em `_serializar_proposicao` (`src/backend/controllers/proposicoes_controller.py`), substituir o campo `subtema` (string, primeira categoria ou null) por `subtemas` (array com o nome de todas as categorias da proposição). **BREAKING**
- Atualizar as specs `api-proposicoes-list` e `api-proposicoes-detail` para refletir o novo contrato de campo.
- Escopo estritamente restrito a `src/backend/` — nenhum arquivo de frontend é tocado nesta mudança.

## Capabilities

### New Capabilities
(nenhuma)

### Modified Capabilities
- `api-proposicoes-list`: campo `subtema` (string, primeira categoria) no item da listagem é substituído por `subtemas` (array de nomes de categorias)
- `api-proposicoes-detail`: campo `subtema` (string, primeira categoria) no objeto de detalhe da proposição é substituído por `subtemas` (array de nomes de categorias)

## Impact

- **Código afetado:** `src/backend/controllers/proposicoes_controller.py` (função `_serializar_proposicao`), usada pelas rotas `GET /api/proposicoes` e `GET /api/proposicoes/<id>`.
- **Consumidores:** o frontend (`fix/frontend`) consome `subtema` como string em `ProposicaoCard`/`DetalheView` e precisa migrar para o array `subtemas`. Os PRs `fix/backend` e `fix/frontend` **precisam ser mergeados juntos** — o campo antigo deixa de existir, não há período de compatibilidade dupla.
- **Sem impacto em:** modelos, repositório, migrations ou banco de dados — a relação `categorias` já é lida em `prop.to_dict()`; a mudança é apenas na serialização da resposta HTTP.
