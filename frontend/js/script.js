// Mock data — substituir por fetch ao backend quando disponível
const MOCK_PROJETOS = [
  {
    id: 'PL-001',
    status: 'Urgente',
    statusBg: '#F6A6A6',
    statusColor: '#8B0000',
    topic: 'Cyberbullying',
    title: 'Tema do Projeto de Lei',
    desc: 'Resumo sobre o novo projeto relacionado à proteção de crianças e adolescentes no ambiente digital.',
    data: 'Data da aprovação do projeto',
    local: 'Onde foi aprovado',
  },
  {
    id: 'PL-002',
    status: 'Aprovado',
    statusBg: '#A7E8B4',
    statusColor: '#1B5E20',
    topic: 'Proteção Infantil',
    title: 'Tema do Projeto de Lei',
    desc: 'Resumo sobre o novo projeto relacionado à proteção de crianças e adolescentes no ambiente digital.',
    data: 'Data da aprovação do projeto',
    local: 'Onde foi aprovado',
  },
];

// Filtro de busca nos projetos recentes
const searchInput = document.getElementById('searchInput');
const projetosList = document.getElementById('projetosList');

if (searchInput && projetosList) {
  searchInput.addEventListener('input', () => {
    const query = searchInput.value.trim().toLowerCase();
    const cards = projetosList.querySelectorAll('.projeto-card');

    let anyVisible = false;
    cards.forEach(card => {
      const topic = card.dataset.topic || '';
      const id = card.dataset.id || '';
      const title = card.querySelector('.projeto-title')?.textContent || '';
      const desc = card.querySelector('.projeto-desc')?.textContent || '';
      const text = `${topic} ${id} ${title} ${desc}`.toLowerCase();

      const match = !query || text.includes(query);
      card.style.display = match ? '' : 'none';
      if (match) anyVisible = true;
    });

    const existing = projetosList.querySelector('.empty-state');
    if (!anyVisible && !existing) {
      const msg = document.createElement('p');
      msg.className = 'empty-state';
      msg.textContent = `Nenhum projeto encontrado para "${searchInput.value}".`;
      projetosList.appendChild(msg);
    } else if (anyVisible && existing) {
      existing.remove();
    }
  });
}

// Alert banner
const alertBtn = document.querySelector('.alert-banner__btn');
if (alertBtn) {
  alertBtn.addEventListener('click', () => {
    // TODO: abrir modal ou navegar para detalhe do PL com prazo próximo
    console.log('Ver detalhes do alerta de prazo');
  });
}

// Projetos — botão Ver Detalhes
projetosList?.addEventListener('click', (e) => {
  if (!e.target.classList.contains('projeto-btn')) return;
  const card = e.target.closest('.projeto-card');
  const id = card?.dataset.id;
  // TODO: navegar para projetos.html?id=PL-001
  console.log(`Abrir detalhes de ${id}`);
});

// Biblioteca — clique nas categorias
document.querySelectorAll('.biblioteca-card').forEach(card => {
  card.addEventListener('click', () => {
    const label = card.querySelector('span')?.textContent;
    if (searchInput) {
      searchInput.value = label;
      searchInput.dispatchEvent(new Event('input'));
      searchInput.focus();
    }
  });
});

// Quick actions
document.querySelectorAll('.qa-card').forEach((card, i) => {
  card.addEventListener('click', () => {
    const actions = ['participacao', 'analises', 'alertas'];
    // TODO: navegar para a página correspondente
    console.log(`Ação rápida: ${actions[i]}`);
  });
});
