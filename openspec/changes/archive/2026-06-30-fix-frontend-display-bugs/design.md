## Context

Três bugs de exibição foram identificados em componentes Vue já existentes (`FilterBar.vue`, `StatusBadge.vue`, `ProposicaoCard.vue`, `DetalheView.vue`). Todos os dados necessários (`sigla_tipo`, `numero`, `ano`, nome do tema) já chegam da API — não há mudança de contrato com o backend. O escopo é estritamente `src/frontend/`.

## Goals / Non-Goals

**Goals:**
- Corrigir o `v-for`/`:value` do select de subtema em `FilterBar.vue` para emitir o nome (string) do tema.
- Cobrir o status `Encerrado` em `StatusBadge.vue` com a mesma classe visual de `Arquivado`.
- Exibir o código legível da proposição (`sigla_tipo numero/ano`) em vez do `id` numérico em `ProposicaoCard.vue` e `DetalheView.vue`.

**Non-Goals:**
- Não alterar endpoints, models ou serviços do backend.
- Não alterar a identidade visual, paleta de cores ou layout além do necessário para o badge `Encerrado`.
- Não refatorar `FilterBar`, `StatusBadge`, `ProposicaoCard` ou `DetalheView` além das correções pontuais descritas.

## Decisions

- **FilterBar — vincular `:value` ao nome do tema**: trocar `:value="t"` por `:value="t.nome"` no `<option>` do select de subtema. Alternativa descartada: manter o objeto e extrair `.nome` no momento de emitir o evento — rejeitada por exigir lógica extra em múltiplos pontos do componente quando o fix na origem (o `<option>`) já resolve o problema de forma mínima.
- **StatusBadge — reaproveitar classe de `Arquivado` para `Encerrado`**: adicionar `Encerrado` ao mesmo mapeamento/case que já resolve a cor cinza de `Arquivado`, em vez de criar uma nova classe CSS. Mantém a paleta institucional consistente e evita duplicação de estilo.
- **Código legível da proposição**: usar diretamente `{{ proposicao.sigla_tipo }} {{ proposicao.numero }}/{{ proposicao.ano }}` no template, sem criar um computed/helper novo, já que a formatação é usada em apenas dois pontos (`ProposicaoCard.vue`, `DetalheView.vue`) e não há lógica condicional além da concatenação.

## Risks / Trade-offs

- [Campos `sigla_tipo`/`numero`/`ano` ausentes ou nulos em algum registro legado] → manter fallback visual equivalente ao já existente para outros campos ausentes em `ProposicaoCard` (ex.: exibir vazio/traço em vez de quebrar a renderização).
- [Outros valores de status não mapeados além de `Encerrado`] → fora do escopo desta mudança; não alterar o tratamento padrão/fallback já existente em `StatusBadge`.
