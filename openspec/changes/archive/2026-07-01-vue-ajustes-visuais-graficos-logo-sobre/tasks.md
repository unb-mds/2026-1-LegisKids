## 1. Gráficos — altura fixa e sem caixa desproporcional

- [x] 1.1 Em `GraficoSubtemas.vue`, `GraficoTemporal.vue` e `GraficoStatus.vue`, definir `height: 260px` no `.grafico-wrapper` (mesmo valor nos três, para consistência visual)
- [x] 1.2 Em cada `new Chart(...)`, adicionar `maintainAspectRatio: false` nas `options`
- [x] 1.3 Em `GraficoSubtemas.vue`, remover `indexAxis: 'y'` (volta a vertical), mantendo `backgroundColor`/`borderColor` por barra a partir da prop `cores`

## 2. Layout do grid de gráficos

- [x] 2.1 Em `DashboardView.vue`, mover `grafico-card--wide` de "Proposições por Subtema" de volta para "Evolução Temporal"
- [x] 2.2 Confirmar visualmente (via build) que "Proposições por Subtema" e "Distribuição por Status" ficam lado a lado na primeira linha, e "Evolução Temporal" ocupa a linha inteira abaixo

## 3. Logo e subtítulo da Navbar

- [x] 3.1 Em `Navbar.vue`, envolver o `<img class="logo-icon">` em um `<div class="logo-badge">` com fundo branco, `border-radius` e padding pequeno, dimensionado à imagem
- [x] 3.2 Ajustar `.logo-subtitle` para `font-size: 13px`, `font-weight: 600`, `color: rgba(255,255,255,0.92)` (ou equivalente com contraste suficiente)

## 4. Card compacto de Projetos relacionados

- [x] 4.1 Em `DetalheView.vue`, substituir o uso de `ProposicaoCard` completo em "Projetos relacionados" por um bloco de card compacto inline (badge de código, título truncado em 1-2 linhas, `StatusBadge`), sem meta-items de partido/data
- [x] 4.2 Manter clique navegando para `/proposicao/:id` da proposição sugerida (`router.push`), usando elemento `<button>` nativo (foco/teclado/Enter já suportados pelo browser, sem precisar de role/tabindex manuais como no `ProposicaoCard`)

## 5. Página Sobre mais interessante

- [x] 5.1 Reescrever `SobreView.vue`: seção de destaque (hero) com título/subtítulo maiores, seção "Como funciona" (coleta → classificação por tema → disponibilização), mantendo as informações factuais já corretas (fonte de dados, contexto acadêmico)
- [x] 5.2 Aplicar tratamento visual com cores institucionais/ícones nas seções, evitando bloco de texto puro repetitivo

## 6. Validação

- [x] 6.1 Rodar `npm run build` e garantir ausência de erros de template — build concluído sem erros (71 módulos)
- [ ] 6.2 **PENDENTE — validação manual**: gráficos sem caixa vazia, subtema vertical colorido, temporal com largura total, logo legível sobre o retângulo branco, subtítulo legível, relacionados compactos e clicáveis, Sobre com visual mais rico
