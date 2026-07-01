## Why

Vários pontos do frontend Vue regrediram ou nunca foram conectados a dados reais que a API já fornece: os subtemas (plural, com cor por categoria) não aparecem em lugar nenhum; não existe link para a ficha real do PL na Câmara mesmo o `id` da proposição sendo o ID oficial; o campo "Autor" é exibido em várias telas mas o backend nunca o preenche (é sempre `null`), então hoje ele só mostra "Não informado" — informação enganosa por omissão de contexto; a seção "Projetos relacionados" do detalhe está sempre vazia mesmo a API já suportando filtro por subtema/partido; o gráfico "Proposições por Subtema" é uma barra vertical monocromática que não aproveita as cores reais de categoria; e o logo da navbar é um ícone SVG genérico em vez do asset real do projeto; e a página "Sobre" do rodapé nunca teve conteúdo (link `href="#"`).

## What Changes

- Exibir todos os subtemas de uma proposição (não só o primeiro) como badges coloridos com a cor real de cada categoria (`categorias[].cor` da API), no mesmo estilo visual dos badges de status/código já existentes, em `ProposicaoCard.vue`, `BuscaView.vue` e `DetalheView.vue`.
- Adicionar link para a ficha real da proposição na Câmara dos Deputados (`https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=<id>`), construído a partir do `id` (que já é o ID oficial da API da Câmara) — sem depender de campo de backend que não existe.
- Remover toda exibição de "Autor" do frontend (`ProposicaoCard.vue`, `BuscaView.vue`, `DetalheView.vue`) — campo nunca populado pelo backend hoje.
- Implementar "Projetos relacionados" em `DetalheView.vue` com busca real via `fetchProposicoes` filtrando primeiro por subtema da proposição atual; se não houver subtema ou não houver resultados suficientes, tenta por partido; exclui a própria proposição da lista.
- Ajustar `GraficoSubtemas.vue` para barra horizontal com cor real por subtema (via `categorias[].cor`), substituindo a barra vertical azul única.
- Trocar o ícone SVG genérico da `Navbar.vue` pelo logo real do projeto (`docs/assets/images/logo-legiskids.png`, copiado para `src/frontend/src/assets/`).
- Criar página `/sobre` com conteúdo institucional real (missão do LegisKids, dados que usa, com quem é feito) e conectar o link "Sobre" do rodapé (`App.vue`) a ela.

## Capabilities

### Modified Capabilities
- `vue-components-ui`: `ProposicaoCard` passa a exibir múltiplos subtemas coloridos e deixa de exibir "Autor"; `Navbar` passa a usar o logo real em vez do ícone SVG.
- `vue-router-pages`: nova rota `/sobre`.
- `vue-detalhe-visual-parity`: card "Projetos relacionados" passa a usar dado real (não mais estado vazio); card "Documentos e anexos"/link oficial passa a incluir o link para a ficha real da Câmara; remoção de "Autor" do card de informações.

## Impact

- Arquivos afetados: `src/frontend/src/components/ProposicaoCard.vue`, `src/frontend/src/components/Navbar.vue`, `src/frontend/src/components/charts/GraficoSubtemas.vue`, `src/frontend/src/views/BuscaView.vue`, `src/frontend/src/views/DetalheView.vue`, `src/frontend/src/App.vue`, `src/frontend/src/router/index.js`
- Arquivo novo: `src/frontend/src/views/SobreView.vue`, `src/frontend/src/assets/images/logo-legiskids.png` (copiado)
- Nenhuma mudança de backend/API — todos os dados usados (`categorias[].cor`, `id`, filtros `subtema`/`partido` de `/api/proposicoes`) já existem hoje
- "Projetos relacionados" consome o mesmo endpoint `/api/proposicoes` já usado pela busca, sem endpoint novo
