## Context

O Dashboard (`DashboardView.vue`) já busca `fetchEstatisticas()` e `fetchTemas()` no `onMounted` e monta 4 stats cards + 3 gráficos (`GraficoSubtemas`, `GraficoStatus`, `GraficoTemporal`) a partir desse payload. Esses componentes de gráfico já são genéricos (recebem `labels`/`values`/`cores` via props) e não têm nenhuma lógica acoplada ao Dashboard — são reutilizáveis como estão.

O card "Análises e Relatórios" nas Ações Rápidas do Dashboard hoje é uma âncora (`<a href="#graficos-secao">`) para a própria seção de gráficos do Dashboard, não uma página separada.

Consultei o usuário sobre o escopo de conteúdo da nova página (reaproveitar tudo vs. adicionar gráfico novo por partido vs. página mínima) — a decisão foi **reaproveitar integralmente os dados e componentes já existentes**, sem nenhuma mudança de backend nesta change.

## Goals / Non-Goals

**Goals:**
- Criar uma página própria (`/analises`) que sirva como "relatório" consolidado, reaproveitando dados e componentes já existentes.
- Manter a página enxuta: 4 cards + 3 gráficos, sem tabelas extensas ou paginação.
- Deixar explícito, ao final da página, que mais análises virão (gerencia expectativa e evita a sensação de página "incompleta").
- Fazer o card do Dashboard navegar de fato para a nova página.

**Non-Goals:**
- Qualquer gráfico ou indicador que exija dado não coletado hoje (ranking de parlamentares, temas emergentes, exportação PDF/CSV) — isso é Release 2 (US11, US12, US14) e fica para changes futuras. (Novos gráficos que apenas *cruzam* dados já coletados, como "Temas ao Longo do Tempo", são aceitos — ver Decisão 5.)
- Remover ou duplicar a seção de gráficos do próprio Dashboard — ela continua existindo como está.

## Decisions

### 1. Nova view dedicada, não reaproveitar `#graficos-secao` do Dashboard

**Decisão:** criar `AnalisesView.vue` com rota própria `/analises`, em vez de apenas manter a âncora do Dashboard.

**Rationale:** o pedido do usuário é por uma "página de Análise e Relatórios" — uma âncora dentro do Dashboard não atende isso; a navegação e a URL devem refletir uma seção própria (consistente com `/configuracoes`, `/notificacoes`, `/sobre`, que já são páginas dedicadas).

### 2. Fetch duplicado ao invés de estado compartilhado (Pinia)

**Decisão:** `AnalisesView.vue` faz sua própria chamada a `fetchEstatisticas()`/`fetchTemas()` no `onMounted`, do mesmo jeito que `DashboardView.vue` já faz — sem introduzir uma store Pinia para compartilhar esse estado entre as duas views.

**Rationale:** as duas páginas são navegadas independentemente (o usuário pode entrar direto em `/analises` pela URL); manter o fetch local em cada view é o padrão já usado no projeto (nenhuma view atual depende de estado pré-carregado por outra). Introduzir uma store para evitar uma segunda chamada HTTP seria otimização prematura para um payload pequeno e infrequente.

### 3. Reaproveitar os componentes de gráfico como estão, sem props novas

**Decisão:** `GraficoSubtemas`, `GraficoStatus` e `GraficoTemporal` são usados sem nenhuma alteração de código — só a composição do layout ao redor deles muda.

**Rationale:** os componentes já são genéricos e sem acoplamento ao Dashboard; qualquer necessidade futura de customização visual (ex: gráfico maior, cores diferentes) pode ser tratada via props/CSS no momento em que surgir, sem exigir mudança agora.

### 4. Card "Período Coberto" reaproveita a mesma lógica de formatação da flag do Dashboard

**Decisão:** a formatação de `data.periodo` (`data_inicio`/`data_fim` → `DD/MM/AAAA`) é reimplementada localmente em `AnalisesView.vue` (mesma função `formatarDataSimples` usada em `DashboardView.vue`), não extraída para um util compartilhado nesta change.

**Rationale:** é uma função de 3 linhas usada em 2 lugares — extrair para `src/frontend/src/utils/` agora seria abstração prematura para uma duplicação mínima. Se um terceiro consumidor aparecer, aí sim vale extrair.

### 5. Gráfico "Temas ao Longo do Tempo" — nova agregação cruzada, não uma nova coleta de dados

**Decisão:** adicionar `temporal_por_subtema` em `get_estatisticas_dashboard` — para cada `(ano, mês)` presente em `temporal`, contar proposições por categoria, usando a mesma junção `proposicao_categoria`/`Categoria` já usada em `por_subtema`. O payload é `{"labels": [...mesmos meses de "temporal"...], "series": [{"nome": ..., "values": [...]}]}`, uma série por categoria com pelo menos uma proposição.

**Rationale:** o usuário pediu explicitamente um gráfico interativo de "temas ao longo do tempo" depois de revisar a página. Os dados já existem (mesma tabela de junção usada por `por_subtema`); faltava apenas cruzá-los por mês. Reaproveitar as chaves de mês de `temporal` garante que o eixo X seja idêntico ao do gráfico de Evolução Temporal, facilitando comparação visual entre os dois gráficos.

**Interatividade:** implementada via `Chart.js` line chart com múltiplos `datasets` — a legenda já é clicável por padrão (toggle de série) e o tooltip usa `mode: 'index'` para mostrar todos os subtemas do mês ao passar o mouse. Não foi necessária nenhuma biblioteca nova.

**Cores:** reaproveita o mesmo mapa `nome → cor` (de `/api/temas`) já usado no gráfico de barras "Proposições por Subtema", garantindo que a cor de cada subtema seja consistente entre os dois gráficos da página.

### 6. Nota de "mais análises em breve" como texto estático no fim da página

**Decisão:** um bloco de texto simples (sem CTA, sem formulário) ao final da página, avisando que mais gráficos/análises serão adicionados.

**Rationale:** é exatamente o que o usuário pediu ("bote no fim da página que ainda criaremos mais gráficos e análises"); não há necessidade de componente novo — reaproveita a classe visual de `.erro-banner`/seção informativa já usada no Dashboard, adaptada para tom neutro (não é um erro).

## Risks / Trade-offs

- **Duplicação visual de conteúdo entre Dashboard e Análises:** aceito conscientemente — foi a opção escolhida pelo usuário entre as alternativas apresentadas. Se no futuro isso incomodar, dá para diferenciar as páginas (ex: Dashboard fica só com cards + alertas rápidos, Análises fica só com os gráficos).
- **Duas chamadas HTTP ao mesmo endpoint ao navegar entre Dashboard e Análises:** aceitável dado o volume de dados (payload pequeno, ~200 proposições agregadas) e a ausência de necessidade de tempo real.

## Migration Plan

1. Criar `AnalisesView.vue` reaproveitando fetch + componentes de gráfico do Dashboard.
2. Adicionar rota `/analises` em `router/index.js`.
3. Trocar o `<a href="#graficos-secao">` do Dashboard por `<RouterLink to="/analises">`.
4. Validar visualmente (desktop + mobile) com dados reais do Neon.

## Open Questions

Nenhuma — escopo e conteúdo já validados com o usuário.
