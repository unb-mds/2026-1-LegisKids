## Why

O frontend Vue já consome 4 endpoints REST (`/api/proposicoes`, `/api/proposicoes/<id>`, `/api/estatisticas`, `/api/temas`) que simplesmente não existem no Flask — toda requisição retorna 404. Isso bloqueia a Release 1, com entrega prevista para quarta-feira (2026-07-01).

## What Changes

- Novo arquivo `src/backend/controllers/proposicoes_controller.py` com um Blueprint Flask registrando as 4 rotas.
- Novos métodos no `src/backend/repository/camara_repository.py` para queries que o controller precisa mas o repositório ainda não tem: listagem paginada com filtros, detalhe por ID, contagens por categoria e por mês, e último sync bem-sucedido.
- Registro do blueprint em `src/backend/app.py` (uma linha).

## Capabilities

### New Capabilities

- `api-proposicoes-list`: `GET /api/proposicoes` — listagem paginada com filtros (q, parlamentar, partido, data_inicio, data_fim, subtema, pagina, por_pagina); retorna `{items, total, pagina, total_paginas}`.
- `api-proposicoes-detail`: `GET /api/proposicoes/<int:id>` — detalhe completo com categorias e tramitações; retorna `{proposicao, tramitacoes}` ou 404.
- `api-estatisticas`: `GET /api/estatisticas` — métricas para o dashboard; retorna `{resumo, ultima_atualizacao, por_subtema, por_status, temporal}`.
- `api-temas`: `GET /api/temas` — lista de categorias com total de proposições vinculadas; retorna array de objetos.

### Modified Capabilities

*(nenhuma — nenhum endpoint existente é alterado)*

## Impact

- **Backend:** novo controller + métodos novos no repositório; `camara_service.py` e `camara_scheduler.py` não são tocados.
- **Frontend:** zero mudanças — os services já apontam para as URLs corretas.
- **Banco:** queries apenas de leitura (SELECT); sem migrações.
- **CORS:** `app.py` já permite `localhost:5173`; nenhuma mudança necessária.
- **Deploy (Vercel):** o frontend é estático; o backend Flask precisará de configuração de variáveis de ambiente (`DATABASE_URL`) no ambiente de produção.
