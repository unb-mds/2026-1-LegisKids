## MODIFIED Requirements

### Requirement: Componente ProposicaoCard
O sistema SHALL possuir `src/components/ProposicaoCard.vue` que recebe via props os campos `titulo`, `autor`, `partido`, `data`, `status`, `subtema`, `id`, `sigla_tipo`, `numero` e `ano`, e os renderiza como card clicável que navega para `/proposicao/:id`. O card SHALL exibir o código legível da proposição no formato `sigla_tipo numero/ano` (ex.: "PL 1234/2023") em vez do `id` numérico interno.

#### Scenario: Card renderizado com dados completos
- **WHEN** o componente recebe todos os campos da proposição
- **THEN** exibe o código no formato `sigla_tipo numero/ano`, título, autor, partido, data formatada e badge de status com cor correspondente

#### Scenario: Campo ausente tratado com fallback
- **WHEN** o campo `autor` não está presente nos dados
- **THEN** exibe "Autor não informado" sem quebrar a renderização

#### Scenario: Clique no card navega para detalhes
- **WHEN** o usuário clica no card
- **THEN** o Vue Router navega para `/proposicao/:id` sem reload da página

### Requirement: Componente FilterBar
O sistema SHALL possuir `src/components/FilterBar.vue` que renderiza os controles de filtro e emite evento `filter-changed` com os valores atuais quando qualquer filtro muda (US09). O filtro de subtema SHALL emitir o nome do tema (string), nunca o objeto tema completo.

#### Scenario: Filtros emitem evento ao mudar
- **WHEN** o usuário seleciona um partido no select
- **THEN** o componente emite `filter-changed` com objeto `{ partido: 'PT', ... }`

#### Scenario: Filtro de subtema emite o nome como string
- **WHEN** o usuário seleciona um subtema no select
- **THEN** o componente emite `filter-changed` com `{ subtema: '<nome do tema>', ... }`, nunca com o objeto tema (`[object Object]`)

#### Scenario: Filtros ativos exibidos como tags removíveis
- **WHEN** existem filtros ativos
- **THEN** cada filtro ativo é exibido como tag com botão "×" para remoção individual

#### Scenario: Botão limpar filtros
- **WHEN** o usuário clica em "Limpar filtros"
- **THEN** todos os filtros são resetados e o evento `filter-changed` é emitido com valores padrão

### Requirement: Componente StatusBadge
O sistema SHALL possuir `src/components/StatusBadge.vue` que recebe um `status` (string) via prop e renderiza um badge colorido seguindo a paleta institucional. O status `Encerrado` SHALL usar a mesma cor/classe (cinza) já usada para `Arquivado`.

#### Scenario: Badge colorido por status
- **WHEN** a prop `status` é "Aprovado"
- **THEN** o badge exibe "Aprovado" com fundo verde (usando variável CSS da paleta)

#### Scenario: Badge para status Encerrado
- **WHEN** a prop `status` é "Encerrado"
- **THEN** o badge exibe "Encerrado" com a mesma cor/classe cinza usada para "Arquivado"
