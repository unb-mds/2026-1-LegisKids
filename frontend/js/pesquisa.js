/* =====================================================
   LegisKids — Tela de Pesquisa
   Renderiza resultados a partir do mockData definido no spec
   ===================================================== */

const MOCK_RESULTS = [
  {
    id: 'PL-2654/2026',
    status: 'Urgente',
    statusType: 'urgent',
    topic: 'Proteção Legal',
    title: 'Proteção Contra Cyberbullying e Assédio Online',
    description: 'Define cyberbullying como crime e estabelece medidas protetivas para vítimas menores de idade.',
    date: '02/04/2026',
    institution: 'Câmara dos Deputados',
  },
  {
    id: 'PL-2103/2026',
    status: 'Aprovado',
    statusType: 'approved',
    topic: 'Transparência',
    title: 'Transparência em Algoritmos de Recomendação para Menores',
    description: 'Obriga plataformas digitais a divulgarem critérios de algoritmos para usuários menores.',
    date: '28/03/2026',
    institution: 'Senado Federal',
  },
  {
    id: 'PL-1987/2026',
    status: 'Ativo',
    statusType: 'active',
    topic: 'Educação Digital',
    title: 'Programa Nacional de Educação Digital Infantil',
    description: 'Institui diretrizes para alfabetização digital segura nas escolas.',
    date: '19/03/2026',
    institution: 'Câmara dos Deputados',
  },
];

const TOTAL_RESULTS = 23;
const TOTAL_PAGES = 8;

const ICON_CALENDAR = `
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <rect x="3" y="4" width="18" height="18" rx="2"/>
    <line x1="16" y1="2" x2="16" y2="6"/>
    <line x1="8" y1="2" x2="8" y2="6"/>
    <line x1="3" y1="10" x2="21" y2="10"/>
  </svg>
`;

const ICON_INSTITUTION = `
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M3 21h18"/>
    <path d="M5 21V8l7-4 7 4v13"/>
    <path d="M9 21V12h6v9"/>
  </svg>
`;

const escapeHtml = (str = '') =>
  String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');

function renderResultCard(item) {
  const card = document.createElement('article');
  card.className = 'result-card';
  card.dataset.id = item.id;

  card.innerHTML = `
    <header class="result-card__header">
      <div class="result-card__badges">
        <span class="badge badge--pl">${escapeHtml(item.id)}</span>
        <span class="badge badge--topic">${escapeHtml(item.topic)}</span>
      </div>
      <span class="badge badge--status is-${escapeHtml(item.statusType)}">${escapeHtml(item.status)}</span>
    </header>

    <div class="result-card__content">
      <h3 class="result-card__title">${escapeHtml(item.title)}</h3>
      <p class="result-card__description">${escapeHtml(item.description)}</p>
    </div>

    <footer class="result-card__footer">
      <span>${ICON_CALENDAR}${escapeHtml(item.date)}</span>
      <span>${ICON_INSTITUTION}${escapeHtml(item.institution)}</span>
    </footer>
  `;

  card.addEventListener('click', () => {
    // TODO: navegar para a página de detalhes (projetos.html?id=...)
    console.log(`[pesquisa] Abrir detalhes de ${item.id}`);
  });

  return card;
}

function renderResults(items) {
  const list = document.getElementById('resultsList');
  if (!list) return;

  list.innerHTML = '';

  if (!items.length) {
    const empty = document.createElement('p');
    empty.className = 'empty-state';
    const query = document.getElementById('searchInput')?.value || '';
    empty.textContent = `Nenhum resultado encontrado para "${query}".`;
    list.appendChild(empty);
    return;
  }

  const fragment = document.createDocumentFragment();
  items.forEach(item => fragment.appendChild(renderResultCard(item)));
  list.appendChild(fragment);
}

