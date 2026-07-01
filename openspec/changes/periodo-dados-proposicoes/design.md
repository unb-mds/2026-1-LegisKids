## Context

`get_estatisticas_dashboard()` (`src/backend/repository/camara_repository.py:289`) já monta o payload consumido por `DashboardView.vue` via `fetchEstatisticas()` (`GET /api/estatisticas`). A view já tem um padrão visual pronto para "flags" informativas no cabeçalho — a classe `.last-update`, usada hoje só para `ultima_atualizacao` (`DashboardView.vue:10-12`). A nova flag de período deve seguir exatamente esse padrão, apenas com um segundo `<span>`.

O campo mais adequado para representar "proposições salvas de X até Y" é `Proposicao.data_apresentacao` (data legislativa de apresentação, indexada — `idx_proposicoes_data_apresentacao`), não `data_coleta` (timestamp técnico de quando o registro entrou no banco). O usuário quer saber que período legislativo está coberto, não quando o scraper rodou.

## Goals / Non-Goals

**Goals:**
- Expor `periodo.data_inicio` / `periodo.data_fim` no `/api/estatisticas`.
- Exibir a flag no dashboard reaproveitando o estilo `.last-update` existente.
- Lidar corretamente com banco vazio (não quebrar, não mostrar flag).

**Non-Goals:**
- Filtrar buscas ou paginação por esse período (isso já existe via `data_inicio`/`data_fim` em `/api/proposicoes`, US09).
- Adicionar seletor de intervalo interativo — é uma flag informativa, somente leitura.
- Alterar `ultima_atualizacao` existente.

## Decisions

### 1. Campo de referência: `data_apresentacao`, não `data_coleta`

**Decisão:** o período é `MIN(data_apresentacao)` até `MAX(data_apresentacao)`.

**Rationale:** o pedido é sobre a cobertura das proposições em si ("temos proposições salvas da data X até a data Y"), que é uma pergunta sobre o dado legislativo, não sobre a infraestrutura de coleta. `data_coleta` já é implicitamente comunicado por `ultima_atualizacao` (via `SyncExecution`).

### 2. Cálculo via agregação SQL, não em Python

**Decisão:** usar `func.min` / `func.max` na mesma query de `get_estatisticas_dashboard`, em vez de carregar proposições e calcular em memória.

**Rationale:** consistente com o resto da função, que já usa `func.count`/`func.extract` agregados no banco. Evita trazer registros desnecessários.

### 3. Payload: objeto aninhado `periodo`, não campos soltos

**Decisão:** `{"periodo": {"data_inicio": "2022-01-01", "data_fim": "2026-06-30"}}` em vez de `data_inicio`/`data_fim` soltos na raiz do JSON.

**Rationale:** evita colisão de nomes com os query params `data_inicio`/`data_fim` já usados em `/api/proposicoes` (semântica diferente: ali são filtros de busca; aqui é um resumo). Mantém o payload de `/api/estatisticas` organizado por seção, como já é (`resumo`, `por_subtema`, `por_status`, `temporal`).

### 4. Banco vazio → `periodo: null`

**Decisão:** se não houver nenhuma proposição, `MIN`/`MAX` retornam `NULL` no SQL; o backend serializa `periodo` como `null` inteiro, e o frontend simplesmente não renderiza a flag (`v-if`).

**Rationale:** mesmo padrão já usado por `ultimaAtualizacao` no frontend (`v-if="ultimaAtualizacao"`), sem necessidade de estado de erro dedicado.

## Risks / Trade-offs

- **Datas fora de ordem** (ex: proposição antiga inserida depois): irrelevante aqui, pois o cálculo é sobre `data_apresentacao` armazenada, não sobre ordem de inserção — `MIN`/`MAX` resolve isso naturalmente.
- **Formato de data no frontend:** reaproveitar `toLocaleString('pt-BR')`/`toLocaleDateString('pt-BR')` já usado para `ultimaAtualizacao`, para manter consistência visual.

## Migration Plan

1. Backend: adicionar `MIN`/`MAX` de `data_apresentacao` em `get_estatisticas_dashboard` e incluir `periodo` na resposta de `/api/estatisticas`.
2. Frontend: ler `data.periodo` em `DashboardView.vue`, formatar como `DD/MM/AAAA`, renderizar novo `<span class="last-update">` condicional.
3. Testar com banco populado e com banco vazio (ou filtrado sem resultados).

## Open Questions

Nenhuma — escopo é pequeno e autocontido.
