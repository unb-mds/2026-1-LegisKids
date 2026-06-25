---
name: vue-router
description: Use this skill when configuring or editing Vue Router routes, navigation guards, or lazy-loaded views in the LegisKids Vue frontend. Triggers on router/index.js, createRouter, route definitions, router-link/router-view, or navigation guards (beforeEach). For the auth state checked inside a guard, also consult pinia-state.
---

# Vue Router — LegisKids

## Estrutura de rotas

```javascript
// router/index.js
import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes = [
  {
    path: "/",
    name: "inicio",
    component: () => import("@/views/InicioView.vue"),
  },
  {
    path: "/proposicoes",
    name: "proposicoes",
    component: () => import("@/views/ProposicoesView.vue"),
  },
  {
    path: "/proposicoes/:id",
    name: "proposicao-detalhe",
    component: () => import("@/views/ProposicaoDetalheView.vue"),
    props: true,
  },
  {
    path: "/perfil",
    name: "perfil",
    component: () => import("@/views/PerfilView.vue"),
    meta: { requerAutenticacao: true },
  },
  {
    path: "/:pathMatch(.*)*",
    name: "nao-encontrado",
    component: () => import("@/views/NaoEncontradoView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((para, _de) => {
  const authStore = useAuthStore();
  if (para.meta.requerAutenticacao && !authStore.estaAutenticado) {
    return { name: "inicio", query: { redirecionarPara: para.fullPath } };
  }
});

export default router;
```

Pontos importantes:
- **Lazy loading** (`component: () => import(...)`) em toda rota, exceto talvez a inicial — cada view só é baixada quando o usuário navega até ela, reduzindo o bundle inicial.
- Rota catch-all (`/:pathMatch(.*)*`) sempre por último, para uma página 404 amigável em vez de tela em branco.
- `props: true` em rotas com parâmetro (`:id`) para receber o parâmetro diretamente como prop no componente, em vez de acessar `route.params.id` manualmente em todo componente.
- `meta.requerAutenticacao` + guard global (`beforeEach`) centraliza a regra de proteção de rota em um único lugar, em vez de repetir a checagem dentro de cada componente protegido.

## Navegação programática

```javascript
import { useRouter } from "vue-router";

const router = useRouter();

function abrirDetalhe(id) {
  router.push({ name: "proposicao-detalhe", params: { id } });
}
```

Prefira navegar por `name` + `params`/`query` (rotas nomeadas) em vez de montar a string da URL manualmente (`router.push("/proposicoes/" + id)`) — assim, se o `path` mudar no futuro, só precisa atualizar em um lugar.

## `<router-link>` no template

```vue
<router-link :to="{ name: 'proposicao-detalhe', params: { id: proposicao.id } }">
  {{ proposicao.titulo }}
</router-link>
```

## Acessando parâmetros e query string

```javascript
import { useRoute } from "vue-router";
import { watch } from "vue";

const route = useRoute();

watch(
  () => route.params.id,
  (novoId) => carregarProposicao(novoId),
  { immediate: true }
);
```

Use `watch` sobre `route.params`/`route.query` (não apenas `onMounted`) quando o componente pode ser reaproveitado para IDs diferentes sem ser destruído/recriado (ex.: navegar de `/proposicoes/1` para `/proposicoes/2` reaproveita a mesma instância do componente).

## Checklist

1. Todas as views carregadas via lazy import.
2. Rotas nomeadas, navegação feita por nome + params, não por string concatenada.
3. Proteção de rotas autenticadas centralizada em um guard global (`beforeEach`), usando a store de auth.
4. Rota catch-all 404 definida por último.
5. Mudança de parâmetro de rota tratada com `watch`, não só `onMounted`, quando o componente pode ser reaproveitado.
