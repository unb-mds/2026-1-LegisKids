## 1. Repositório — métodos de leitura

- [x] 1.1 Adicionar `listar_proposicoes_paginado(filtros, pagina, por_pagina)` em `camara_repository.py`: query com filtros opcionais (q ILIKE, partido, data_inicio, data_fim, subtema via JOIN), retorna `(items: list[Proposicao], total: int)`
- [x] 1.2 Adicionar `get_proposicao_detalhe(id)` em `camara_repository.py`: busca proposição por PK com tramitações (eager load ou `.all()` explícito), retorna `Proposicao | None`
- [x] 1.3 Adicionar `get_estatisticas_dashboard()` em `camara_repository.py`: retorna dict com `total`, `ativas`, `subtemas`, `por_subtema`, `por_status`, `temporal`, `ultima_atualizacao`
- [x] 1.4 Adicionar `listar_categorias_com_total()` em `camara_repository.py`: retorna lista de dicts com campos de Categoria + `total` (contagem de proposições vinculadas), ordenado por total DESC

## 2. Controller Flask

- [x] 2.1 Criar `src/backend/controllers/proposicoes_controller.py` com `proposicoes_bp = Blueprint('proposicoes', __name__)`
- [x] 2.2 Implementar `GET /api/proposicoes`: ler query params (pagina, por_pagina, q, parlamentar, partido, data_inicio, data_fim, subtema), chamar `listar_proposicoes_paginado`, serializar com aliases (`status`, `subtema`, `nome_autor`)
- [x] 2.3 Implementar `GET /api/proposicoes/<int:id>`: chamar `get_proposicao_detalhe`, serializar proposição com aliases + tramitações com aliases (data, descricao, orgao); retornar 404 se não encontrar
- [x] 2.4 Implementar `GET /api/estatisticas`: chamar `get_estatisticas_dashboard`, retornar dict no formato `{resumo, ultima_atualizacao, por_subtema, por_status, temporal}`
- [x] 2.5 Implementar `GET /api/temas`: chamar `listar_categorias_com_total`, retornar array JSON
- [x] 2.6 Adicionar handler de erro genérico no blueprint para retornar `{"error": "..."}` em vez de HTML

## 3. Registro do blueprint em app.py

- [x] 3.1 Adicionar `from src.backend.controllers.proposicoes_controller import proposicoes_bp` e `app.register_blueprint(proposicoes_bp)` em `src/backend/app.py` (após `db.init_app(app)`)

## 4. Verificação manual das rotas

- [x] 4.1 Iniciar `flask run` e confirmar que `GET /api/temas` retorna array de categorias com campo `total`
- [x] 4.2 Confirmar que `GET /api/proposicoes` retorna `{items, total, pagina, total_paginas}`
- [x] 4.3 Confirmar que `GET /api/proposicoes/<id>` retorna `{proposicao, tramitacoes}` (ou 404 para ID inválido)
- [x] 4.4 Confirmar que `GET /api/estatisticas` retorna todas as 5 chaves: `resumo`, `ultima_atualizacao`, `por_subtema`, `por_status`, `temporal`
- [x] 4.5 Confirmar que uma requisição a ID inexistente retorna `{"error": "..."}` com status 404 (não HTML)
