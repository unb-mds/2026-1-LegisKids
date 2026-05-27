## 1. HTML — estrutura e componentes

- [ ] 1.1 Criar `frontend/pages/detalhe-projeto.html` com `<!DOCTYPE>`, fontes Inter/IBM Plex Mono/Cinzel via Google Fonts e `<body class="detalhe-page">`
- [ ] 1.2 Replicar a navbar de `index.html` (mesmas classes, mesmo SVG do logo, mesmo menu Projetos/Alertas/Análises e ícones de configurações/notificações)
- [ ] 1.3 Implementar `.detalhe-topbar` com link "Voltar ao dashboard" (`arrow-left`) e botões "Compartilhar"/"Salvar" (`.btn-outline`)
- [ ] 1.4 Implementar `.projeto-header` com badges (`.badge--id`, `.badge--urgente`, `.badge--topic`), título `<h1>`, subtítulo e `.projeto-header__meta` com 2 `.meta-item` (calendário + balança)
- [ ] 1.5 Implementar `.detalhe-tabs` com 5 botões `role="tab"` (Visão geral ativa, Tramitação, Análise, Documentos, Comentários) e ícones Lucide
- [ ] 1.6 Implementar `.detalhe-grid` com `.detalhe-main` (`role="tabpanel"` para cada aba) e `.detalhe-sidebar` (320px)
- [ ] 1.7 Implementar card "Sobre o projeto" com `.detalhe-card__body.collapsed`, 2 parágrafos do `spec.json.sobre` e `#sobreToggle` "Ver mais"
- [ ] 1.8 Implementar card "Informações pessoais" com `.info-grid` de 4 colunas e 8 `.info-cell` (incluindo uma com `.dot.dot--red` em Urgência)
- [ ] 1.9 Implementar card "Objetivos do projeto" com `.objetivos-list` e 4 `.objetivo-item` (cada um com `.objetivo-check` + SVG check branco)
- [ ] 1.10 Implementar card "Documentos e anexos" com `.doc-list` (3 `.doc-item` com ícone PDF + nome + meta + `.btn-download`) e link "Ver todos os documentos (5)"
- [ ] 1.11 Implementar card "Projetos relacionados" com `.detalhe-card__header` (título + link "Ver todos") e `.relacionados-grid` com 3 `.relacionado-card`
- [ ] 1.12 Implementar sidebar card "Status da tramitação" com `.badge--em-tramitacao`, subtítulo, `.timeline` com 4 `.timeline-item` (done/active/pending/pending) e link "Ver tramitação completa"
- [ ] 1.13 Implementar sidebar card "Análise e indicadores" com `.analise-icon` (book-open), 3 `.indicator` (Relevância 4/5, Impacto social 3/5, Apoio popular 3/5) e link "Ver análise detalhada"
- [ ] 1.14 Implementar sidebar card "Compartilhar" com `.share-header`, subtítulo e 4 `.share-btn` (link, WhatsApp, Twitter, Facebook) com `data-share="<rede>"`
- [ ] 1.15 Replicar o footer de `index.html` (mesma cor de fundo, copyright, links Sobre/Contato/Privacidade)
- [ ] 1.16 Linkar `<script src="../js/detalhe.js">` no final do `<body>`

## 2. CSS — design system e responsividade

- [ ] 2.1 Criar `frontend/css/detalhe.css` com cabeçalho de comentário explicando que herda `style.css` e adiciona apenas estilos exclusivos
- [ ] 2.2 Definir tokens `--d-*` sob `.detalhe-page` (todos os 22 tokens listados no SPEC-detalhe.md §6) e aplicar `background: var(--d-page-bg)` no body
- [ ] 2.3 Estilizar `.detalhe-topbar`, `.detalhe-topbar__back` e `.btn-outline` (incluindo hover)
- [ ] 2.4 Estilizar `.projeto-header`, `.projeto-header__badges`, `.badge`/`.badge--id`/`.badge--urgente`/`.badge--topic`, `.projeto-header__title`, `.projeto-header__subtitle`, `.projeto-header__meta`, `.meta-item`, `.meta-item__label`, `.meta-item__value`
- [ ] 2.5 Estilizar `.detalhe-tabs`, `.detalhe-tab` e `.detalhe-tab--active` com hover, transição e ícones SVG
- [ ] 2.6 Estilizar `.detalhe-grid`, `.detalhe-main`, `.detalhe-sidebar` (flex desktop, column tablet)
- [ ] 2.7 Estilizar `.detalhe-card`, `.detalhe-card__title`, `.detalhe-card__header`, `.detalhe-card__link`, `.detalhe-card__link-right`
- [ ] 2.8 Estilizar `.detalhe-card__body`, `.detalhe-card__body.collapsed`, `.btn-expand`, `.btn-expand--open` (chevron rotaciona 180°)
- [ ] 2.9 Estilizar `.info-grid`, `.info-cell`, `.info-cell__label`, `.info-cell__value`, `.dot`, `.dot--red`, `.dot--gray`
- [ ] 2.10 Estilizar `.objetivos-list`, `.objetivo-item`, `.objetivo-check`
- [ ] 2.11 Estilizar `.doc-list`, `.doc-item`, `.doc-item__icon`, `.doc-item__info`, `.doc-item__name`, `.doc-item__meta`, `.btn-download`
- [ ] 2.12 Estilizar `.relacionados-grid`, `.relacionado-card`, `.relacionado-card__title` (incluindo hover com box-shadow)
- [ ] 2.13 Estilizar `.sidebar-card`, `.sidebar-card__header`, `.sidebar-card__subtitle`, `.sidebar-card__link`
- [ ] 2.14 Estilizar `.timeline`, `.timeline-item`, `.timeline-node` (done/active/pending), `.timeline-line`, `.timeline-content` (title/date/desc) e variante `.timeline-item--active`
- [ ] 2.15 Estilizar `.badge--em-tramitacao`
- [ ] 2.16 Estilizar `.analise-header`, `.analise-icon`, `.indicators`, `.indicator`, `.indicator__labels`, `.indicator__name`, `.indicator__value`, `.indicator__bar`, `.indicator__segment`/`--filled`/`--empty`
- [ ] 2.17 Estilizar `.share-header`, `.share-buttons`, `.share-btn` (incluindo hover)
- [ ] 2.18 Implementar tooltip "Copiado!" (`.share-tooltip`) com estado `.is-visible` e animação fade
- [ ] 2.19 Implementar breakpoint tablet (≤1024px): `.detalhe-grid` empilha, sidebar 100%, `.info-grid` 2 cols, `.relacionados-grid` 2 cols
- [ ] 2.20 Implementar breakpoint mobile (≤640px): topbar em coluna, título 24px, `.relacionados-grid` 1 col, tabs 14px

