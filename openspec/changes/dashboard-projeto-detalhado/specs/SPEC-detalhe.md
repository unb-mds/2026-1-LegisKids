# SPEC — Tela de Detalhes de Projeto de Lei (`detalhe-projeto.html`)

> Spec de implementação derivada de `openspec/changes/dashboard-projeto-detalhado/spec.json` (fonte oficial de design) e alinhada às convenções de `frontend/pages/index.html` + `frontend/css/style.css`.

---

## 1. Objetivo

Implementar a página de detalhes de um Projeto de Lei (`PL-XXXX/YYYY`) seguindo o protótipo Figma, consumindo (via Fetch API, em etapa posterior) o endpoint `/api/proposicoes/<id>` do backend Flask. A tela deve apresentar, em layout de duas colunas no desktop:

- **Coluna principal**: cabeçalho do projeto, abas de seção, "Sobre o projeto", "Informações pessoais", "Objetivos do projeto", "Documentos e anexos" e "Projetos relacionados".
- **Coluna lateral**: "Status da tramitação" (timeline), "Análise e indicadores" (barras segmentadas) e "Compartilhe este projeto".

Atende às user stories **US15 (tela de detalhes)** e parcialmente **US17 (responsividade WCAG AA)** da Release 1.

---

## 2. Contexto

- A página é parte do Release 1 (frontend consome backend, sem IA, sem autenticação, sem favoritos persistentes por usuário).
- Existem hoje `index.html` (dashboard) e `pesquisa.html` (resultados). A tela de detalhes é o terceiro fluxo principal.
- O design system do projeto vive em `frontend/css/style.css` via tokens `:root` (`--primary`, `--bg`, `--card`, etc.). O `spec.json` introduz uma paleta de detalhe (navy `#2B3FBF`, fundo `#DDE3EE`, badges roxa/verde/azul) específica desta página.
- O fluxo de implementação segue OpenSpec: este arquivo é o `spec.md` que dá origem ao `proposal.md`, `design.md` e `tasks.md` da mudança `dashboard-projeto-detalhado`.

---

## 3. Escopo

### Dentro do escopo
- Estrutura HTML5 semântica de `detalhe-projeto.html`.
- Estilos em `frontend/css/detalhe.css` (importa `style.css` para reuso de navbar/footer/tokens base e adiciona estilos próprios).
- Lógica em `frontend/js/detalhe.js` para: troca de abas, expandir/recolher "Sobre o projeto", copiar link, compartilhamento social, navegação por teclado.
- Mock data inline (objeto `MOCK_PROJETO` em `detalhe.js`) até integração com backend.
- Ícones inline SVG no padrão Lucide (stroke 2, linecap round) — sem dependência externa.
- Responsividade desktop / tablet / mobile.

### Fora do escopo
- Integração real com `/api/proposicoes/:id` (vira tarefa subsequente).
- Botão **Salvar** funcional (depende de autenticação — R2).
- Aba **Comentários** com conteúdo dinâmico (placeholder vazio nesta entrega).
- Análise IA dos indicadores (valores virão mockados; geração via IA é R2).
- Modificações em `index.html`/`pesquisa.html` além de adicionar o link de navegação.

---

## 4. Arquivos afetados

| Arquivo | Ação | Notas |
|---|---|---|
| `frontend/pages/detalhe-projeto.html` | **Criar** | Página principal |
| `frontend/css/detalhe.css` | **Criar** | Estilos específicos; usa tokens de `style.css` |
| `frontend/js/detalhe.js` | **Criar** | Lógica de UI (tabs, expand, share) |
| `frontend/pages/index.html` | **Editar** | Linkar `Ver Detalhes` para `detalhe-projeto.html?id=...` |
| `frontend/pages/pesquisa.html` | **Editar** | Linkar resultados da busca para a página de detalhes |

Reutilizar **navbar** e **footer** copiando o markup de `index.html` (mesmas classes `.navbar`, `.footer`, `.icon-btn`, etc.). Nenhum estilo de navbar deve ser duplicado em `detalhe.css`.

---

## 5. Convenções herdadas (obrigatórias)

### 5.1 CSS
- **Tokens em `:root`** já existentes (`--primary #2563EB`, `--bg #F1F5F9`, `--card`, `--text-primary`, `--text-secondary`, `--text-caption`, `--radius`, `--shadow`, `--transition`, `--gap`). Reusar onde aplicável.
- **Nomenclatura BEM**: `.bloco`, `.bloco__elemento`, `.bloco--modificador` (vide `.projeto-card`, `.projeto-card__header`, `.projeto-status--urgente`).
- **Sem CSS inline** salvo casos isolados de cor de fundo de ícone (precedente em `index.html`: `style="background:#DBEAFE"`).
- **Sem !important.**
- Espaçamentos múltiplos de 4px.
- Sombras: `var(--shadow)` para card padrão, `var(--shadow-hover)` em hover.
- Transições: `var(--transition)` (`0.2s ease`).

