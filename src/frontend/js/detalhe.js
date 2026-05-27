/* =====================================================
   LegisKids — Tela de Detalhes do Projeto de Lei
   Lógica de UI: tabs, expand "Sobre", share, salvar.
   Mock data espelhando spec.json.mockData.projeto;
   render dinâmico só será necessário quando o backend
   /api/proposicoes/<id> estiver disponível.
   ===================================================== */

(() => {
  'use strict';

  const MOCK_PROJETO = {
    id: 'PL-2654/2026',
    status: 'urgente',
    status_label: 'Urgente',
    topico: 'Proteção Legal',
    titulo: 'Proteção Contra Cyberbullying e Assédio Online',
    subtitulo: 'Define cyberbullying como crime e estabelece medidas protetivas para vítimas menores de idade.',
    data_aprovacao: '12/02/2026',
    casa_aprovacao: 'Câmara dos Deputados',
    autor: 'Dep. Ana Silva',
    partido: 'PL',
    data_apresentacao: '10/05/2025',
    urgencia: 'Alta',
    situacao_atual: 'Em tramitação',
    casa_legislativa: 'Câmara dos Deputados',
    regime_tramitacao: 'Ordinário'
  };

  /* ===== TABS ===== */
  function initTabs() {
    const tabs = Array.from(document.querySelectorAll('.detalhe-tab'));
    const panels = Array.from(document.querySelectorAll('.detalhe-panel'));
    if (!tabs.length) return;

    function activate(target) {
      const tab = typeof target === 'string'
        ? tabs.find(t => t.dataset.tab === target)
        : target;
      if (!tab) return;

      tabs.forEach(t => {
        const isActive = t === tab;
        t.classList.toggle('detalhe-tab--active', isActive);
        t.setAttribute('aria-selected', isActive ? 'true' : 'false');
        t.setAttribute('tabindex', isActive ? '0' : '-1');
      });

      const targetPanel = tab.dataset.tab;
      panels.forEach(p => {
        const matches = p.dataset.panel === targetPanel;
        if (matches) {
          p.removeAttribute('hidden');
        } else {
          p.setAttribute('hidden', '');
        }
      });
    }

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => activate(tab));

      tab.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          activate(tab);
          return;
        }
        if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') {
          e.preventDefault();
          const direction = e.key === 'ArrowRight' ? 1 : -1;
          const next = tabs[(index + direction + tabs.length) % tabs.length];
          next.focus();
          activate(next);
        }
        if (e.key === 'Home') {
          e.preventDefault();
          tabs[0].focus();
          activate(tabs[0]);
        }
        if (e.key === 'End') {
          e.preventDefault();
          tabs[tabs.length - 1].focus();
          activate(tabs[tabs.length - 1]);
        }
      });
    });

    return { activate };
  }

  /* ===== SOBRE — EXPANDIR / RECOLHER ===== */
  function initSobreToggle() {
    const toggle = document.getElementById('sobreToggle');
    const body = document.getElementById('sobreBody');
    if (!toggle || !body) return;

    const label = toggle.querySelector('.btn-expand__label');

    toggle.addEventListener('click', () => {
      const willExpand = body.classList.contains('collapsed');
      body.classList.toggle('collapsed', !willExpand);
      toggle.classList.toggle('btn-expand--open', willExpand);
      toggle.setAttribute('aria-expanded', willExpand ? 'true' : 'false');
      if (label) label.textContent = willExpand ? 'Ver menos' : 'Ver mais';
    });
  }

  /* ===== COMPARTILHAR ===== */
  function showTooltip() {
    const tooltip = document.getElementById('shareTooltip');
    if (!tooltip) return;
    tooltip.classList.add('is-visible');
    clearTimeout(showTooltip._timer);
    showTooltip._timer = setTimeout(() => {
      tooltip.classList.remove('is-visible');
    }, 2000);
  }

  async function copyLink() {
    const url = window.location.href;
    try {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(url);
      } else {
        // Fallback simples para browsers sem Clipboard API
        const temp = document.createElement('textarea');
        temp.value = url;
        temp.setAttribute('readonly', '');
        temp.style.position = 'absolute';
        temp.style.left = '-9999px';
        document.body.appendChild(temp);
        temp.select();
        document.execCommand('copy');
        document.body.removeChild(temp);
      }
      showTooltip();
    } catch (err) {
      console.error('Falha ao copiar link:', err);
    }
  }

  function buildShareUrl(rede) {
    const url = window.location.href;
    const titulo = MOCK_PROJETO.titulo;
    switch (rede) {
      case 'whatsapp':
        return 'https://wa.me/?text=' + encodeURIComponent(titulo + ' — ' + url);
      case 'twitter':
        return 'https://twitter.com/intent/tweet?url=' + encodeURIComponent(url) +
               '&text=' + encodeURIComponent(titulo);
      case 'facebook':
        return 'https://www.facebook.com/sharer/sharer.php?u=' + encodeURIComponent(url);
      default:
        return null;
    }
  }

  function initShare() {
    document.querySelectorAll('[data-share]').forEach(btn => {
      btn.addEventListener('click', () => {
        const rede = btn.dataset.share;
        if (rede === 'link') {
          copyLink();
          return;
        }
        const shareUrl = buildShareUrl(rede);
        if (shareUrl) window.open(shareUrl, '_blank', 'noopener,noreferrer');
      });
    });
  }

  function initBtnShareTop() {
    const btn = document.getElementById('btnShareTop');
    if (!btn) return;
    btn.addEventListener('click', copyLink);
  }

  /* ===== SALVAR ===== */
  function initSalvar() {
    const btn = document.getElementById('btnSalvar');
    if (!btn) return;
    const label = btn.querySelector('.btn-outline__label');
    btn.addEventListener('click', () => {
      const isSaved = btn.classList.toggle('is-saved');
      btn.setAttribute('aria-pressed', isSaved ? 'true' : 'false');
      if (label) label.textContent = isSaved ? 'Salvo' : 'Salvar';
    });
  }

  /* ===== LINKS DA SIDEBAR ===== */
  function initSidebarLinks(tabsApi) {
    if (!tabsApi) return;
    document.querySelectorAll('[data-link]').forEach(link => {
      link.addEventListener('click', (e) => {
        const target = link.dataset.link;
        if (!target) return;
        e.preventDefault();
        tabsApi.activate(target);
        const panel = document.querySelector('[data-panel="' + target + '"]');
        if (panel) panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  /* ===== BOOTSTRAP ===== */
  document.addEventListener('DOMContentLoaded', () => {
    const tabsApi = initTabs();
    initSobreToggle();
    initShare();
    initBtnShareTop();
    initSalvar();
    initSidebarLinks(tabsApi);
  });
})();
