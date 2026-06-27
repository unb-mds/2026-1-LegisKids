# Spec: pinia-state

## Objetivo

Definir o gerenciamento de estado global da SPA via Pinia: filtros de busca ativos, paginação e lista de proposições carregadas.

## Contexto

O LegisKids usa Pinia como gerenciador de estado oficial do Vue 3. O estado gerenciado inclui filtros de busca (compartilhados entre FilterBar e BuscaView) e a lista de proposições retornada pelo backend.

## Escopo

- Store `useBuscaStore` para filtros e paginação
- Store `useProposicoesStore` para lista, total, loading e error
- Registro do Pinia no `main.js` antes do `app.mount()`

## Requisitos

### Requirement: Store de busca e filtros
O sistema SHALL possuir uma store Pinia `useBuscaStore` em `src/stores/busca.js` que gerencia o estado da busca ativa: termo de busca, filtros selecionados (parlamentar, partido, dataInicio, dataFim, subtema) e número da página atual.

#### Scenario: Filtros persistem na paginação
- **WHEN** o usuário está na página 2 de resultados com filtro "subtema: cyberbullying" ativo
- **THEN** os filtros permanecem aplicados e os resultados da página 2 refletem o filtro

#### Scenario: Limpar filtros reseta a paginação
- **WHEN** o usuário clica em "Limpar Filtros"
- **THEN** todos os filtros são resetados para valores padrão e a página volta para 1

### Requirement: Store de proposições carregadas
O sistema SHALL possuir uma store Pinia `useProposicoesStore` em `src/stores/proposicoes.js` que armazena a lista atual de proposições retornadas pelo backend, o total de resultados, o estado de carregamento (`loading`) e o erro atual (se houver).

#### Scenario: Estado de carregamento
- **WHEN** uma requisição ao backend está em andamento
- **THEN** `loading` é `true` e os componentes exibem o `LoadingSpinner`

#### Scenario: Erro de rede tratado na store
- **WHEN** o backend retorna erro 500 ou a rede falha
- **THEN** `error` é preenchido com mensagem descritiva e `loading` volta para `false`

#### Scenario: Dados carregados com sucesso
- **WHEN** o backend retorna lista de proposições com sucesso
- **THEN** a lista é armazenada na store, `loading` é `false` e `error` é `null`

### Requirement: Store inicializada antes da aplicação montar
O sistema SHALL registrar o Pinia no `src/main.js` via `app.use(createPinia())` antes de `app.mount('#app')`, garantindo que as stores estejam disponíveis em todos os componentes.

#### Scenario: Store acessível em qualquer componente
- **WHEN** qualquer componente importa e usa `useBuscaStore()` ou `useProposicoesStore()`
- **THEN** o estado é compartilhado corretamente sem erros de "store not found"