function renderPagination(current = 1, total = TOTAL_PAGES) {
  const nav = document.getElementById('pagination');
  if (!nav) return;

  nav.innerHTML = '';

  const makeBtn = (label, page, opts = {}) => {
    const btn = document.createElement('button');
    btn.className = 'pagination__btn';
    btn.type = 'button';
    btn.innerHTML = label;
    if (opts.active) btn.classList.add('is-active');
    if (opts.disabled) btn.disabled = true;
    if (opts.ariaLabel) btn.setAttribute('aria-label', opts.ariaLabel);
    if (page) {
      btn.addEventListener('click', () => renderPagination(page, total));
    }
    return btn;
  };

  const makeEllipsis = () => {
    const span = document.createElement('span');
    span.className = 'pagination__ellipsis';
    span.textContent = '…';
    return span;
  };

  const chevronLeft = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>`;
  const chevronRight = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>`;

  nav.appendChild(makeBtn(chevronLeft, Math.max(1, current - 1), {
    disabled: current === 1,
    ariaLabel: 'Página anterior',
  }));

  const pages = new Set([1, 2, current - 1, current, current + 1, total - 1, total]);
  const visible = [...pages].filter(p => p >= 1 && p <= total).sort((a, b) => a - b);

  let prev = 0;
  visible.forEach(p => {
    if (p - prev > 1) nav.appendChild(makeEllipsis());
    nav.appendChild(makeBtn(String(p), p, {
      active: p === current,
      ariaLabel: `Página ${p}`,
    }));
    prev = p;
  });

  nav.appendChild(makeBtn(chevronRight, Math.min(total, current + 1), {
    disabled: current === total,
    ariaLabel: 'Próxima página',
  }));
}

function getQueryFromURL() {
  try {
    const params = new URLSearchParams(window.location.search);
    const q = params.get('q');
    return q ? q.trim() : '';
  } catch {
    return '';
  }
}

const INITIAL_QUERY = getQueryFromURL() || 'Cyberbullying';

function filterResults(query) {
  const q = (query || '').trim().toLowerCase();
  // Query original/semântica: backend já entregou esses 3 resultados.
  if (!q || q === INITIAL_QUERY.toLowerCase()) return MOCK_RESULTS;

  return MOCK_RESULTS.filter(item => {
    const haystack = `${item.id} ${item.title} ${item.topic} ${item.description} ${item.institution} ${item.status}`.toLowerCase();
    return haystack.includes(q);
  });
}

function updateSearchSummary(query) {
  const queryEl = document.getElementById('searchSummaryQuery');
  const counterEl = document.getElementById('resultsCounter');
  if (!queryEl || !counterEl) return;

  const text = (query || '').trim();
  queryEl.textContent = text ? `“${text}”` : '“Todos os resultados”';

  if (!text || text.toLowerCase() === INITIAL_QUERY.toLowerCase()) {
    counterEl.textContent = TOTAL_RESULTS;
    return;
  }
  const filtered = filterResults(text);
  counterEl.textContent = filtered.length;
}

function sortResults(items, mode) {
  const copy = [...items];
  switch (mode) {
    case 'old':
      return copy.sort((a, b) => parseDate(a.date) - parseDate(b.date));
    case 'urgent': {
      const order = { urgent: 0, active: 1, analysis: 2, approved: 3 };
      return copy.sort((a, b) => (order[a.statusType] ?? 9) - (order[b.statusType] ?? 9));
    }
    case 'alpha':
      return copy.sort((a, b) => a.title.localeCompare(b.title, 'pt-BR'));
    case 'recent':
    default:
      return copy.sort((a, b) => parseDate(b.date) - parseDate(a.date));
  }
}

function parseDate(str) {
  const [d, m, y] = String(str).split('/').map(Number);
  return new Date(y, (m || 1) - 1, d || 1).getTime();
}

function refresh() {
  const searchInput = document.getElementById('searchInput');
  const sortSelect = document.getElementById('sortDropdown');
  const query = searchInput?.value || '';
  const sortMode = sortSelect?.value || 'recent';

  const filtered = filterResults(query);
  const sorted = sortResults(filtered, sortMode);

  renderResults(sorted);
  updateSearchSummary(query);
}

/* ===== INIT ===== */
document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  if (searchInput) searchInput.value = INITIAL_QUERY;

  refresh();
  renderPagination(1, TOTAL_PAGES);

  document.getElementById('searchInput')?.addEventListener('input', refresh);

  document.getElementById('searchInput')?.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      refresh();
    }
  });

  document.getElementById('sortDropdown')?.addEventListener('change', refresh);

  document.getElementById('filtersButton')?.addEventListener('click', () => {
    // TODO: abrir modal lateral de filtros
    console.log('[pesquisa] Abrir modal de filtros');
  });

  document.getElementById('backButton')?.addEventListener('click', () => {
    if (window.history.length > 1) {
      window.history.back();
    } else {
      window.location.href = 'index.html';
    }
  });
});