### 5.2 HTML
- `<!DOCTYPE html>`, `lang="pt-BR"`, `<meta charset="UTF-8">`, `<meta viewport>`.
- Fontes via `<link>` Google Fonts: `Inter` (400/500/600/700) e `IBM Plex Mono` (400/600). Manter também `Cinzel` no `<link>` para consistência com as outras páginas, mesmo não usado nesta.
- `<title>LegisKids — Detalhes do Projeto</title>`.
- Importar `style.css` antes de `detalhe.css`.
- Hierarquia: `<nav class="navbar">` → `<main class="main">` com `<div class="container">` → `<footer class="footer">`.
- Atributos `aria-label` em botões só com ícone (padrão de `.icon-btn` em `index.html`).

### 5.3 JavaScript
- Vanilla JS, sem frameworks/bundlers.
- IIFE ou módulo simples: `(() => { ... })();`.
- Separar dados (mock) da lógica de renderização.
- Event listeners adicionados após `DOMContentLoaded`.

---

## 6. Tokens locais a adicionar (em `detalhe.css`, escopados por `.detalhe-page`)

A paleta do `spec.json` difere do dashboard. Definir tokens locais para evitar mudar `style.css`:

```css
.detalhe-page {
  --d-page-bg: #DDE3EE;
  --d-card-bg: #FFFFFF;
  --d-card-bg-subtle: #EEF1F8;
  --d-primary: #2B3FBF;
  --d-primary-hover: #1E2E99;
  --d-primary-light: #E8ECFB;
  --d-text-primary: #0F172A;
  --d-text-secondary: #475569;
  --d-text-caption: #64748B;
  --d-border: #D1D9E6;
  --d-border-light: #E8ECF4;
  --d-badge-urgente-bg: #FBCFCA;
  --d-badge-urgente-text: #C0392B;
  --d-badge-topic-bg: #F0E6FB;
  --d-badge-topic-text: #7C3AED;
  --d-badge-tramitacao-bg: #E0F2FE;
  --d-badge-tramitacao-text: #0369A1;
  --d-timeline-done: #22C55E;
  --d-timeline-line: #CBD5E1;
  --d-indicator-fill: #7C3AED;
  --d-indicator-empty: #D1D5DB;
  --d-pdf-icon-bg: #FEE2E2;
  --d-pdf-icon-color: #EF4444;
  --d-radius-md: 12px;
  --d-radius-lg: 16px;
}
.detalhe-page { background: var(--d-page-bg); }
```

A `<body>` da página recebe `class="detalhe-page"` (padrão já usado em `pesquisa.html` com `class="pesquisa-page"`).

---

## 7. Estrutura HTML (esqueleto)

