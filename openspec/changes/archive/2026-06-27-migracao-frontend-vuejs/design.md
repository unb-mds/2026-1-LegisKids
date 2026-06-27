## Context

O LegisKids possui atualmente um frontend planejado em HTML5/CSS3/JS puro (conforme `CLAUDE.md` e o estudo `docs/estudos/frontend/tecnologias_estrutura.md`), mas ainda sem implementação real na pasta `frontend/`. O backend Flask em `backend/src/` já expõe endpoints REST que retornam JSON. A identidade visual foi definida no Figma com paleta institucional, fontes Cinzel/Inter e design system de componentes.

O estudo técnico em `docs/estudos/frontend/frameworks_bibliotecas.md` avaliou React, Vue.js, Svelte, Alpine.js, HTMX, Tailwind, Bootstrap, Chart.js, D3 e ApexCharts com os critérios: compatibilidade com Flask, curva de aprendizado da equipe, escalabilidade para Release 2 e compatibilidade com o design system existente.

## Goals / Non-Goals

**Goals:**
- Scaffoldar o frontend como projeto Vue 3 + Vite desde o início (sem legado vanilla para migrar)
- Estabelecer estrutura de componentes, roteamento e estado que suporte Release 1 e Release 2 sem reescrita
- Integrar Chart.js para os gráficos especificados nas US11, US12, US13, US14
- Preservar 100% da identidade visual do Figma (variáveis CSS, fontes, paleta)
- Manter Flask como API REST pura — sem templates Jinja nem endpoints que retornem HTML

**Non-Goals:**
- Autenticação (Release 2 — US19/US20/US21)
- Integração com IA/Gemini no frontend (Release 2)
- SSR (Server-Side Rendering) ou nuxt
- Adoção de Tailwind, Bootstrap ou qualquer outro framework CSS

## Decisions

### D1: Vue 3 com Composition API e `<script setup>`
**Decisão:** Usar Vue 3 com Composition API e a sintaxe `<script setup>` (açúcar sintático).
**Razão:** `<script setup>` é o padrão recomendado no Vue 3, produz menos boilerplate que Options API e é o que a documentação oficial e comunidade adotam. A equipe parte de JS puro — a Composition API é mais próxima de funções JS simples do que a Options API é de classes.
**Alternativa descartada:** Options API — sintaxe mais próxima do Vue 2, mas a documentação oficial recomenda Composition API para projetos novos.

### D2: Vite como bundler
**Decisão:** Usar Vite (scaffolding padrão `npm create vue@latest`).
**Razão:** É a ferramenta padrão do ecossistema Vue 3. HMR (Hot Module Replacement) instantâneo, build otimizado com Rollup, suporte nativo a ES modules. Sem configuração manual.
**Alternativa descartada:** Webpack — configuração manual pesada, sem vantagem para este projeto.

### D3: Vue Router 4 para roteamento client-side
**Decisão:** Vue Router 4 (oficial do Vue 3) para navegação entre páginas sem reload.
**Razão:** É a solução oficial do ecossistema Vue. Modo `history` (HTML5) para URLs limpas. O Flask precisa servir `index.html` para qualquer rota em produção (fallback SPA).
**Rotas definidas:**
- `/` — Dashboard principal (US13, US14)
- `/busca` — Busca e filtros (US08, US09, US10)
- `/proposicao/:id` — Detalhes da proposição (US15)

### D4: Pinia para estado global
**Decisão:** Pinia (gerenciador de estado oficial do Vue 3).
**Razão:** Pinia substituiu Vuex como solução oficial, é mais simples, TypeScript-friendly e sem mutations boilerplate. Estado necessário: filtros de busca ativos, página atual na paginação, lista de proposições carregadas.
**Alternativa descartada:** Vuex — mais verboso, não é mais recomendado para projetos novos.

### D5: Chart.js 4 para gráficos
**Decisão:** Chart.js 4 importado via npm (não CDN).
**Razão:** O estudo técnico concluiu que os gráficos especificados (barras, linhas, pizza/rosca) são convencionais e não exigem as capacidades avançadas do D3. Chart.js tem API simples, integração trivial com Fetch e comunidade madura (63k+ stars).
**Alternativa descartada:** ApexCharts — bundle maior (~500KB vs ~200KB), comunidade menor. D3.js — curva altíssima de aprendizado, desproporcional para gráficos padrão.

### D6: CSS próprio preservado via variáveis globais
**Decisão:** Manter o design system da equipe (variáveis CSS `--primary`, `--bg`, fontes Cinzel/Inter) como arquivo global importado no `src/assets/main.css`.
**Razão:** A identidade visual foi investida no Figma e nas variáveis CSS existentes. Substituir por Tailwind ou Bootstrap implicaria reescrever toda a estilização sem ganho real.
**Cada componente `.vue` usa `<style scoped>`** para estilos específicos, e as variáveis globais ficam disponíveis em todos os componentes via cascade do CSS.

### D7: Comunicação com Flask via Fetch API em services
**Decisão:** Encapsular todas as chamadas ao backend em módulos `src/services/*.js` (sem bibliotecas como axios).
**Razão:** A Fetch API nativa é suficiente. Encapsular em services separa a lógica de dados dos componentes, facilita mock em testes e centraliza o tratamento de erros.
**Estrutura:**
```
src/services/
  proposicoes.js   // GET /api/proposicoes, GET /api/proposicoes/:id
  temas.js         // GET /api/temas
  estatisticas.js  // GET /api/estatisticas
```

## Risks / Trade-offs

**[Risco] Equipe nunca usou Vue** → A curva de aprendizado existe, mas Vue 3 com `<script setup>` é a mais suave entre os frameworks SPA. A documentação oficial em português é de alta qualidade. Mitigação: scaffoldar componentes-padrão como exemplos na primeira task.

**[Risco] CORS entre Vite (porta 5173) e Flask (porta 5000)** → Flask precisa de `flask-cors` configurado para `http://localhost:5173` em desenvolvimento. Em produção, ambos servidos na mesma origem (build estático servido pelo Flask ou Nginx). Mitigação: documentar no README e nas variáveis de ambiente.

**[Risco] Build step necessário para produção** → Diferente de arquivos HTML estáticos, o Vue exige `npm run build` gerando a pasta `dist/`. Mitigação: adicionar step de build no GitHub Actions CI.

**[Trade-off] Bundle size maior que vanilla** → O bundle do Vue 3 + Chart.js em produção é ~150-300KB gzipped. Para uma aplicação de governo/institucional com usuários em desktop, isso é aceitável.

## Migration Plan

1. Criar estrutura Vite/Vue em `frontend/` via `npm create vue@latest`
2. Implementar componentes de UI base (Navbar, Card, Badge, Spinner)
3. Configurar Vue Router com as 3 rotas principais
4. Configurar Pinia com as stores necessárias
5. Implementar páginas: Dashboard → Busca → Detalhes
6. Integrar Chart.js nos componentes de gráficos
7. Configurar CORS no Flask para localhost:5173
8. Adicionar step de build no CI
9. Atualizar `CLAUDE.md` e `README.md` com novos comandos

**Rollback:** Como não há legado vanilla implementado, não há rollback — o scaffold Vue é a primeira implementação real.

## Open Questions

- O Flask em produção vai servir o `dist/` do Vue ou haverá Nginx na frente? (Impacta configuração de fallback SPA para Vue Router no modo history)
- O `package.json` do frontend fica em `frontend/package.json` ou na raiz do repositório? (Recomendação: `frontend/package.json` para isolamento)
