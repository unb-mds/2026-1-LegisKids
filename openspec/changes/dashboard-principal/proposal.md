## Why

O LegisKids precisa de uma tela principal que sirva de porta de entrada para todos os usuários da plataforma. Sem um dashboard funcional, o sistema não tem ponto de início navegável: os dados legislativos coletados pelo backend ficam inacessíveis e o protótipo do Figma não se materializa em código.

A ausência de uma change formal para esse componente tornaria difícil rastrear evoluções futuras (integração com backend real, novos widgets, acessibilidade) e alinhar o time sobre o que está feito e o que ainda falta.

## What Changes

- Implementar `frontend/pages/index.html` seguindo fielmente o visual spec em `specs/dashboard/spec.json`, incluindo todos os componentes da tela: navbar, stats cards, alert banner, search bar, biblioteca legislativa, projetos recentes, ações rápidas e footer.
- Escrever `frontend/css/style.css` com todos os tokens de design do spec como variáveis CSS, responsividade em três breakpoints (mobile, tablet, desktop) e animações de hover definidas no spec.
- Escrever `frontend/js/script.js` com mock data e interatividade básica (filtro de busca em tempo real, clique nas categorias da biblioteca, navegação futura preparada).
- Preparar a estrutura para substituição posterior do mock por chamadas reais ao backend via Fetch API, sem alterar a estrutura do HTML.

## Capabilities

### New Capabilities
- `dashboard-principal`: Tela principal do LegisKids com visualização de métricas legislativas, busca, filtros por categoria e ações rápidas, operando inicialmente com dados mock.

### Modified Capabilities
- `frontend/css/style.css`: reescrito com sistema de design tokens baseado no spec.json, substituindo o CSS mínimo anterior.

## Impact

- Arquivos afetados: `frontend/pages/index.html`, `frontend/css/style.css`, `frontend/js/script.js`.
- Nenhuma dependência de backend ou banco de dados — todo dado é mock nesta fase.
- A estrutura do HTML e as classes CSS são projetadas para facilitar a futura integração com a API Flask (Release 1 do backlog).
- Sem novas dependências de build; fonte Inter carregada via Google Fonts CDN.