```html
<body class="detalhe-page">
  <nav class="navbar">…</nav>

  <main class="main">
    <div class="container detalhe-container">

      <!-- 7.1 TopBar -->
      <div class="detalhe-topbar">
        <a class="detalhe-topbar__back" href="index.html">…</a>
        <div class="detalhe-topbar__actions">
          <button class="btn-outline" id="btnShareTop">Compartilhar</button>
          <button class="btn-outline" id="btnSalvar">Salvar</button>
        </div>
      </div>

      <!-- 7.2 ProjectHeader -->
      <header class="projeto-header">
        <div class="projeto-header__badges">
          <span class="badge badge--id">PL-2654/2026</span>
          <span class="badge badge--urgente">Urgente</span>
          <span class="badge badge--topic">Proteção Legal</span>
        </div>
        <h1 class="projeto-header__title">…</h1>
        <p class="projeto-header__subtitle">…</p>
        <div class="projeto-header__meta">
          <div class="meta-item">…</div>
          <div class="meta-item">…</div>
        </div>
      </header>

      <!-- 7.3 Tabs -->
      <nav class="detalhe-tabs" role="tablist">
        <button class="detalhe-tab detalhe-tab--active" role="tab" aria-selected="true" data-tab="visao">…</button>
        <button class="detalhe-tab" role="tab" data-tab="tramitacao">…</button>
        <button class="detalhe-tab" role="tab" data-tab="analise">…</button>
        <button class="detalhe-tab" role="tab" data-tab="documentos">…</button>
        <button class="detalhe-tab" role="tab" data-tab="comentarios">…</button>
      </nav>

      <!-- 7.4 Content Grid -->
      <div class="detalhe-grid">

        <section class="detalhe-main" role="tabpanel" data-panel="visao">
          <!-- Sobre o projeto -->
          <article class="detalhe-card">
            <h2 class="detalhe-card__title">Sobre o projeto</h2>
            <div class="detalhe-card__body collapsed" id="sobreBody">…</div>
            <button class="btn-expand" id="sobreToggle">Ver mais <svg>…</svg></button>
          </article>

          <!-- Informações pessoais -->
          <article class="detalhe-card">
            <h2 class="detalhe-card__title">Informações pessoais</h2>
            <div class="info-grid">
              <div class="info-cell">
                <span class="info-cell__label">Autor</span>
                <span class="info-cell__value">Dep. Ana Silva</span>
              </div>
              …
            </div>
          </article>

          <!-- Objetivos do projeto -->
          <article class="detalhe-card">
            <h2 class="detalhe-card__title">Objetivos do projeto</h2>
            <ul class="objetivos-list">
              <li class="objetivo-item">
                <span class="objetivo-check"><svg>…</svg></span>
                <span>Proteger crianças e adolescentes…</span>
              </li>
              …
            </ul>
          </article>

          <!-- Documentos e anexos -->
          <article class="detalhe-card">
            <h2 class="detalhe-card__title">Documentos e anexos</h2>
            <div class="doc-list">
              <div class="doc-item">
                <div class="doc-item__icon">…</div>
                <div class="doc-item__info">
                  <span class="doc-item__name">Texto completo do projeto</span>
                  <span class="doc-item__meta">PDF • 245 KB</span>
                </div>
                <button class="btn-download">Baixar</button>
              </div>
              …
            </div>
            <a class="detalhe-card__link" href="#">Ver todos os documentos (5) <svg>…</svg></a>
          </article>

          <!-- Projetos relacionados -->
          <article class="detalhe-card">
            <header class="detalhe-card__header">
              <h2 class="detalhe-card__title">Projetos relacionados</h2>
              <a class="detalhe-card__link-right" href="#">Ver todos</a>
            </header>
            <div class="relacionados-grid">
              <a class="relacionado-card" href="…">…</a>
              <a class="relacionado-card" href="…">…</a>
              <a class="relacionado-card" href="…">…</a>
            </div>
          </article>
        </section>

        <aside class="detalhe-sidebar">
          <!-- Status da tramitação -->
          <article class="detalhe-card sidebar-card">…</article>
          <!-- Análise e indicadores -->
          <article class="detalhe-card sidebar-card">…</article>
          <!-- Compartilhar -->
          <article class="detalhe-card sidebar-card">…</article>
        </aside>

      </div>
    </div>
  </main>

  <footer class="footer">…</footer>
  <script src="../js/detalhe.js"></script>
</body>
```

---

## 8. Componentes — classes e regras

> Todas as regras a seguir vivem em `frontend/css/detalhe.css`. Tokens `--d-*` definidos na seção 6.

### 8.1 TopBar — `.detalhe-topbar`
- Flex space-between; padding `20px 0 16px`.
- `.detalhe-topbar__back`: link com SVG `arrow-left` + texto "Voltar ao dashboard"; `color: var(--d-primary)`; `font-size:14px`; `font-weight:500`. Hover: underline.
- `.detalhe-topbar__actions`: flex gap `12px`.
- `.btn-outline`: `background: var(--d-card-bg)`; `border:1px solid var(--d-border)`; `border-radius:8px`; `padding:8px 16px`; `font-size:14px`; cursor pointer; flex com gap 8px para ícone. Hover: `background:#F1F5F9; border-color:#B0BBD0`.

### 8.2 ProjectHeader — `.projeto-header`
- `padding: 8px 0 24px`.
- `.projeto-header__badges`: flex gap `10px` margin-bottom `16px` flex-wrap.
- `.badge`: `font-size:12px; font-weight:600; padding:5px 14px; border-radius:9999px`.
- `.badge--id`: `background: var(--d-primary-light); color: var(--d-primary); font-family:'IBM Plex Mono', monospace`.
- `.badge--urgente`: `background: var(--d-badge-urgente-bg); color: var(--d-badge-urgente-text)`.
- `.badge--topic`: `background: var(--d-badge-topic-bg); color: var(--d-badge-topic-text)`.
- `.projeto-header__title`: `font-size:32px; font-weight:700; line-height:1.2; color: var(--d-text-primary); margin-bottom:8px`.
- `.projeto-header__subtitle`: `font-size:14px; color: var(--d-text-secondary); margin-bottom:20px`.
- `.projeto-header__meta`: flex gap `40px` flex-wrap.
- `.meta-item`: flex align-items flex-start gap `10px`; SVG `width:20px; height:20px; stroke:#94A3B8; flex-shrink:0; margin-top:2px`.
- `.meta-item__label`: `display:block; font-size:12px; color: var(--d-text-caption)`.
- `.meta-item__value`: `display:block; font-size:14px; font-weight:600; color: var(--d-text-primary)`.

