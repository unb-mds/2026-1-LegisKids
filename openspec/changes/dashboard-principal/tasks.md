## 1. HTML — estrutura e componentes

- [x] 1.1 Implementar navbar com logo SVG inline, links Projetos/Alertas/Análises, botões de configurações e notificações com badge de contagem
- [x] 1.2 Implementar seção de stats cards (4 cards: Projetos Ativos, Proposições Ativas, Alertas Urgentes, Monitoramentos) com valores mock e ícones SVG coloridos por categoria
- [x] 1.3 Implementar alert banner laranja com borda esquerda, ícone de aviso, texto e botão "Ver Detalhes"
- [x] 1.4 Implementar search bar arredondada (border-radius 999px) com ícone de lupa posicionado
- [x] 1.5 Implementar Biblioteca Legislativa em grid 4×2 com 8 cards temáticos (Cyberbullying, Proteção de Dados, Exploração Infantil, Redes Sociais, Jogos Online, Conteúdo Nocivo, Segurança Digital, Regulação Digital) e ícones SVG
- [x] 1.6 Implementar seção "Projetos de Lei Recentes" com 2 cards mock (PL-001 Urgente, PL-002 Aprovado) contendo tag, status colorido, tópico, título, descrição, metadados e botão "Ver Detalhes"
- [x] 1.7 Implementar seção "Ações Rápidas" com 3 cards (Participação Pública, Análises e Relatórios, Configurar Alertas) com ícones e seta de navegação
- [x] 1.8 Implementar footer com cor `#2447D5`, texto de copyright e links (Sobre, Contato, Privacidade)

## 2. CSS — design system e responsividade

- [x] 2.1 Mapear todos os tokens de cor, sombra, border-radius e transição do `spec.json` para variáveis CSS em `:root`
- [x] 2.2 Estilizar navbar com altura 72px, sticky, sombra e estados hover/active nos links
- [x] 2.3 Estilizar stats cards com hover `translateY(-3px)` e transição 0.2s
- [x] 2.4 Estilizar biblioteca cards com hover `translateY(-3px)`, borda sutil e ícone com border-radius 13px
- [x] 2.5 Estilizar projeto cards e quick action cards com hover e botões com transição de preenchimento
- [x] 2.6 Implementar breakpoint desktop → 4 colunas nas stats e biblioteca, bottom-grid com sidebar de 360px
- [x] 2.7 Implementar breakpoint tablet (≤900px) → 2 colunas nas stats e biblioteca, bottom-grid empilhado
- [x] 2.8 Implementar breakpoint mobile (≤640px) → navbar sem menu, padding reduzido, footer empilhado

## 3. JavaScript — mock data e interatividade

- [x] 3.1 Definir `MOCK_PROJETOS` e `MOCK_STATS` como constantes documentadas com TODO de substituição por fetch
- [x] 3.2 Implementar filtro de busca em tempo real nos cards de projetos recentes (filtra por tópico, id, título, descrição)
- [x] 3.3 Implementar empty state ("Nenhum projeto encontrado para...") quando busca não retorna resultados
- [x] 3.4 Implementar clique nos cards da Biblioteca Legislativa para preencher e disparar o filtro de busca
- [x] 3.5 Adicionar event listeners nos botões "Ver Detalhes" e quick actions com console.log e TODO de navegação

## 4. Integração futura (próximas tasks — não nesta change)

- [ ] 4.1 Substituir `MOCK_STATS` por `fetch('/api/stats')` quando o endpoint Flask estiver disponível
- [ ] 4.2 Substituir `MOCK_PROJETOS` por `fetch('/api/proposicoes?limite=5')` e renderizar cards dinamicamente
- [ ] 4.3 Substituir SVGs inline do logo e ícones pelos arquivos de imagem quando `frontend/assets/` for populado
- [ ] 4.4 Implementar menu hambúrguer para mobile (drawer ou bottom nav)
- [ ] 4.5 Implementar navegação real entre páginas (projetos.html, alertas.html, analises.html)
