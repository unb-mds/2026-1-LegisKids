## 1. Scaffold do Projeto Vue 3 + Vite

- [x] 1.1 Criar projeto Vue 3 em `frontend/` via `npm create vue@latest` com Vue Router e Pinia habilitados
- [x] 1.2 Instalar Chart.js: `npm install chart.js` dentro de `frontend/`
- [x] 1.3 Configurar `frontend/.env` e `.env.example` com `VITE_API_BASE_URL=http://localhost:5000`
- [x] 1.4 Adicionar `frontend/.env` ao `.gitignore` e commitar `.env.example`
- [x] 1.5 Migrar variáveis CSS da identidade visual (paleta, fontes Cinzel/Inter) para `frontend/src/assets/main.css`
- [x] 1.6 Importar `main.css` globalmente no `frontend/src/main.js`
- [x] 1.7 Verificar que `npm run dev` sobe em `http://localhost:5173` sem erros
- [x] 1.8 Verificar que `npm run build` gera `frontend/dist/` sem erros

## 2. Services (comunicação com Flask)

- [x] 2.1 Criar `frontend/src/services/proposicoes.js` com funções `fetchProposicoes(filtros, pagina, porPagina)` e `fetchProposicao(id)` usando Fetch API e `VITE_API_BASE_URL`
- [x] 2.2 Criar `frontend/src/services/temas.js` com função `fetchTemas()`
- [x] 2.3 Criar `frontend/src/services/estatisticas.js` com função `fetchEstatisticas()` para dados dos gráficos
- [x] 2.4 Configurar `flask-cors` no backend Flask para permitir requisições de `http://localhost:5173`

## 3. Stores Pinia

- [x] 3.1 Criar `frontend/src/stores/busca.js` com estado: `termo`, `filtros` (parlamentar, partido, dataInicio, dataFim, subtema), `pagina`, `porPagina` e ação `limparFiltros()`
- [x] 3.2 Criar `frontend/src/stores/proposicoes.js` com estado: `lista`, `total`, `loading`, `error` e ações `carregar(filtros)` e `resetar()`
- [x] 3.3 Registrar `createPinia()` no `frontend/src/main.js` antes de `app.mount()`

## 4. Componentes de UI Base

- [x] 4.1 Criar `frontend/src/components/Navbar.vue` com logo, links de navegação via `RouterLink`, classe ativa automática e menu hambúrguer responsivo (< 768px)
- [x] 4.2 Criar `frontend/src/components/StatusBadge.vue` com cores institucionais por status (Aprovado → verde, Em tramitação → amarelo, Arquivado → cinza)
- [x] 4.3 Criar `frontend/src/components/LoadingSpinner.vue` com `role="status"` e `aria-label="Carregando..."`
- [x] 4.4 Criar `frontend/src/components/ProposicaoCard.vue` com props (titulo, autor, partido, data, status, subtema, id), fallback para campos ausentes e clique navegando para `/proposicao/:id`
- [x] 4.5 Criar `frontend/src/components/FilterBar.vue` com controles de filtro e emissão de evento `filter-changed`; exibir filtros ativos como tags removíveis
- [x] 4.6 Criar `frontend/src/components/Pagination.vue` com props (totalItems, itemsPerPage, currentPage) e emissão de `page-changed` e `per-page-changed`; select de 10/25/50 itens por página

## 5. Componentes de Gráficos (Chart.js)

- [x] 5.1 Criar `frontend/src/components/charts/GraficoSubtemas.vue` com gráfico de barras verticais; destruir instância Chart.js no `onUnmounted`; `aria-label` no `<canvas>`
- [x] 5.2 Criar `frontend/src/components/charts/GraficoTemporal.vue` com gráfico de linha temporal; destruir instância no `onUnmounted`
- [x] 5.3 Criar `frontend/src/components/charts/GraficoStatus.vue` com gráfico de rosca por status; destruir instância no `onUnmounted`
- [x] 5.4 Verificar que todos os gráficos exibem "Nenhum dado disponível" quando dados estão vazios

## 6. Roteamento e Views

- [x] 6.1 Configurar Vue Router em `frontend/src/router/index.js` com rotas: `/` → `DashboardView`, `/busca` → `BuscaView`, `/proposicao/:id` → `DetalheView`; adicionar rota catch-all para 404
- [x] 6.2 Criar `frontend/src/views/DashboardView.vue` com cards de estatísticas resumidas (total de proposições, distribuição por subtema) e área para os três gráficos
- [x] 6.3 Criar `frontend/src/views/BuscaView.vue` integrando `FilterBar`, `ProposicaoCard` (lista), `Pagination` e `LoadingSpinner`; conectar com as stores `busca` e `proposicoes`
- [x] 6.4 Criar `frontend/src/views/DetalheView.vue` com título, autor, partido, data, status, ementa completa, link para documento oficial e área de histórico de tramitação em linha do tempo
- [x] 6.5 Atualizar `frontend/src/App.vue` para exibir `Navbar` e `<RouterView>` (Navbar fora do RouterView)

## 7. Responsividade e Acessibilidade (US17)

- [x] 7.1 Verificar responsividade de todas as views em 320px, 768px e desktop (1280px)
- [x] 7.2 Verificar contraste mínimo WCAG AA nas cores de texto e background
- [x] 7.3 Verificar navegação por teclado: Tab, Enter e Esc funcionando em Navbar, FilterBar, cards e paginação

## 8. CI/CD e Documentação

- [x] 8.1 Adicionar step de `npm install && npm run build` no GitHub Actions para o frontend
- [x] 8.2 Atualizar `CLAUDE.md` com a nova stack frontend (Vue 3 + Vite + Chart.js) e os comandos de execução
- [x] 8.3 Atualizar `README.md` com instruções de instalação e execução do frontend (`cd frontend && npm install && npm run dev`)