### 8.3 Tabs — `.detalhe-tabs`
- Container: `display:flex; background: var(--d-card-bg); border-radius: var(--d-radius-md); padding: 0 8px; box-shadow: var(--shadow); overflow-x:auto`.
- `.detalhe-tab`: `display:flex; align-items:center; gap:8px; padding:16px 20px; font-size:15px; font-weight:500; color: var(--d-text-caption); background:none; border:none; cursor:pointer; border-bottom:3px solid transparent; white-space:nowrap; transition: color var(--transition), border-color var(--transition)`.
- `.detalhe-tab--active`: `color: var(--d-primary); border-bottom-color: var(--d-primary); font-weight:600`.
- Hover (não-ativa): `color: var(--d-primary); background:#F8F9FF`.
- Ícones SVG `width:18px; height:18px; stroke:currentColor`.
- Tabs e seus ícones (Lucide): `globe` (Visão geral, ativa), `settings` (Tramitação), `bar-chart-2` (Análise), `file-text` (Documentos), `message-square` (Comentários).

### 8.4 Card base — `.detalhe-card`
- `background: var(--d-card-bg); border-radius: var(--d-radius-lg); padding:24px; box-shadow: var(--shadow)`.
- `.detalhe-card__title`: `font-size:18px; font-weight:700; color: var(--d-text-primary); margin-bottom:16px`.
- `.detalhe-card__header`: flex space-between align-items center margin-bottom `20px` (variante usada em "Projetos relacionados").
- `.detalhe-card__link`: flex space-between padding `16px 0 4px` color `var(--d-primary)` font-weight 500 text-decoration none. Hover: underline.
- `.detalhe-card__link-right`: `font-size:14px; font-weight:600; color: var(--d-primary)`.

### 8.5 Sobre o projeto
- `.detalhe-card__body`: `font-size:14px; color: var(--d-text-secondary); line-height:1.6; display:flex; flex-direction:column; gap:12px`.
- `.detalhe-card__body.collapsed`: `max-height:120px; overflow:hidden; mask-image: linear-gradient(to bottom, #000 60%, transparent)` (degradê opcional).
- `.btn-expand`: `display:flex; align-items:center; gap:6px; background:none; border:none; color: var(--d-primary); font-size:14px; font-weight:500; cursor:pointer; margin-top:16px`. Hover: underline. Chevron `svg.btn-expand__icon` rotaciona `transform: rotate(180deg)` quando expandido (classe `.btn-expand--open`).

### 8.6 Informações pessoais — `.info-grid`
- `display:grid; grid-template-columns:repeat(4, 1fr); gap:12px`.
- `.info-cell`: `background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:12px 16px`.
- `.info-cell__label`: `display:block; font-size:12px; color: var(--d-text-caption); margin-bottom:4px`.
- `.info-cell__value`: `display:block; font-size:14px; font-weight:600; color: var(--d-text-primary)`.
- **Especial — urgência**: `.info-cell__value` contém `<span class="dot dot--red"></span>` inline antes do texto:
  - `.dot`: `width:8px; height:8px; border-radius:50%; display:inline-block; margin-right:6px; vertical-align: middle`.
  - `.dot--red`: `background:#EF4444`.
  - `.dot--gray`: `background: var(--d-text-caption)`.

### 8.7 Objetivos — `.objetivos-list`
- `list-style:none; display:flex; flex-direction:column; gap:16px; padding:0`.
- `.objetivo-item`: `display:flex; align-items:center; gap:12px; font-size:14px; color: var(--d-text-primary); font-weight:500`.
- `.objetivo-check`: `width:24px; height:24px; border-radius:50%; background: var(--d-timeline-done); display:flex; align-items:center; justify-content:center; flex-shrink:0`.
- SVG check interno: `stroke:#FFFFFF; stroke-width:2.5; width:12px; height:12px`.

### 8.8 Documentos — `.doc-list`
- Container: `display:flex; flex-direction:column`.
- `.doc-item`: `display:flex; align-items:center; gap:16px; padding:16px 0; border-bottom:1px solid var(--d-border-light)`. Último item sem borda inferior.
- `.doc-item__icon`: `width:40px; height:40px; border-radius:8px; background: var(--d-pdf-icon-bg); display:flex; align-items:center; justify-content:center; flex-shrink:0`. SVG `stroke: var(--d-pdf-icon-color)`.
- `.doc-item__info`: `flex:1; min-width:0`.
- `.doc-item__name`: `display:block; font-size:14px; font-weight:600; color: var(--d-text-primary)`.
- `.doc-item__meta`: `display:flex; align-items:center; gap:6px; font-size:12px; color: var(--d-text-caption); margin-top:2px`.
- `.btn-download`: idem `.btn-outline`, com SVG `download` 16x16. Hover: `background:#F1F5F9`.

