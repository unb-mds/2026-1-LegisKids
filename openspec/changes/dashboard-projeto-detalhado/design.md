## Context

O frontend do LegisKids é HTML + CSS + JavaScript puro (sem framework, sem build). O `dashboard-principal` (`index.html`) e o `dashboard-pesquisa` (`pesquisa.html`) já estão implementados e ambos herdam os tokens globais definidos em `frontend/css/style.css` (`:root` com `--primary #2563EB`, `--bg #F1F5F9`, etc.). A tela de detalhes é a terceira página principal, ponto de chegada do fluxo `dashboard → pesquisa → detalhe`.

O spec visual está em `specs/spec.json` (paleta navy `#2B3FBF`, fundo `#DDE3EE`, badges urgente/topic/tramitação, timeline vertical, barras segmentadas) e em `specs/SPEC-detalhe.md` (decomposição em componentes BEM, requisitos OpenSpec, critérios de aceitação). O princípio arquitetural é que **o frontend nunca acessa a API da Câmara diretamente** — todos os dados vêm do backend Flask via Fetch API. Nesta change, os dados são mock; a estrutura já está pronta para substituição por `fetch('/api/proposicoes/<id>')`.

## Goals / Non-Goals

**Goals:**
- Reproduzir fielmente os componentes do `spec.json`: top bar, project header, tabs, cards principais (Sobre, Informações pessoais, Objetivos, Documentos, Projetos relacionados) e sidebar (Status da tramitação, Análise e indicadores, Compartilhar).
- Encapsular a paleta navy da página em tokens `--d-*` sob `.detalhe-page`, sem modificar `style.css`.
- Reutilizar integralmente a navbar e o footer já existentes em `style.css` (zero duplicação).
- Implementar todas as interações: troca de tabs com `aria-selected`, expand/colapse do "Sobre o projeto", cópia de link, share WhatsApp/Twitter/Facebook, toggle visual de "Salvar".
- Garantir acessibilidade WCAG AA: contraste, navegação por teclado, foco visível, `role=tablist`/`role=tab`/`role=tabpanel`.
- Responsividade até 320px sem scroll horizontal.

**Non-Goals:**
- Integração real com backend (`/api/proposicoes/<id>`) — fica para task subsequente da Release 1.
- Persistência do "Salvar" como favorito — requer autenticação (Release 2).
- Conteúdo dinâmico da aba "Comentários" — placeholder vazio nesta entrega.
- Geração via IA dos indicadores (Relevância, Impacto social, Apoio popular) — Release 2.
- Modal de compartilhamento avançado no `btnShareTop` — MVP usa "copiar link".

## Decisions

### 1. Tokens locais `--d-*` escopados em `.detalhe-page`

**Decisão:** A paleta divergente do `spec.json` (navy `#2B3FBF` vs. indigo `#2563EB` do dashboard) é definida como tokens locais com prefixo `--d-` dentro do seletor `.detalhe-page`. `style.css` permanece intocado.

**Rationale:** Evita conflito visual entre as três páginas (cada uma com sua identidade dentro do mesmo sistema), mantém `:root` global limpo, e permite que mudanças globais (ex.: novo tipo de letra) ainda se propaguem.

### 2. Reuso da navbar e footer via cópia de markup

**Decisão:** Copiar o markup completo de navbar e footer de `index.html` (mesmas classes `.navbar`, `.icon-btn`, `.footer`). Não há sistema de includes/templates no projeto.

**Rationale:** É o padrão já adotado em `pesquisa.html` e é a única forma viável sem build/SSR. Trade-off conhecido: duplicação de markup; mitigado por nunca duplicar estilos.

### 3. Body com classe `.detalhe-page` (padrão de `pesquisa-page`)

**Decisão:** `<body class="detalhe-page">` ativa tanto a paleta local quanto o background `--d-page-bg`.

**Rationale:** Consistente com `pesquisa.html` e mantém escopo de seletores em `detalhe.css` sob esse prefixo, garantindo zero vazamento para outras páginas.

### 4. Tabs estáticas (todos os painéis no DOM, ocultos via `hidden`)

