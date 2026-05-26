## Why

O LegisKids precisa de uma tela de resultados de pesquisa que dê continuidade à busca iniciada no dashboard principal. Sem ela, o campo de busca do `index.html` não tem destino navegável: o usuário digita uma query e não chega a lugar nenhum.

A tela de pesquisa é o ponto central da US08 (busca por palavra-chave) e US09 (filtros combinados) do Release 1, e sua ausência de uma change formal dificulta rastrear a evolução futura do componente (integração com backend, modal de filtros, paginação real, histórico de buscas).

## What Changes

- Implementar `frontend/pages/pesquisa.html` seguindo fielmente o visual spec em `specs/spec.json`, incluindo todos os componentes da tela: navbar, botão voltar, cabeçalho, search bar, search summary card, toolbar (filtros + ordenação), lista de resultados, paginação e footer.
- Escrever `frontend/css/pesquisa.css` com os estilos específicos desta página — back button, search summary, toolbar, result cards e pagination — aproveitando os tokens CSS já definidos em `style.css` via herança de variáveis.
- Escrever `frontend/js/pesquisa.js` com mock data (`MOCK_RESULTS`) e interatividade completa: filtro em tempo real, ordenação, paginação cliente-side, leitura de query via `URLSearchParams` e empty state.
- Preparar a estrutura para substituição posterior do mock por chamadas reais ao backend via Fetch API, sem alterar a estrutura do HTML.

## Capabilities

### New Capabilities

- `dashboard-pesquisa`: Tela de resultados de busca do LegisKids, com filtro em tempo real, ordenação multi-critério, paginação e empty state, operando inicialmente com dados mock.
- `frontend/css/pesquisa.css`: folha de estilo isolada para os componentes específicos desta página.
- `frontend/js/pesquisa.js`: módulo de dados e interatividade da tela de pesquisa.

### Modified Capabilities

- `frontend/pages/pesquisa.html`: substituído o scaffold vazio pelo HTML completo seguindo o spec.

## Impact

- Arquivos afetados: `frontend/pages/pesquisa.html`, `frontend/css/pesquisa.css`, `frontend/js/pesquisa.js`.
- Nenhuma dependência de backend ou banco de dados — todo dado é mock nesta fase.
- A estrutura do HTML e as classes CSS são projetadas para facilitar a futura integração com a API Flask (Release 1 — US08, US09, US10).
- Sem novas dependências de build; herda a fonte Inter já carregada via Google Fonts CDN em `style.css`.