### 8.9 Projetos relacionados — `.relacionados-grid`
- `display:grid; grid-template-columns:repeat(3, 1fr); gap:16px`.
- `.relacionado-card`: `background: var(--d-card-bg-subtle); border:1px solid #DDE3EE; border-radius: var(--d-radius-md); padding:16px; display:flex; flex-direction:column; gap:10px; cursor:pointer; text-decoration:none; transition: box-shadow var(--transition), border-color var(--transition)`.
- Hover: `box-shadow:0 4px 16px rgba(0,0,0,0.10); border-color:#B8C5E0`.
- `.relacionado-card__title`: `font-size:13px; color: var(--d-text-secondary); line-height:1.5; flex:1`.

### 8.10 Sidebar — `.detalhe-sidebar` + `.sidebar-card`
- Sidebar: flex column gap `20px`; largura fixa `320px` no desktop.
- `.sidebar-card`: `padding:20px; border-radius: var(--d-radius-lg)` (override sutil de `.detalhe-card` para sidebar mais compacto).
- `.sidebar-card__header`: flex space-between align-items center margin-bottom `6px`.
- `.sidebar-card__header h3`: `font-size:15px; font-weight:700; color: var(--d-text-primary)`.
- `.sidebar-card__subtitle`: `font-size:12px; color: var(--d-text-caption); margin-bottom:20px`.
- `.sidebar-card__link`: flex space-between padding `12px 0 0` border-top `1px solid var(--d-border-light)` margin-top `4px` font-size 14px font-weight 500 color `var(--d-primary)`.

### 8.11 Timeline — `.timeline`
- Container: `position:relative; display:flex; flex-direction:column`.
- `.timeline-item`: `display:flex; gap:12px; position:relative`.
- `.timeline-node`: `width:24px; height:24px; border-radius:50%; border:2px solid; display:flex; align-items:center; justify-content:center; flex-shrink:0; z-index:1; background:#FFFFFF`.
- `.timeline-node--done`: `background: var(--d-timeline-done); border-color: var(--d-timeline-done)` — SVG check branco interno.
- `.timeline-node--active`: `border-color: var(--d-primary)`.
- `.timeline-node--pending`: `border-color: var(--d-timeline-line)`.
- `.timeline-line`: `position:absolute; left:11px; top:24px; bottom:-24px; width:2px; background: var(--d-timeline-line); z-index:0`. Último item não tem linha.
- `.timeline-content`: `padding-bottom:24px; flex:1`.
- `.timeline-content__title`: `display:block; font-size:14px; font-weight:600; color: var(--d-text-primary)`.
- `.timeline-content__date`: `float:right; font-size:12px; color: var(--d-text-caption)`.
- `.timeline-content__desc`: `display:block; font-size:12px; color: var(--d-text-caption); margin-top:4px; clear:both`.
- `.timeline-item--active .timeline-content__title`: `color: var(--d-primary)`.
- `.badge--em-tramitacao`: `background: var(--d-badge-tramitacao-bg); color: var(--d-badge-tramitacao-text); font-size:11px; padding:3px 10px`.

### 8.12 Análise e indicadores — `.analise-card`
- `.analise-header`: flex gap `14px` align-items flex-start margin-bottom `20px`.
- `.analise-icon`: `width:48px; height:48px; border-radius:12px; background: var(--d-badge-topic-bg); display:flex; align-items:center; justify-content:center; flex-shrink:0`. SVG `book-open` stroke `#7C3AED`.
- `.indicators`: flex column.
- `.indicator`: `padding:16px 0; border-bottom:1px solid var(--d-border-light)`. Último item sem borda.
- `.indicator__labels`: flex space-between baseline margin-bottom `10px`.
- `.indicator__name`: `font-size:14px; font-weight:600; color: var(--d-text-primary)`.
- `.indicator__value`: `font-size:13px; color: var(--d-text-caption)`.
- `.indicator__bar`: `display:flex; gap:4px`.
- `.indicator__segment`: `height:8px; flex:1; border-radius:4px`.
- `.indicator__segment--filled`: `background: var(--d-indicator-fill)`.
- `.indicator__segment--empty`: `background: var(--d-indicator-empty)`.

### 8.13 Compartilhar — `.share-card`
- `.share-header`: flex gap `10px` align-items center margin-bottom `8px`. SVG `stroke:#475569`.
- `.share-buttons`: flex gap `8px`.
- `.share-btn`: `width:44px; height:44px; border-radius:8px; background:#F1F5F9; border:1px solid #E2E8F0; display:flex; align-items:center; justify-content:center; cursor:pointer; transition: background 0.15s`. Hover: `background:#E2E8F0`.

---

## 9. Grid principal (`.detalhe-grid`)

```css
.detalhe-grid {
  display: flex;
  gap: 24px;
}
.detalhe-main { flex: 1 1 0; min-width: 0; display: flex; flex-direction: column; gap: 20px; }
.detalhe-sidebar { width: 320px; flex-shrink: 0; display: flex; flex-direction: column; gap: 20px; }
```

---

## 10. Responsividade