**Decisão:** Os 5 painéis ficam todos no DOM; troca de aba apenas alterna o atributo `hidden`.

**Rationale:** Simplicidade — sem rotas hash, sem lazy-load. Para uma tela de leitura, o custo extra de DOM é irrelevante. Quando backend estiver disponível, cada painel pode ser populado por uma chamada distinta sem mudar a estrutura.

### 5. Compartilhamento via deeplinks padrão das redes

**Decisão:** WhatsApp (`wa.me/?text=`), Twitter (`twitter.com/intent/tweet`) e Facebook (`facebook.com/sharer/sharer.php`) abertos via `window.open(url, '_blank')`. "Copiar link" usa `navigator.clipboard.writeText()`.

**Rationale:** Padrão da indústria, sem SDKs externos, funciona em todos os browsers modernos. Fallback de `clipboard` (browsers antigos) sai do escopo desta change.

### 6. Mock data inline no HTML + mirror no JS

**Decisão:** Os valores do `mockData.projeto` do `spec.json` ficam diretamente no HTML estático (mais simples de revisar visualmente). O `detalhe.js` mantém `MOCK_PROJETO` como referência, mas a renderização dinâmica só será necessária quando o backend estiver pronto.

**Rationale:** Render dinâmico exige sanitização (escapeHtml), template strings e DOM building — overhead desnecessário com dados estáticos. Em contraste, `pesquisa.js` precisava de render dinâmico para filtros/ordenação/paginação.

### 7. Botão "Salvar" sem persistência

**Decisão:** Clicar em `#btnSalvar` apenas alterna a classe `.is-saved` (visual: ícone bookmark preenchido).

**Rationale:** Sem autenticação no Release 1, persistir favoritos em `localStorage` criaria expectativa errada (perde no logout/troca de device). O comportamento visual já demonstra a intenção; persistência real virá com OAuth (Release 2).

## Risks / Trade-offs

- **Duplicação de navbar/footer entre 3 páginas:** sem templating, qualquer mudança na navbar precisa ser propagada manualmente. Mitigado mantendo o markup idêntico e centralizando os estilos em `style.css`.
- **Paleta divergente entre páginas pode parecer inconsistente:** o `spec.json` da tela de detalhe usa navy mais escuro; outras páginas usam indigo. É decisão de design do Figma. Mitigado escopando os tokens em `.detalhe-page` e mantendo navbar/footer com a paleta global.
- **Mock data inline no HTML:** quando o backend chegar, será preciso refatorar o HTML para template + render via JS. Tradeoff aceito por simplicidade nesta fase.
- **Aba "Comentários" vazia:** vai entregar um painel placeholder visível. Solução: exibir uma mensagem "Em breve" centralizada no painel correspondente para não parecer bug.

## Migration Plan

1. Criar os 3 arquivos novos (`detalhe-projeto.html`, `detalhe.css`, `detalhe.js`) com mock data. *(esta change)*
2. Atualizar links em `index.html` e `pesquisa.html`. *(esta change)*
3. Quando o backend Flask tiver `/api/proposicoes/<id>`, substituir os valores estáticos do HTML por placeholders e popular via `detalhe.js` lendo `?id=` da URL.
4. Quando autenticação estiver disponível (Release 2), conectar `#btnSalvar` ao endpoint de favoritos.
5. Quando IA estiver classificando (Release 2), substituir os valores dos indicadores por dados reais.
6. Quando endpoint de comentários existir, popular a aba homônima.

## Open Questions

- O título da página no `<title>` deve incluir o ID do projeto (`PL-2654/2026`) dinamicamente quando vier do backend?
- O share do Twitter deve incluir hashtags fixas (`#LegisKids #ProteçãoInfantilDigital`)?
- "Ver tramitação completa" e "Ver análise detalhada" devem navegar para uma URL distinta ou apenas trocar a aba? Esta change assume a segunda opção.
- O botão "Compartilhar" da top bar deve abrir um modal (mais opções) ou repetir a ação de "Copiar link"? MVP assume cópia.
