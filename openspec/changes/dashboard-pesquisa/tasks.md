## 1. HTML — estrutura e componentes

- [x] 1.1 Implementar navbar com logo SVG inline, links Projetos/Alertas/Análises, botões de configurações e notificações com badge de contagem
- [x] 1.2 Implementar botão "Voltar ao Dashboard" com ícone de seta esquerda e navegação via `history.back()`
- [x] 1.3 Implementar cabeçalho da página com título "Resultados da Pesquisa" e subtítulo descritivo
- [x] 1.4 Implementar search bar em estilo pill (border-radius 999px) com ícone de lupa e input pré-preenchido pela query da URL
- [x] 1.5 Implementar search summary card (fundo `#EEF3FF`) com bubble de ícone à esquerda, texto "Resultados para: <query>" e contador de resultados à direita
- [x] 1.6 Implementar toolbar com botão de filtros (ícone funil) à esquerda e dropdown de ordenação à direita
- [x] 1.7 Implementar título de seção "Projetos encontrados" acima da lista
- [x] 1.8 Implementar `<section id="resultsList">` como contêiner para os cards renderizados via JS
- [x] 1.9 Implementar `<nav id="pagination">` como contêiner para os botões de paginação gerados via JS
- [x] 1.10 Implementar footer com cor `#2846B7`, copyright e links (Sobre, Contato, Privacidade)

## 2. CSS — design system e responsividade

- [x] 2.1 Herdar todos os tokens de cor, sombra, border-radius e transição de `style.css` sem duplicar variáveis em `pesquisa.css`
- [x] 2.2 Estilizar `.back-button` com cor primária, hover `translateX(-2px)` e transição
- [x] 2.3 Estilizar `.search-summary` com fundo `var(--secondary)`, bordas sutis e layout flex space-between
- [x] 2.4 Estilizar `.toolbar__filters` e `.toolbar__sort-select` com border `1px solid var(--border)`, hover com borda primária
- [x] 2.5 Estilizar `.result-card` com hover `translateY(-2px)` e borda primária no hover, consistente com `projeto-card` do dashboard
- [x] 2.6 Implementar variantes de badge por status: `.is-urgent` (vermelho), `.is-active` (âmbar), `.is-approved` (verde), `.is-analysis` (azul)
- [x] 2.7 Estilizar `.pagination__btn` com estado ativo (`background: var(--primary)`) e disabled (opacity 0.45)
- [x] 2.8 Estilizar `.empty-state` centralizado dentro da lista de resultados
- [x] 2.9 Implementar breakpoint tablet (≤900px): search summary empilhado em coluna
- [x] 2.10 Implementar breakpoint mobile (≤640px): toolbar empilhada, cards com padding reduzido, paginação compacta

## 3. JavaScript — mock data e interatividade

- [x] 3.1 Definir `MOCK_RESULTS` com os 3 itens do spec (PL-2654/2026, PL-2103/2026, PL-1987/2026) e `TOTAL_RESULTS = 23`, `TOTAL_PAGES = 8`
- [x] 3.2 Implementar `getQueryFromURL()` para ler `?q=` via `URLSearchParams` e pré-preencher o campo de busca
- [x] 3.3 Implementar `filterResults(query)` com filtro case-insensitive sobre id, título, tópico, descrição, instituição e status
- [x] 3.4 Implementar `sortResults(items, mode)` com quatro modos: `recent`, `old`, `urgent`, `alpha`
- [x] 3.5 Implementar `renderResultCard(item)` gerando `<article class="result-card">` com badges, status, título, descrição e rodapé com ícones SVG de data e instituição
- [x] 3.6 Implementar `renderResults(items)` com empty state quando array vazio
- [x] 3.7 Implementar `renderPagination(current, total)` com algoritmo de janela deslizante e reticências entre gaps
- [x] 3.8 Implementar `updateSearchSummary(query)` atualizando a query exibida e o contador de resultados
- [x] 3.9 Implementar `refresh()` orquestrando filter → sort → renderResults → updateSearchSummary
- [x] 3.10 Wiring de todos os event listeners: `input` no search, `keydown Enter` no search, `change` no sort, `click` no botão de filtros e `click` no botão voltar
- [x] 3.11 Implementar `escapeHtml()` para sanitizar dados antes de inserir no innerHTML

## 4. Integração futura (próximas tasks — não nesta change)

- [ ] 4.1 Substituir `MOCK_RESULTS` por `fetch('/api/proposicoes?q=&page=&per_page=')` quando o endpoint Flask estiver disponível
- [ ] 4.2 Alimentar `renderPagination()` com `total_pages` retornado pela API em vez do mock fixo
- [ ] 4.3 Implementar modal lateral de filtros (US09): parlamentar, partido, data e subtema
- [ ] 4.4 Preservar estado de filtros e página atual na URL para permitir compartilhamento e navegação com back/forward
- [ ] 4.5 Implementar histórico das últimas 10 buscas por usuário autenticado (US08 complemento — Release 2)
- [ ] 4.6 Substituir SVGs inline pelos assets de imagem quando `frontend/assets/` for populado
