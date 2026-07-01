## Why

O card "Análises e Relatórios" já existe nas Ações Rápidas do Dashboard (`DashboardView.vue`), mas hoje ele só rola a página até a seção de gráficos do próprio Dashboard (`href="#graficos-secao"`) — não existe uma página dedicada de análise. Isso limita a experiência: o usuário que quer "ver os relatórios" cai na mesma tela que já viu, sem um espaço próprio para consolidar indicadores em formato de relatório.

## What Changes

- Nova view `AnalisesView.vue` e rota `/analises`, acessível a partir do card "Análises e Relatórios" do Dashboard (que passa a navegar para a rota em vez de rolar âncora).
- A página consome os dados que **já existem** (mais uma pequena agregação nova, ver abaixo) via `GET /api/estatisticas` e `GET /api/temas`.
- Conteúdo, deliberadamente enxuto (decisão validada com o usuário):
  - 4 cards de resumo: Total de Proposições, Em Tramitação, Subtemas Cobertos, Período Coberto (reaproveitando o campo `periodo` recém-adicionado ao endpoint).
  - 3 gráficos reaproveitando os componentes já existentes (`GraficoSubtemas`, `GraficoStatus`, `GraficoTemporal`), organizados como uma visão de relatório.
  - Nota ao final da página avisando que mais gráficos e análises serão adicionados futuramente (Release 2 — US11, US12, US14).
- **Adicionado após revisão com o usuário:** um 4º gráfico interativo, "Temas ao Longo do Tempo" — linhas múltiplas (uma por subtema) mostrando a evolução mensal de cada categoria, com legenda clicável para isolar/ocultar subtemas. Isso exige uma nova agregação no backend (`temporal_por_subtema`), já que `/api/estatisticas` só tinha totais agregados (por subtema OU por mês, nunca os dois cruzados).

## Capabilities

### New Capabilities
- `pagina-analises-relatorios`: página dedicada de análise consolidando indicadores e gráficos já coletados, servindo de base para futuras análises mais avançadas (temas emergentes, ranking de parlamentares, exportação).

### Modified Capabilities
- `dashboard-principal` (Vue): o card "Análises e Relatórios" nas Ações Rápidas passa a navegar para `/analises` em vez de rolar até `#graficos-secao`.

## Impact

- **Frontend**: nova view `src/frontend/src/views/AnalisesView.vue`, novo componente `src/frontend/src/components/charts/GraficoTemasTempo.vue`, nova rota em `src/frontend/src/router/index.js`, ajuste de link em `DashboardView.vue`.
- **Backend**: `camara_repository.py` (nova agregação `temporal_por_subtema` em `get_estatisticas_dashboard`), `proposicoes_controller.py` (inclui o campo na resposta de `/api/estatisticas`).
- **Sem impacto**: banco de dados (schema), autenticação, outras rotas.