Manter coerência com os breakpoints já existentes (`style.css`: 1100 / 900 / 640). Reconciliação com `spec.json`:

| Breakpoint | Comportamento |
|---|---|
| ≥ 1025px (desktop) | Grid 2 colunas; sidebar 320px; `.info-grid` 4 cols; `.relacionados-grid` 3 cols. |
| 641–1024px (tablet) | Sidebar empilhada abaixo da main; `.info-grid` 2 cols; `.relacionados-grid` 2 cols; tabs com `overflow-x:auto`. |
| ≤ 640px (mobile) | `.detalhe-topbar` empilhada (`flex-direction:column; align-items:flex-start; gap:12px`); `.projeto-header__title` `font-size:24px`; `.info-grid` 2 cols; `.relacionados-grid` 1 col; `.detalhe-tab` `padding:14px 14px; font-size:13px`; container padding lateral `16px`. |

```css
@media (max-width: 1024px) {
  .detalhe-grid { flex-direction: column; }
  .detalhe-sidebar { width: 100%; }
  .info-grid { grid-template-columns: repeat(2, 1fr); }
  .relacionados-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .detalhe-topbar { flex-direction: column; align-items: flex-start; gap: 12px; }
  .projeto-header__title { font-size: 24px; }
  .relacionados-grid { grid-template-columns: 1fr; }
  .detalhe-tab { padding: 14px 14px; font-size: 13px; }
}
```

---

## 11. Interações (JS — `detalhe.js`)

| Interação | Comportamento |
|---|---|
| Click em `.detalhe-tab` | Remove `.detalhe-tab--active` de todas, adiciona na clicada; alterna `aria-selected`; oculta/exibe `[data-panel]` correspondente. Painéis inicialmente: `visao` visível, demais com `hidden`. Suporte a `Enter`/`Space` para acessibilidade. |
| Click em `#sobreToggle` | Alterna classe `.collapsed` em `#sobreBody` e `.btn-expand--open` no botão; troca texto entre "Ver mais" / "Ver menos". |
| Click em `.btn-download` | Padrão de link de download — `<a download href="...">` wrapping ou `window.open(url, "_blank")`. Sem loading visível. |
| Click em `.relacionado-card` | `<a>` que navega para `detalhe-projeto.html?id=<id-do-relacionado>`. |
| Click em "Ver tramitação completa" / "Ver análise detalhada" | Aciona a tab correspondente (mesmo handler de `.detalhe-tab`). |
| Click em `.share-btn[data-share="link"]` | `navigator.clipboard.writeText(window.location.href)` → exibe tooltip "Copiado!" por 2s. |
| Click em `.share-btn[data-share="whatsapp"]` | Abre `https://wa.me/?text=<encodeURIComponent(titulo + " — " + url)>` em nova aba. |
| Click em `.share-btn[data-share="twitter"]` | Abre `https://twitter.com/intent/tweet?url=<url>&text=<titulo>` em nova aba. |
| Click em `.share-btn[data-share="facebook"]` | Abre `https://www.facebook.com/sharer/sharer.php?u=<url>` em nova aba. |
| Click em `#btnShareTop` | Mesma ação de copiar link (MVP) ou abrir dropdown (R2). |
| Click em `#btnSalvar` | Apenas alterna classe visual `.saved` no botão e troca SVG bookmark para preenchido. Sem persistência (sem auth — R2). |
| Navegação por teclado | Tab cicla pelos elementos interativos; foco visível com outline `2px solid var(--d-primary)` offset `2px`. |

```js
// Pseudocódigo de detalhe.js
const MOCK_PROJETO = { /* ver §13 */ };

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initSobreToggle();
  initShare();
  initSalvar();
});
```

---

## 12. Acessibilidade

- Contraste WCAG AA: revisar especialmente `--d-text-caption` (`#64748B`) sobre `--d-card-bg-subtle` (`#EEF1F8`) — `4.65:1`, OK.
- Tabs com `role="tablist"`, cada `button` com `role="tab"`, `aria-selected`, `tabindex="0"` apenas no ativo (roving tabindex).
- Painéis com `role="tabpanel"` e `aria-labelledby` apontando para o id da tab.
- Imagens decorativas (SVG) com `aria-hidden="true"`.
- Botões somente-ícone com `aria-label`.
- `<h1>` único por página (o título do projeto). `<h2>` para títulos de cards.

---

## 13. Mock data

Em `detalhe.js`, replicar o objeto `mockData.projeto` do `spec.json` como `MOCK_PROJETO`. Renderização: para esta entrega, preencher os campos diretamente no HTML estático (mais simples e visualmente verificável). A renderização dinâmica via mock fica como tarefa opcional preparatória para integração com backend.

