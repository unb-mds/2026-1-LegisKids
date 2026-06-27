## ADDED Requirements

### Requirement: Componente ProposicaoCard
O sistema SHALL possuir `src/components/ProposicaoCard.vue` que recebe via props os campos `titulo`, `autor`, `partido`, `data`, `status`, `subtema` e `id` de uma proposição e os renderiza como card clicável que navega para `/proposicao/:id`.

#### Scenario: Card renderizado com dados completos
- **WHEN** o componente recebe todos os campos da proposição
- **THEN** exibe título, autor, partido, data formatada e badge de status com cor correspondente

#### Scenario: Campo ausente tratado com fallback
- **WHEN** o campo `autor` não está presente nos dados
- **THEN** exibe "Autor não informado" sem quebrar a renderização

#### Scenario: Clique no card navega para detalhes
- **WHEN** o usuário clica no card
- **THEN** o Vue Router navega para `/proposicao/:id` sem reload da página

### Requirement: Componente FilterBar
O sistema SHALL possuir `src/components/FilterBar.vue` que renderiza os controles de filtro (campo texto, selects de partido/parlamentar/subtema, date pickers de período) e emite evento `filter-changed` com os valores atuais quando qualquer filtro muda (US09).

#### Scenario: Filtros emitem evento ao mudar
- **WHEN** o usuário seleciona um partido no select
- **THEN** o componente emite `filter-changed` com objeto `{ partido: 'PT', ... }`

#### Scenario: Filtros ativos exibidos como tags removíveis
- **WHEN** existem filtros ativos
- **THEN** cada filtro ativo é exibido como tag com botão "×" para remoção individual

#### Scenario: Botão limpar filtros
- **WHEN** o usuário clica em "Limpar filtros"
- **THEN** todos os filtros são resetados e o evento `filter-changed` é emitido com valores padrão

### Requirement: Componente Pagination
O sistema SHALL possuir `src/components/Pagination.vue` que recebe `totalItems`, `itemsPerPage` e `currentPage` via props, renderiza os controles de paginação e emite `page-changed` e `per-page-changed` (US10).

#### Scenario: Navegação entre páginas
- **WHEN** o usuário clica em "Próxima" ou em um número de página
- **THEN** o evento `page-changed` é emitido com o número correto

#### Scenario: Seletor de itens por página
- **WHEN** o usuário altera o select para "25 itens por página"
- **THEN** o evento `per-page-changed` é emitido com o valor `25`

#### Scenario: Página atual marcada como ativa
- **WHEN** `currentPage` é `3`
- **THEN** o botão da página 3 tem classe CSS ativa e está desabilitado para clique

### Requirement: Componente StatusBadge
O sistema SHALL possuir `src/components/StatusBadge.vue` que recebe um `status` (string) via prop e renderiza um badge colorido seguindo a paleta institucional: verde para "Aprovado", amarelo para "Em tramitação", cinza para "Arquivado".

#### Scenario: Badge colorido por status
- **WHEN** a prop `status` é "Aprovado"
- **THEN** o badge exibe "Aprovado" com fundo verde (usando variável CSS da paleta)

### Requirement: Componente LoadingSpinner
O sistema SHALL possuir `src/components/LoadingSpinner.vue` que exibe indicador de carregamento acessível com `role="status"` e `aria-label="Carregando..."`, visível enquanto `useProposicoesStore().loading` for `true`.

#### Scenario: Spinner visível durante carregamento
- **WHEN** a store tem `loading: true`
- **THEN** o `LoadingSpinner` é exibido na área de conteúdo principal

#### Scenario: Spinner oculto após carregamento
- **WHEN** `loading` volta para `false`
- **THEN** o spinner é removido do DOM e o conteúdo é exibido

### Requirement: Componente Navbar responsivo
O sistema SHALL possuir `src/components/Navbar.vue` com o logo do LegisKids, links de navegação para as rotas principais e comportamento responsivo (menu hambúrguer em telas menores que 768px) conforme design no Figma (US17).

#### Scenario: Links de navegação ativos
- **WHEN** o usuário está na rota `/busca`
- **THEN** o link "Busca" na Navbar tem classe ativa via `RouterLink` com `active-class`

#### Scenario: Menu responsivo em mobile
- **WHEN** a largura da tela é menor que 768px
- **THEN** os links de navegação ficam ocultos e um ícone de menu hambúrguer é exibido; ao clicar, o menu expande

#### Scenario: Navegação por teclado na Navbar
- **WHEN** o usuário navega pela Navbar usando Tab e Enter
- **THEN** todos os links são acessíveis e ativáveis via teclado (conformidade WCAG AA — US17)