## 3. JavaScript — mock data e interatividade

- [ ] 3.1 Criar `frontend/js/detalhe.js` em IIFE `(() => { ... })();`
- [ ] 3.2 Definir `MOCK_PROJETO` com os campos `id`, `titulo`, `subtitulo`, `objetivos`, `tramitacao`, `indicadores`, `documentos`, `projetos_relacionados` do `spec.json.mockData`
- [ ] 3.3 Implementar `initTabs()`: query em `.detalhe-tab`, click handler que alterna `.detalhe-tab--active`/`aria-selected`/`tabindex` e mostra `[data-panel="<id>"]` ocultando os demais
- [ ] 3.4 Adicionar suporte de teclado em `initTabs()`: `Enter`/`Space` acionam click; setas ←/→ movem foco entre tabs (roving tabindex)
- [ ] 3.5 Implementar `initSobreToggle()`: click em `#sobreToggle` alterna `.collapsed` em `#sobreBody` e `.btn-expand--open` no botão; troca texto "Ver mais"/"Ver menos"
- [ ] 3.6 Implementar `initShare()`: handlers por `data-share`:
  - `link` → `navigator.clipboard.writeText(window.location.href)` + tooltip "Copiado!" por 2s
  - `whatsapp` → `window.open('https://wa.me/?text=' + encodeURIComponent(titulo + ' — ' + url), '_blank')`
  - `twitter` → `window.open('https://twitter.com/intent/tweet?url=' + encodeURIComponent(url) + '&text=' + encodeURIComponent(titulo), '_blank')`
  - `facebook` → `window.open('https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url), '_blank')`
- [ ] 3.7 Implementar `initSalvar()`: click em `#btnSalvar` alterna classe `.is-saved` no botão e troca atributo `aria-pressed`
- [ ] 3.8 Implementar `initSidebarLinks()`: clicks em "Ver tramitação completa" e "Ver análise detalhada" acionam a tab correspondente programaticamente
- [ ] 3.9 Implementar `initBtnShareTop()`: `#btnShareTop` reaproveita handler de "copiar link"
- [ ] 3.10 Adicionar event listener `DOMContentLoaded` que chama todos os `init*()`

## 4. Integração da página com o app

- [ ] 4.1 Atualizar `frontend/pages/index.html`: trocar `<button class="projeto-btn">Ver Detalhes</button>` por `<a class="projeto-btn" href="detalhe-projeto.html?id=PL-001">Ver Detalhes</a>` (e equivalente para PL-002)
- [ ] 4.2 Garantir que `.projeto-btn` mantém aparência idêntica como `<a>` (adicionar regra `text-decoration:none; display:inline-block` em `style.css` se necessário — verificar primeiro se já funciona)
- [ ] 4.3 Atualizar `frontend/pages/pesquisa.html`/`pesquisa.js`: cards de resultado devem linkar para `detalhe-projeto.html?id=<id-do-resultado>`

## 5. Validação manual

- [ ] 5.1 Abrir `detalhe-projeto.html` em Chrome desktop e validar layout em 2 colunas
- [ ] 5.2 Reduzir para 1024px e validar empilhamento da sidebar
- [ ] 5.3 Reduzir para 640px e 320px e validar ausência de scroll horizontal
- [ ] 5.4 Clicar em cada uma das 5 tabs e confirmar troca de painel
- [ ] 5.5 Clicar "Ver mais" e confirmar expand/recolhe do card "Sobre o projeto"
- [ ] 5.6 Clicar em cada botão de compartilhamento e validar comportamento
- [ ] 5.7 Navegar apenas via `Tab` da navbar até a sidebar e validar foco visível em todos os interativos
- [ ] 5.8 Rodar Lighthouse / axe DevTools e atingir Accessibility ≥ 95
- [ ] 5.9 Confirmar que `index.html` e `pesquisa.html` continuam visualmente idênticos (nada quebrou)

## 6. Integração futura (próximas changes — não nesta)

- [ ] 6.1 Substituir mock data por `fetch('/api/proposicoes/' + id)` quando endpoint Flask estiver disponível
- [ ] 6.2 Implementar persistência real do "Salvar" via OAuth (Release 2)
- [ ] 6.3 Implementar painel de Comentários com dados dinâmicos
- [ ] 6.4 Substituir valores dos indicadores por classificação IA real (Release 2)
- [ ] 6.5 Adicionar modal avançado de compartilhamento ao botão da top bar
