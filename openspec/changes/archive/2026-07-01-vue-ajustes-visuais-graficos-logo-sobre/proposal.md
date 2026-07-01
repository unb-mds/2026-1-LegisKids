## Why

A rodada anterior de mudanças visuais introduziu alguns problemas que o usuário identificou ao revisar: o gráfico de subtema horizontal ficou pior que o vertical original; o gráfico de evolução temporal perdeu a largura total (ficou espremido) quando a largura extra foi realocada para o gráfico de subtema; os três gráficos (Chart.js) renderizam com uma caixa/retângulo desproporcional atrás do conteúdo real, por falta de altura fixa e `maintainAspectRatio` explícito; o logo real (PNG com fundo cinza opaco) fica ilegível direto sobre o fundo azul da navbar; os cards de "Projetos relacionados" (reaproveitando `ProposicaoCard` inteiro) ficam altos demais para uma lista de sugestões; a página "Sobre" ficou genérica/pouco envolvente; e o subtítulo "Monitoramento Legislativo" da navbar está pequeno e com baixo contraste, difícil de ler.

## What Changes

- `GraficoSubtemas.vue`: volta para barras verticais (mantendo a cor real por subtema já implementada), com `maintainAspectRatio: false` e altura fixa no wrapper para eliminar a caixa desproporcional.
- `GraficoTemporal.vue` e `GraficoStatus.vue`: mesmo tratamento de altura fixa/`maintainAspectRatio: false`.
- `DashboardView.vue`: reorganiza o grid de gráficos — "Evolução Temporal" volta a ocupar a largura total (`grafico-card--wide`); "Proposições por Subtema" e "Distribuição por Status" dividem a linha de cima.
- `Navbar.vue`: logo passa a ficar sobre um pequeno retângulo branco arredondado, garantindo legibilidade do PNG (que tem fundo cinza) contra o azul da navbar.
- `Navbar.vue`: subtítulo "Monitoramento Legislativo" ganha tamanho, peso de fonte e contraste maiores para ficar legível.
- `DetalheView.vue`: "Projetos relacionados" passa a usar um card compacto próprio (mais baixo verticalmente que o `ProposicaoCard` padrão), clicável, navegando para o detalhe (`/proposicao/:id`) da proposição sugerida.
- `SobreView.vue`: conteúdo reescrito para ser mais envolvente — problema que o projeto resolve, como funciona na prática, e contexto acadêmico — com tratamento visual mais rico que os cards simples atuais.

## Capabilities

### Modified Capabilities
- `chart-visualizations`: `GraficoSubtemas` volta a ser vertical; os três componentes de gráfico passam a ter dimensionamento fixo (sem caixa desproporcional).
- `vue-components-ui`: `Navbar` com logo sobre fundo branco e subtítulo mais legível.

Nota: `vue-detalhe-visual-parity` (card compacto de "Projetos relacionados") não tem spec permanente ainda — a change que a introduziu (`vue-detalhe-config-notificacoes`) segue arquivada pendente por um problema de formatação de specs já registrado anteriormente. O ajuste do card compacto é feito como detalhe de implementação (documentado em design.md), sem delta formal contra uma base que ainda não existe.

## Impact

- Arquivos afetados: `src/frontend/src/components/charts/GraficoSubtemas.vue`, `GraficoTemporal.vue`, `GraficoStatus.vue`, `src/frontend/src/views/DashboardView.vue`, `src/frontend/src/components/Navbar.vue`, `src/frontend/src/views/DetalheView.vue`, `src/frontend/src/views/SobreView.vue`
- Nenhuma mudança de backend/API
- Sem novos componentes de rota; só ajustes visuais/estruturais nos já existentes
