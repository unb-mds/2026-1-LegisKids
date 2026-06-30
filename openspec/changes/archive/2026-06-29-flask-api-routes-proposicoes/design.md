## Context

O frontend Vue 3 já está implementado e consumindo 4 endpoints REST. O backend Flask tem models, repository e service completos, mas zero rotas HTTP de leitura. O bloqueio é pura ausência de controller — os dados já existem no banco.

**Estado atual do repositório** (métodos relevantes):
- `get_ids_existentes`, `get_proposicoes_pendentes`, `upsert_proposicoes_lote` — voltados para ETL
- `get_ultimas_execucoes(limite)` — retorna SyncExecucoes; serve para achar o último sync bem-sucedido
- Nenhum método de listagem, detalhe ou agregação para a API de leitura

**Gaps de dados descobertos na análise do frontend:**
1. `proposicoes` não tem coluna `autor`/`nome_autor` — o frontend tem fallback para null; retornar campo ausente.
2. `proposicoes` não tem coluna `url_documento`/`url` — idem, fallback visual no frontend.
3. O frontend lê `status` mas o banco tem `descricao_situacao` — resolver com alias na serialização.
4. O frontend lê `subtema`/`categoria` (string) mas o banco tem `categorias` (array) — retornar o nome da primeira categoria como `subtema`.
5. Tramitações: frontend lê `data`, `descricao`, `orgao`; banco tem `data_hora`, `descricao_tramitacao`, `sigla_orgao` — adicionar aliases no dict.

## Goals / Non-Goals

**Goals:**
- Implementar `GET /api/proposicoes`, `GET /api/proposicoes/<id>`, `GET /api/estatisticas`, `GET /api/temas` com respostas que o frontend atual já interpreta corretamente.
- Adicionar métodos de leitura no repositório para não escrever SQL no controller.
- Todos os erros retornam JSON `{"error": "..."}` com status HTTP adequado.

**Non-Goals:**
- Autenticação / autorização (Release 2).
- Modificar `camara_service.py` ou `camara_scheduler.py`.
- Migrações de banco — nenhuma coluna nova.
- Endpoints de escrita (POST/PUT/DELETE).

## Decisions

**D1 — Blueprint Flask separado**
`controllers/proposicoes_controller.py` exporta `proposicoes_bp`. Registrado em `app.py` com uma linha. Alternativa (rotas inline em app.py) rejeitada por falta de separação.

**D2 — Aliases de campo na serialização, não nos models**
`Proposicao.to_dict()` permanece inalterado. O controller cria um dict derivado adicionando `status`, `subtema`, `nome_autor` etc. Alternativa (alterar `to_dict()`) rejeitada porque quebraria a consistência interna usada pelo service/scheduler.

**D3 — Queries de agregação no repositório, não no controller**
Métodos novos em `camara_repository.py`: `listar_proposicoes_paginado`, `get_proposicao_detalhe`, `get_estatisticas_dashboard`, `listar_categorias_com_total`. Controller chama o repositório, nunca `db.session` diretamente.

**D4 — Filtro por subtema via JOIN em proposicao_categoria**
`subtema` no query param filtra por `Categoria.nome`. Exige JOIN; feito com SQLAlchemy (sem SQL raw).

**D5 — Lazy loading explícito para tramitações na rota de detalhe**
A rota de detalhe carrega `prop.tramitacoes.all()` explicitamente. A rota de lista NÃO carrega tramitações (evita N+1).

## Risks / Trade-offs

**[N+1 nas categorias na lista]** → Mitigado pela paginação (máx. 50 itens/página) e `joinedload` nas categorias.

**[Dados sem autor]** → Frontend já tem fallback para 'Não informado'; campo ausente na resposta é aceitável para R1.

**[`url_documento` inexistente]** → Seção de link no DetalheView não renderiza se o campo for null; sem impacto visual crítico para R1.

**[Estatísticas com banco vazio]** → Contagens retornam 0, listas retornam vazias; frontend mostra '—' nos cards.

## Migration Plan

1. Criar `src/backend/controllers/proposicoes_controller.py`
2. Adicionar métodos de leitura em `src/backend/repository/camara_repository.py`
3. Adicionar duas linhas em `src/backend/app.py` (import + register_blueprint)
4. Rollback: remover as duas linhas de app.py e o arquivo do controller (sem efeito no banco)
