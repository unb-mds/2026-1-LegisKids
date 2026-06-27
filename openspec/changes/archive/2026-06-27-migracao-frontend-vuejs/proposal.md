## Why

O frontend atual em HTML/CSS/JS puro foi adequado para a fase inicial, mas as funcionalidades da Release 1 (dashboards, filtros combinados, paginação, gráficos interativos) exigem componentização, reatividade e organização que o vanilla JS não mantém de forma sustentável. O estudo técnico de frameworks ([`docs/estudos/frontend/frameworks_bibliotecas.md`](../../docs/estudos/frontend/frameworks_bibliotecas.md)) concluiu que Vue.js + Vite + Chart.js é a combinação com melhor custo-benefício para o projeto.

## What Changes

- **BREAKING** Substituição do scaffold vanilla (HTML/CSS/JS puro) por uma SPA Vue.js 3 com Vite como bundler
- Estrutura `frontend/` passa a ser um projeto Vite/Vue com `src/`, `public/`, `package.json` e `vite.config.js`
- Páginas existentes (ou planejadas) são reescritas como componentes Vue (`.vue` Single File Components)
- Roteamento entre páginas via **Vue Router 4**
- Estado global (filtros, paginação, tema) gerenciado via **Pinia**
- Gráficos implementados com **Chart.js 4** (barras, linhas, pizza — conforme US11, US12, US14)
- Comunicação com o backend Flask permanece via **Fetch API** (sem mudanças no backend)
- Identidade visual atual (variáveis CSS, fontes Cinzel/Inter, paleta institucional) preservada dentro dos componentes Vue
- Nenhuma dependência de Tailwind, Bootstrap ou frameworks CSS externos

## Capabilities

### New Capabilities

- `vue-project-scaffold`: Estrutura base do projeto Vue 3 + Vite — `package.json`, `vite.config.js`, `src/main.js`, `App.vue`, configuração de CORS para dev
- `vue-router-pages`: Rotas e páginas da aplicação — Home (dashboard principal), Busca (US08/US09/US10), Detalhes de proposição (US15), layout com Navbar persistente
- `pinia-state`: Stores Pinia para estado global — filtros de busca, página atual, dados de proposições carregados
- `chart-visualizations`: Componentes de gráficos com Chart.js integrados ao Fetch API — barras por subtema, linha temporal, rosca de status (preparação para US11/US13)
- `vue-components-ui`: Componentes reutilizáveis de UI alinhados ao Figma — `ProposicaoCard`, `FilterBar`, `Pagination`, `StatusBadge`, `LoadingSpinner`, `Navbar`

### Modified Capabilities

<!-- Nenhuma spec existente em openspec/specs/ é afetada em nível de requisitos — apenas a camada de implementação muda. -->

## Impact

- **Frontend:** reescrita completa da camada de apresentação; arquivos na pasta `frontend/` substituídos pela estrutura Vite/Vue
- **Backend Flask:** sem alterações — continua servindo JSON via endpoints REST; adicionar/confirmar headers CORS para `localhost:5173` (porta padrão do Vite dev server)
- **CI/CD:** pipeline do GitHub Actions deve incluir step de `npm install && npm run build` para o frontend
- **Dependências novas:** `vue@3`, `vue-router@4`, `pinia`, `chart.js`, `vite`, `@vitejs/plugin-vue` (todas via npm, sem impacto no `requirements.txt` do Python)
- **Documentação:** `CLAUDE.md` e `README.md` precisam refletir a nova stack e comandos de execução do frontend
