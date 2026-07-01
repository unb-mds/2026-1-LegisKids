## 1. Frontend — nova view

- [x] 1.1 Criar `src/frontend/src/views/AnalisesView.vue`: header com título "Análises e Relatórios" + descrição curta
- [x] 1.2 Buscar dados no `onMounted` via `fetchEstatisticas()` e `fetchTemas()` (mesmo padrão de `DashboardView.vue`), com `LoadingSpinner` e banner de erro em caso de falha
- [x] 1.3 Renderizar 4 cards de resumo: Total de Proposições, Em Tramitação, Subtemas Cobertos, Período Coberto (formatado via função local `formatarDataSimples`, `null`-safe)
- [x] 1.4 Renderizar os 3 gráficos reaproveitando `GraficoSubtemas`, `GraficoStatus` e `GraficoTemporal` sem alterar os componentes
- [x] 1.5 Adicionar bloco de texto ao final da página avisando que mais gráficos e análises serão adicionados futuramente (destacado com ícone, fundo azul claro e borda de destaque, a pedido do usuário)

## 2. Frontend — navegação

- [x] 2.1 Adicionar rota `/analises` (`name: "analises"`) em `src/frontend/src/router/index.js`, apontando para `AnalisesView.vue` (lazy-loaded, como as demais rotas exceto o Dashboard)
- [x] 2.2 Em `DashboardView.vue`, trocar o card "Análises e Relatórios" de `<a href="#graficos-secao">` para `<RouterLink to="/analises">`

## 3. Validação

- [x] 3.1 Rodar `flask run` + `npm run dev` e navegar até `/analises` com dados reais do Neon — conferir se os 4 cards e os 3 gráficos batem com os mesmos valores exibidos no Dashboard. Confirmado via screenshot: 198/198/8/"11/08/2025 até 26/06/2026", gráficos idênticos aos do Dashboard
- [x] 3.2 Conferir responsividade da nova página em viewport mobile (≤640px). Os cards empilham corretamente em 2 colunas; existe um bug de overflow horizontal pré-existente em todo o app (já observado em change anterior), não introduzido por esta página — fora de escopo
- [x] 3.3 Confirmar que o card "Análises e Relatórios" do Dashboard navega corretamente para `/analises`. Confirmado no DOM renderizado: `<a href="/analises" class="quick-action-card">`

## 4. Gráfico "Temas ao Longo do Tempo" (adicionado após revisão com o usuário)

- [x] 4.1 Em `get_estatisticas_dashboard` (`camara_repository.py`), adicionar agregação `temporal_por_subtema`: contagem de proposições por `(ano, mês, categoria)`, alinhada às mesmas chaves de mês de `temporal`
- [x] 4.2 Incluir `dados["temporal_por_subtema"]` na resposta de `/api/estatisticas` (`proposicoes_controller.py`)
- [x] 4.3 Criar `src/frontend/src/components/charts/GraficoTemasTempo.vue`: gráfico de linhas múltiplas (Chart.js), uma série por subtema, legenda clicável (toggle) e tooltip por índice de mês
- [x] 4.4 Em `AnalisesView.vue`, buscar `data.temporal_por_subtema`, mapear cor de cada série pelo mesmo `corPorNome` usado no gráfico de barras, e renderizar o novo gráfico com subtítulo explicando a interação da legenda
- [x] 4.5 Validar: reiniciar backend, confirmar via curl que `temporal_por_subtema` retorna séries coerentes com `por_subtema`/`temporal`, e capturar screenshot confirmando as 8 linhas coloridas e a legenda