Campos mínimos no HTML estático:
- ID: `PL-2654/2026`
- Status: `Urgente`
- Tópico: `Proteção Legal`
- Título: `Proteção Contra Cyberbullying e Assédio Online`
- Subtítulo: `Define cyberbullying como crime e estabelece medidas protetivas para vítimas menores de idade.`
- Meta: data `12/02/2026`, casa `Câmara dos Deputados`.
- Sobre: 2 parágrafos do `spec.json.sobre`.
- Informações pessoais (8 cells): Autor, Partido, Data de apresentação, Urgência (dot vermelho), Situação atual, Casa legislativa, Regime de tramitação, Autor (data secundária).
- Objetivos: 4 itens do `spec.json.objetivos`.
- Documentos: 3 PDFs visíveis + link "Ver todos os documentos (5)".
- Projetos relacionados: 3 cards do `spec.json.projetos_relacionados`.
- Timeline: 4 passos (`done`, `active`, `pending`, `pending`).
- Indicadores: Relevância 4/5 "Muito alta", Impacto social 3/5 "Alto", Apoio popular 3/5 "75%".

---

## 14. Critérios de aceitação

1. A página abre em `frontend/pages/detalhe-projeto.html` e renderiza sem erros no console.
2. Navbar e footer são visualmente idênticos aos de `index.html` (mesmas classes, mesma altura, mesmo logo, mesmo menu).
3. Clicar em "Ver Detalhes" em qualquer `projeto-card` de `index.html` ou em resultado de `pesquisa.html` navega para `detalhe-projeto.html?id=<id>`.
4. Clicar no botão "Voltar ao dashboard" retorna para `index.html`.
5. Trocar de aba muda visualmente o estado ativo e o conteúdo exibido (mesmo que aba `comentarios` mostre placeholder).
6. Botão "Ver mais" expande/contrai o card "Sobre o projeto" suavemente.
7. Botão "Baixar" em cada documento dispara o comportamento de download do browser (mesmo apontando para `#` em mock).
8. Botão "Copiar link" copia a URL atual e mostra confirmação "Copiado!".
9. Botões WhatsApp/Twitter/Facebook abrem URLs corretas em nova aba.
10. Em 320px de largura: navbar collapse (já é comportamento de `style.css`), layout em coluna única, sem scroll horizontal.
11. Foco visível em todos os elementos interativos (botões, links, tabs) ao navegar por teclado.
12. Contraste de texto/fundo aprovado em ferramenta automatizada (Lighthouse / axe DevTools) sem violações AA.
13. Nenhum estilo inline de cor/espaçamento adicionado a `style.css` (apenas leitura de tokens; estilos novos vivem em `detalhe.css`).
14. Lighthouse Performance ≥ 90 em desktop (sem assets pesados extras).

---

## 15. Restrições

- **Não** alterar `frontend/css/style.css`. Toda regra nova vai em `detalhe.css`.
- **Não** introduzir dependência JS externa (sem Tailwind, sem React, sem Lucide pacote — usar SVG inline).
- **Não** consumir API externa diretamente (frontend sempre via backend Flask — R2).
- **Não** implementar autenticação ou persistência de "Salvar"/"Favoritos".
- **Não** modificar a identidade visual de navbar/footer.
- Manter compatibilidade com Chrome/Edge/Firefox atuais (sem IE).
- Página HTML não pode exceder ~600 linhas; mover SVGs repetidos para constantes em `detalhe.js` quando passar disso.

---

## 16. Testes

### 16.1 Manual (checklist)
- [ ] Abrir `detalhe-projeto.html` em Chrome desktop (1920×1080) e validar layout 2 colunas.
- [ ] Reduzir janela para 1024px → sidebar empilha abaixo.
- [ ] Reduzir para 640px e 320px → grid colapsa, navbar reduzida, sem scroll horizontal.
- [ ] Clicar em cada uma das 5 tabs → conteúdo certo é exibido.
- [ ] Clicar "Ver mais" → card "Sobre o projeto" expande; clicar novamente → recolhe.
- [ ] Clicar em cada botão de compartilhamento → ação correta executada.
- [ ] Navegar apenas com `Tab` da navbar até o último botão da sidebar → ordem lógica, foco visível.
- [ ] Rodar `axe DevTools` → 0 violações críticas.
- [ ] Rodar Lighthouse → Accessibility ≥ 95, Performance ≥ 90.

### 16.2 Automatizado (futuro, fora deste escopo)
- Testes Playwright para a navegação `index → detalhe → voltar`, troca de tabs e cópia de link. Documentar quando ferramenta de E2E for incorporada ao projeto.

---

## 17. ADDED Requirements (formato OpenSpec)

### Requirement: Layout de duas colunas no desktop
A página SHALL renderizar conteúdo principal (largura flexível) e barra lateral (320px) lado a lado em viewports `≥ 1025px`, e em coluna única em viewports menores.

