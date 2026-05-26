## Why

O LegisKids precisa de uma tela de detalhes para que o usuário possa aprofundar a leitura de um Projeto de Lei após encontrá-lo no dashboard principal ou nos resultados de busca. Sem ela, os botões "Ver Detalhes" do `index.html` e os cards de `pesquisa.html` não têm destino — o fluxo de leitura legislativa fica interrompido.

A tela é o entregável central da **US15 (tela de detalhes)** do Release 1 e materializa o protótipo Figma já especificado em `openspec/changes/dashboard-projeto-detalhado/spec.json`. Sem uma change formal, perderíamos a rastreabilidade da paleta navy específica desta página, da timeline de tramitação, das barras de indicadores e das interações de compartilhamento.

## What Changes

- Implementar `frontend/pages/detalhe-projeto.html` seguindo `specs/spec.json` e `specs/SPEC-detalhe.md`: top bar com voltar/compartilhar/salvar, cabeçalho do projeto (badges + título + meta), 5 abas (Visão geral, Tramitação, Análise, Documentos, Comentários), coluna principal (Sobre, Informações pessoais, Objetivos, Documentos, Projetos relacionados) e sidebar (Status da tramitação com timeline, Análise e indicadores, Compartilhar).
- Escrever `frontend/css/detalhe.css` com tokens locais `--d-*` escopados em `.detalhe-page` (paleta navy `#2B3FBF`, fundo `#DDE3EE`) sem alterar `style.css`, e estilizar todos os componentes BEM novos.
- Escrever `frontend/js/detalhe.js` com `MOCK_PROJETO`, troca de tabs (com acessibilidade por teclado), expand/recolher do card "Sobre o projeto", botões de compartilhamento (copiar link, WhatsApp, Twitter, Facebook) e toggle visual do botão "Salvar".
- Atualizar `index.html` e `pesquisa.html` para que os botões "Ver Detalhes" / cards de resultado naveguem para `detalhe-projeto.html?id=<id>`.

## Capabilities

### New Capabilities

- `dashboard-projeto-detalhado`: Tela de detalhes de um Projeto de Lei do LegisKids, com tabs, timeline de tramitação, indicadores visuais, lista de documentos e compartilhamento social, operando inicialmente com dados mock.
- `frontend/css/detalhe.css`: folha de estilo isolada com paleta navy escopada em `.detalhe-page`.
- `frontend/js/detalhe.js`: módulo de dados mock e interatividade (tabs, expand, share).

### Modified Capabilities

- `frontend/pages/index.html`: botão "Ver Detalhes" dos cards de Projetos Recentes passa a navegar para a nova página.
- `frontend/pages/pesquisa.html`: cards de resultado passam a linkar para `detalhe-projeto.html?id=<id>`.

## Impact

- Arquivos afetados: `frontend/pages/detalhe-projeto.html` (novo), `frontend/css/detalhe.css` (novo), `frontend/js/detalhe.js` (novo), `frontend/pages/index.html` (edit), `frontend/pages/pesquisa.html` (edit).
- Nenhuma dependência de backend ou banco nesta fase — todo dado é mock.
- A estrutura do HTML e o `MOCK_PROJETO` são projetados para que a futura integração com `/api/proposicoes/<id>` substitua apenas o bloco de dados sem alterar a marcação.
- Sem novas dependências de build; herda fontes Inter, IBM Plex Mono e Cinzel já carregadas via Google Fonts.
- Reuso integral de navbar e footer de `style.css` — zero duplicação dessas regras em `detalhe.css`.
