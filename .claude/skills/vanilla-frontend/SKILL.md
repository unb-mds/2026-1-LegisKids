---
name: vanilla-frontend
description: Use this skill when working on plain HTML/CSS/JavaScript pages in the LegisKids frontend that do not use Vue — static pages, the Fetch API integration with the Flask backend, DOM manipulation, accessibility, and responsive CSS without a framework or build step. Triggers on .html files, vanilla <script> blocks, fetch() calls, or CSS file edits outside a Vue SFC. If the file is a .vue component or uses Vue's reactivity (ref/reactive/Composition API), use vuejs-frontend instead.
---

# HTML/CSS/JS Vanilla — LegisKids

## Quando usar vanilla vs. Vue

O projeto tem partes em HTML/CSS/JS puro (provavelmente páginas institucionais, landing page, protótipo inicial) e partes em Vue (interatividade mais rica). Antes de adicionar JS a uma página, confirme se ela já é ou vai ser migrada para um componente Vue — não duplique lógica de fetch entre as duas abordagens.

## Estrutura HTML semântica

Use elementos semânticos em vez de `<div>` genérico para tudo — ajuda acessibilidade e SEO da página institucional:

```html
<main>
  <section aria-labelledby="titulo-busca">
    <h2 id="titulo-busca">Buscar proposições</h2>
    <form id="form-busca" role="search">
      <label for="campo-tema">Tema</label>
      <input id="campo-tema" name="tema" type="text" autocomplete="off" />
      <button type="submit">Buscar</button>
    </form>
  </section>
  <section aria-live="polite" id="resultados"></section>
</main>
```

- `aria-live="polite"` na região de resultados para leitores de tela anunciarem atualizações dinâmicas.
- `<label for>` sempre associado ao `id` do input.

## Consumindo a API Flask com Fetch

Centralize as chamadas de API em um único módulo, não espalhe `fetch()` cru por toda a página:

```javascript
// js/api.js
const API_BASE_URL = "/api";

async function buscarProposicoes({ pagina = 1, tema } = {}) {
  const params = new URLSearchParams({ pagina });
  if (tema) params.set("tema", tema);

  const resposta = await fetch(`${API_BASE_URL}/proposicoes?${params}`);
  if (!resposta.ok) {
    throw new Error(`Erro ${resposta.status} ao buscar proposições`);
  }
  return resposta.json();
}

export { buscarProposicoes };
```

```javascript
// js/busca.js
import { buscarProposicoes } from "./api.js";

const form = document.getElementById("form-busca");
const resultados = document.getElementById("resultados");

form.addEventListener("submit", async (evento) => {
  evento.preventDefault();
  const tema = form.elements.tema.value.trim();

  resultados.textContent = "Carregando...";
  try {
    const { data } = await buscarProposicoes({ tema });
    renderizarResultados(data);
  } catch (erro) {
    resultados.textContent = "Não foi possível carregar os resultados.";
    console.error(erro);
  }
});

function renderizarResultados(proposicoes) {
  resultados.innerHTML = "";
  if (proposicoes.length === 0) {
    resultados.textContent = "Nenhuma proposição encontrada.";
    return;
  }

  const lista = document.createElement("ul");
  for (const proposicao of proposicoes) {
    const item = document.createElement("li");
    item.textContent = `${proposicao.titulo} — ${proposicao.status}`;
    lista.appendChild(item);
  }
  resultados.appendChild(lista);
}
```

Pontos importantes:
- Use `<script type="module">` para poder usar `import`/`export` nativamente, sem bundler.
- Sempre trate o caso de erro de rede/HTTP e o caso de "lista vazia" — nunca deixe a UI em estado indefinido.
- Nunca construa HTML por concatenação de string com dados do usuário/API sem sanitização (`innerHTML = "<li>" + dado + "</li>"` é vetor de XSS); prefira `textContent` ou `createElement`, como no exemplo acima.

## CSS responsivo sem framework

Mobile-first com variáveis CSS para manter consistência visual entre páginas:

```css
:root {
  --cor-primaria: #1d4ed8;
  --cor-texto: #1f2937;
  --espacamento: 1rem;
  --raio-borda: 0.5rem;
}

body {
  margin: 0;
  font-family: system-ui, sans-serif;
  color: var(--cor-texto);
}

.container {
  width: 100%;
  max-width: 1100px;
  margin-inline: auto;
  padding-inline: var(--espacamento);
}

@media (min-width: 768px) {
  .grid-proposicoes {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--espacamento);
  }
}
```

- Defina variáveis de cor/espaçamento uma vez em `:root` e reuse — facilita manter consistência visual com o que for migrado depois para Vue.
- Use `clamp()` para tipografia fluida em vez de múltiplos `@media` só para `font-size`.

## Performance e boas práticas

- `<script type="module" src="js/busca.js" defer></script>` no final do `<head>` ou `<body>` — `defer` evita bloquear o parsing do HTML.
- Otimize imagens (formato `webp`, `loading="lazy"` em imagens fora da viewport inicial).
- Evite manipular o DOM em loop sem batching; quando precisar inserir muitos itens, monte em um `DocumentFragment` antes de anexar ao DOM real.

## Checklist

1. HTML semântico, labels associadas a inputs, `aria-live` em regiões dinâmicas.
2. Chamadas de API centralizadas em um módulo, com tratamento de erro e estado vazio.
3. Inserção de dados externos no DOM via `textContent`/`createElement`, nunca `innerHTML` com dado não sanitizado.
4. CSS com variáveis reutilizáveis e abordagem mobile-first.
5. Scripts carregados como `type="module"` com `defer`.
