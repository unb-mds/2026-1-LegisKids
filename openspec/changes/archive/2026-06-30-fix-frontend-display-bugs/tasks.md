## 1. Filtro de subtema (FilterBar.vue)

- [x] 1.1 Em `src/frontend/src/components/FilterBar.vue`, trocar `:value="t"` por `:value="t.nome"` no `<option v-for="t in temas">` do select de subtema
- [x] 1.2 Confirmar que `filter-changed` passa a emitir `{ subtema: '<nome>', ... }` (string), nunca o objeto tema

## 2. Badge de status "Encerrado" (StatusBadge.vue)

- [x] 2.1 Em `src/frontend/src/components/StatusBadge.vue`, adicionar o caso `Encerrado` ao mapeamento de classes/cores, reaproveitando a mesma cor cinza de `Arquivado`
- [x] 2.2 Confirmar visualmente que o badge `Encerrado` renderiza com a cor cinza e não cai no fallback sem estilo

## 3. Código legível da proposição (ProposicaoCard.vue, DetalheView.vue)

- [x] 3.1 Em `src/frontend/src/components/ProposicaoCard.vue`, substituir a exibição do `id` numérico por `{{ proposicao.sigla_tipo }} {{ proposicao.numero }}/{{ proposicao.ano }}`
- [x] 3.2 Em `src/frontend/src/views/DetalheView.vue`, aplicar a mesma substituição do `id` numérico pelo formato `sigla_tipo numero/ano`
- [x] 3.3 Verificar que o `id` continua sendo usado internamente (rota `/proposicao/:id`, key de lista) e que apenas a exibição visual muda

## 4. Validação

- [x] 4.1 Rodar o frontend localmente (`npm run dev`) e validar manualmente: filtro de subtema funcionando, badge "Encerrado" estilizado, código da proposição exibido em card e na tela de detalhes
- [x] 4.2 Rodar lint/build do frontend (`npm run build` ou equivalente) para garantir que não há erros de template

## 5. Robustez na exibição de partido (BuscaView.vue, DetalheView.vue)

- [x] 5.1 Causa raiz identificada: `sigla_partido` chega sempre vazio do backend (ETL não busca `siglaPartido`, que não existe na listagem da API da Câmara — precisa do endpoint de autores). Fix de dado fica fora do escopo desta branch (frontend-only); registrado para change de backend futura.
- [x] 5.2 Em `BuscaView.vue` e `DetalheView.vue`, adicionar `partidoLabel`/`partidoLabel(p)` que lê tanto `partido` (objeto `{sigla, nome}`, quando o backend popular o relacionamento) quanto `sigla_partido` (string), evitando que o card/detalhe exiba `[object Object]` quando o backend for corrigido
