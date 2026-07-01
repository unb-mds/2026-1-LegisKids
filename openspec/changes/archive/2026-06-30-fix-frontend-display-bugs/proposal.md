## Why

Três bugs visuais no frontend (Vue) estão degradando a experiência de busca e visualização de proposições: o filtro de subtema envia o objeto inteiro em vez do nome (quebrando a filtragem), o badge de status não reconhece o valor "Encerrado" (renderiza sem estilo), e cards/detalhes exibem o `id` numérico interno em vez do código legível da proposição (`sigla_tipo numero/ano`). São correções pontuais, sem mudança de arquitetura, restritas a `src/frontend/`.

## What Changes

- Corrigir `FilterBar.vue` para vincular o `<option>` de subtema ao nome (`t.nome`) em vez do objeto `t`, garantindo que `filter-changed` emita uma string e não `[object Object]`.
- Adicionar o status `Encerrado` ao mapeamento de cores de `StatusBadge.vue`, reaproveitando a mesma classe/cor cinza já usada para `Arquivado`.
- Substituir a exibição do `id` numérico pelo código legível (`sigla_tipo numero/ano`) em `ProposicaoCard.vue` e `DetalheView.vue`, usando os campos `sigla_tipo`, `numero` e `ano` já retornados pela API.

## Capabilities

### New Capabilities
(nenhuma)

### Modified Capabilities
- `vue-components-ui`: `FilterBar` deve emitir o nome do subtema (string) e não o objeto tema; `StatusBadge` deve estilizar o status `Encerrado` igual a `Arquivado`; `ProposicaoCard` deve exibir o código legível da proposição (`sigla_tipo numero/ano`) em vez do `id` numérico.

## Impact

- Código afetado: `src/frontend/src/components/FilterBar.vue`, `src/frontend/src/components/StatusBadge.vue`, `src/frontend/src/components/ProposicaoCard.vue`, `src/frontend/src/views/DetalheView.vue`.
- Nenhum endpoint, modelo ou rota de backend é alterado.
- Sem novas dependências.
