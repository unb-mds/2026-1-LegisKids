---
name: pinia-state
description: Use this skill when creating or editing Pinia stores in the LegisKids Vue frontend — global state for auth/user session, proposições cache, or any defineStore() usage. Triggers on "store", "Pinia", defineStore, or state shared across multiple Vue components. For local component state, prefer plain ref/reactive inside the component instead (see vuejs-frontend) — only reach for Pinia when state must be shared across unrelated components.
---

# Pinia — Estado Global do LegisKids

## Quando usar Pinia vs. estado local

Use uma store Pinia apenas para estado que precisa ser compartilhado entre componentes não relacionados por props/emits diretos: sessão do usuário autenticado, filtros de busca persistidos entre páginas, cache de proposições já carregadas. Para estado que só importa a um componente e seus filhos diretos, prefira `ref`/composables locais (ver skill `vuejs-frontend`) — Pinia para tudo é complexidade desnecessária.

## Store de autenticação

```javascript
// stores/auth.js
import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("token_app") || null);
  const usuario = ref(null);

  const estaAutenticado = computed(() => token.value !== null);

  function definirSessao({ token: novoToken, usuario: dadosUsuario }) {
    token.value = novoToken;
    usuario.value = dadosUsuario;
    localStorage.setItem("token_app", novoToken);
  }

  function sair() {
    token.value = null;
    usuario.value = null;
    localStorage.removeItem("token_app");
  }

  return { token, usuario, estaAutenticado, definirSessao, sair };
});
```

Usando a sintaxe "setup stores" (function-based) em vez da sintaxe de objeto Options — é mais consistente com `<script setup>` no resto do projeto e dá mais flexibilidade para composição.

## Store de proposições (cache + filtros)

```javascript
// stores/proposicoes.js
import { defineStore } from "pinia";
import { ref } from "vue";
import { buscarProposicoes } from "@/services/api";

export const useProposicoesStore = defineStore("proposicoes", () => {
  const itens = ref([]);
  const carregando = ref(false);
  const erro = ref(null);
  const filtros = ref({ tema: "", pagina: 1 });

  async function carregar() {
    carregando.value = true;
    erro.value = null;
    try {
      const { data } = await buscarProposicoes(filtros.value);
      itens.value = data;
    } catch (e) {
      erro.value = e;
    } finally {
      carregando.value = false;
    }
  }

  function atualizarFiltro(novoFiltro) {
    filtros.value = { ...filtros.value, ...novoFiltro, pagina: 1 };
    carregar();
  }

  return { itens, carregando, erro, filtros, carregar, atualizarFiltro };
});
```

## Usando a store em um componente

```vue
<script setup>
import { onMounted } from "vue";
import { useProposicoesStore } from "@/stores/proposicoes";

const store = useProposicoesStore();
onMounted(store.carregar);
</script>

<template>
  <p v-if="store.carregando">Carregando...</p>
  <ul v-else>
    <li v-for="p in store.itens" :key="p.id">{{ p.titulo }}</li>
  </ul>
</template>
```

Não use `mapState`/destructuring direto que quebre a reatividade (`const { itens } = store` perde reatividade); acesse via `store.itens` no template, ou use `toRefs(store)` se realmente precisar desestruturar em `<script setup>`.

## Persistência

Para estado que deve sobreviver a reload de página (sessão, preferências), persista explicitamente em `localStorage` dentro das actions da store (como no exemplo de `auth.js`), ou adote o plugin `pinia-plugin-persistedstate` se o projeto crescer e isso se repetir em várias stores.

## Organização

- Uma store por domínio (`auth`, `proposicoes`, `temas`) — não crie uma store gigante "app" com tudo dentro.
- Nomeie a store com o mesmo nome do arquivo (`useAuthStore` em `stores/auth.js`) para facilitar localização.

## Checklist

1. Pinia reservado para estado realmente compartilhado entre partes não relacionadas da árvore de componentes.
2. Uma store por domínio, não uma store global única.
3. Estados de carregando/erro tratados dentro da própria store quando ela faz chamadas assíncronas.
4. Persistência em `localStorage` feita explicitamente nas actions, não direto nos componentes.
5. Acesso reativo ao estado da store sem desestruturação que quebre a reatividade.