#### Scenario: Desktop large
- **WHEN** o viewport tem largura ≥ 1025px
- **THEN** `.detalhe-grid` aplica `flex-direction: row`, `.detalhe-sidebar` tem `width: 320px`, e o conteúdo principal ocupa o espaço restante.

#### Scenario: Tablet
- **WHEN** o viewport tem largura entre 641px e 1024px
- **THEN** `.detalhe-grid` aplica `flex-direction: column` e a sidebar passa a `width: 100%`.

### Requirement: Navegação por abas
A página SHALL exibir 5 abas (Visão geral, Tramitação, Análise, Documentos, Comentários) e permitir trocá-las via clique ou teclado, mantendo apenas uma ativa por vez.

#### Scenario: Click em aba inativa
- **WHEN** o usuário clica em uma `.detalhe-tab` que não tem `.detalhe-tab--active`
- **THEN** a classe é removida da aba anteriormente ativa e adicionada na clicada, e o `[data-panel]` correspondente passa a ser exibido enquanto os demais ficam ocultos.

#### Scenario: Acessibilidade por teclado
- **WHEN** o foco está em uma `.detalhe-tab` e o usuário pressiona `Enter` ou `Space`
- **THEN** a troca de aba ocorre exatamente como em um clique.

### Requirement: Expansão de "Sobre o projeto"
O card "Sobre o projeto" SHALL iniciar com altura limitada e ser expandido sob demanda pelo botão "Ver mais".

#### Scenario: Estado inicial
- **WHEN** a página carrega
- **THEN** `#sobreBody` tem a classe `.collapsed` e exibe no máximo `120px` de conteúdo.

#### Scenario: Expansão
- **WHEN** o usuário clica em `#sobreToggle`
- **THEN** `.collapsed` é removida de `#sobreBody`, o texto do botão muda para "Ver menos", e o chevron rotaciona 180°.

### Requirement: Reuso de tokens globais
A página SHALL reutilizar a navbar e o footer definidos em `style.css` sem duplicar regras CSS para esses componentes.

#### Scenario: Navbar reutilizada
- **WHEN** comparada visualmente com `index.html`
- **THEN** `.navbar`, `.logo-icon`, `.nav-item`, `.icon-btn` e `.notif-badge` apresentam o mesmo estilo, e nenhuma dessas classes é redefinida em `detalhe.css`.

### Requirement: Tokens locais com prefixo `--d-`
Tokens de cor e raio específicos desta página SHALL ser definidos sob o seletor `.detalhe-page` com prefixo `--d-`, sem modificar `:root` em `style.css`.

#### Scenario: Encapsulamento
- **WHEN** o seletor `.detalhe-page` é removido do `<body>`
- **THEN** nenhuma regra de `style.css` quebra e a página `index.html` continua exibida sem alterações visuais.

### Requirement: Compartilhamento por redes sociais
A página SHALL oferecer 4 botões de compartilhamento (Copiar link, WhatsApp, Twitter, Facebook).

#### Scenario: Copiar link
- **WHEN** o usuário clica em `.share-btn[data-share="link"]`
- **THEN** `navigator.clipboard.writeText(window.location.href)` é chamado e um tooltip "Copiado!" aparece por 2 segundos.

#### Scenario: WhatsApp
- **WHEN** o usuário clica em `.share-btn[data-share="whatsapp"]`
- **THEN** `https://wa.me/?text=<encoded>` é aberto em nova aba com o título do projeto e a URL atual.

### Requirement: Responsividade até 320px
A página SHALL ser totalmente utilizável em viewports a partir de 320px de largura, sem scroll horizontal e mantendo todos os elementos interativos acessíveis.

#### Scenario: Viewport mínimo
- **WHEN** o viewport tem largura 320px
- **THEN** não há scroll horizontal, `.detalhe-tabs` tem `overflow-x:auto`, `.info-grid` tem 2 colunas, e `.relacionados-grid` tem 1 coluna.

### Requirement: Acessibilidade WCAG AA
Todos os elementos textuais SHALL atender ao critério de contraste WCAG 2.1 AA (4.5:1 para texto normal, 3:1 para texto grande) e todos os elementos interativos SHALL ser operáveis por teclado.

#### Scenario: Auditoria automatizada
- **WHEN** a página é auditada com axe DevTools ou Lighthouse Accessibility
- **THEN** o score de acessibilidade é ≥ 95 e não há violações de contraste em texto sobre fundo.

---

## 18. Próximos passos pós-spec

1. Gerar `proposal.md`, `design.md` e `tasks.md` desta mudança a partir deste arquivo (executar `/opsx:propose`).
2. Implementar via `/opsx:apply`, seguindo as tasks em ordem.
3. Validar critérios da §14 manualmente.
4. Arquivar a mudança com `/opsx:archive` após merge.

> Esta spec é a fonte da verdade para `detalhe-projeto.html`. Qualquer divergência entre código e spec deve atualizar primeiro este arquivo.
