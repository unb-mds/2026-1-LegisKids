---
name: vuejs-frontend
description: Use this skill when working on Vue.js components (.vue Single File Components, Composition API, props/emits, computed/watch) in the LegisKids frontend. Triggers on .vue files, <script setup>, ref/reactive, defineProps/defineEmits, or discussion of Vue components/composables. For routing use vue-router, for global state use pinia-state, for the build tool use vite-build, and for plain HTML/JS pages without Vue use vanilla-frontend.
---

# Vue.js — Frontend do LegisKids

## Composition API com `<script setup>`

Padrão recomendado para todo componente novo — mais conciso e com melhor inferência de tipos que a Options API:

```vue
<script setup>
import { ref, computed, onMounted } from "vue";
import { buscarProposicoes } from "@/services/api";

const proposicoes = ref([]);
const carregando = ref(false);
const erro = ref(null);
const tema = ref("");

const totalEncontrado = computed(() => proposicoes.value.length);

async function buscar() {
  carregando.value = true;
  erro.value = null;
  try {
    const { data } = await buscarProposicoes({ tema: tema.value });
    proposicoes.value = data;
  } catch (e) {
    erro.value = "Não foi possível carregar as proposições.";
  } finally {
    carregando.value = false;
  }
}

onMounted(buscar);
</script>

<template>
  <section>
    <form @submit.prevent="buscar">
      <label for="tema">Tema</label>
      <input id="tema" v-model="tema" type="text" />
      <button type="submit" :disabled="carregando">Buscar</button>
    </form>

    <p v-if="carregando">Carregando...</p>
    <p v-else-if="erro" role="alert">{{ erro }}</p>
    <p v-else-if="totalEncontrado === 0">Nenhuma proposição encontrada.</p>
    <ul v-else>
      <li v-for="proposicao in proposicoes" :key="proposicao.id">
        {{ proposicao.titulo }} — {{ proposicao.status }}
      </li>
    </ul>
  </section>
</template>
```

Sempre trate os três estados de uma chamada assíncrona: carregando, erro, vazio — não apenas o "caminho feliz" com dados.

## Props e emits explícitos

```vue
<script setup>
const props = defineProps({
  proposicao: { type: Object, required: true },
});

const emit = defineEmits(["selecionar"]);

function aoClicar() {
  emit("selecionar", props.proposicao.id);
}
</script>
```

Nunca mute uma prop diretamente (`props.proposicao.titulo = "..."`) — props são somente leitura no componente filho. Se precisar de estado local editável derivado de uma prop, copie para um `ref` próprio.

## Componentização

Separe por responsabilidade, evitando componentes "deus" de centenas de linhas:
- `ProposicaoCard.vue` — exibição de um item.
- `ProposicaoLista.vue` — orquestra a lista, paginação, e estados de carregamento.
- `BuscaFiltro.vue` — formulário de busca/filtros.
- `composables/useProposicoes.js` — lógica reutilizável de busca/paginação extraída em uma composable.

Exemplo de composable:

```javascript
// composables/useProposicoes.js
import { ref } from "vue";
import { buscarProposicoes } from "@/services/api";

export function useProposicoes() {
  const proposicoes = ref([]);
  const carregando = ref(false);
  const erro = ref(null);

  async function carregar(params) {
    carregando.value = true;
    erro.value = null;
    try {
      const { data } = await buscarProposicoes(params);
      proposicoes.value = data;
    } catch (e) {
      erro.value = e;
    } finally {
      carregando.value = false;
    }
  }

  return { proposicoes, carregando, erro, carregar };
}
```

Extraia para uma composable sempre que a mesma lógica de busca/estado for usada em mais de um componente — evita duplicação e facilita testes unitários isolados de UI.

## `computed` vs `watch`

- Use `computed` quando o valor é **derivado** de outro estado de forma síncrona (ex.: `totalEncontrado`, `proposicoesFiltradas`).
- Use `watch`/`watchEffect` apenas quando precisar de um **efeito colateral** (chamar API, atualizar `localStorage`) em reação a uma mudança — não para apenas calcular um valor.

```javascript
import { watch } from "vue";

watch(tema, (novoTema) => {
  if (novoTema.length >= 3) buscar();
});
```

## Performance

- Sempre forneça `:key` único e estável (id do banco, não índice do array) em `v-for`.
- Use `v-show` para alternâncias frequentes de visibilidade e `v-if` para condições que raramente mudam ou que devem evitar montar o componente.
- Evite computeds caros recalculando em cada render sem necessidade — se o cálculo for pesado, considere memoização ou mover para o backend.

## Checklist

1. `<script setup>` com Composition API em componentes novos.
2. Estados de carregando/erro/vazio tratados explicitamente.
3. Props nunca mutadas diretamente; comunicação para o pai via `emit`.
4. Lógica reutilizável extraída em composables, não duplicada entre componentes.
5. `:key` estável em todo `v-for`.
