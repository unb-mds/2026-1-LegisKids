## Context

Nenhum dos três componentes de gráfico (`GraficoSubtemas`, `GraficoStatus`, `GraficoTemporal`) define altura fixa no `.grafico-wrapper` nem `maintainAspectRatio` explícito nas opções do Chart.js. Com `responsive: true` e o default `maintainAspectRatio: true` (razão ~2:1), o canvas pode crescer de forma inconsistente dentro de containers flex/grid sem altura definida, deixando uma área vazia/desproporcional ao redor do gráfico real — é essa a "caixa desproporcional" reportada.

O logo real (`logo-legiskids.png`) tem fundo cinza/gradiente opaco (decisão anterior: usar mesmo assim). Sem tratamento, o texto "LegisKids" fica com baixo contraste sobre o azul `--primary` da navbar.

## Goals / Non-Goals

**Goals:**
- Gráficos com altura previsível, sem caixa vazia desproporcional, mantendo os dados/cores reais já implementados.
- `GraficoSubtemas` volta a vertical; `GraficoTemporal` recupera a largura total.
- Logo legível: pequeno retângulo branco atrás do PNG, sem alterar o asset em si.
- Subtítulo da navbar com contraste e tamanho adequados.
- "Projetos relacionados" com card mais compacto, mantendo clique para o detalhe interno da proposição sugerida (comportamento já existente do `ProposicaoCard`, preservado na versão compacta).
- Página Sobre com conteúdo mais rico e visualmente mais interessante, sem inventar funcionalidades que não existem.

**Non-Goals:**
- Não alterar o asset do logo (permanece o PNG com fundo cinza, decisão já tomada).
- Não mudar a fonte tipográfica global do projeto (Inter) — "fonte mais legível" do subtítulo é resolvido com tamanho/peso/contraste, não troca de font-family.
- Não adicionar novos dados/endpoints de backend para a página Sobre ou para os gráficos.

## Decisions

- **Altura fixa + `maintainAspectRatio: false`**: cada `.grafico-wrapper` ganha `height: 260px` (valor único reaproveitado nos 3 componentes, consistente com o tamanho dos cards do dashboard), e cada `new Chart(...)` passa `maintainAspectRatio: false` nas `options`. Isso faz o canvas preencher exatamente a altura do wrapper, sem sobra.
- **GraficoSubtemas volta a vertical**: remove `indexAxis: 'y'`, mantém `backgroundColor`/`borderColor` por barra usando a cor real da categoria (já implementado, não é revertido).
- **Grid do dashboard**: `Evolução Temporal` recebe de volta `grafico-card--wide` (ocupa a linha inteira); `Proposições por Subtema` e `Distribuição por Status` ficam lado a lado na primeira linha — layout idêntico ao que existia antes da rodada anterior, só que com o gráfico de subtema colorido por categoria (mudança já feita e mantida).
- **Logo sobre retângulo branco**: `.logo-icon` (a tag `<img>`) passa a ficar dentro de um `<div class="logo-badge">` com `background: #fff`, `border-radius`, e `padding` pequeno, dimensionado só o suficiente para a imagem (não um card grande) — o efeito visual é de um "selo" branco atrás do logo, como pedido.
- **Subtítulo "Monitoramento Legislativo"**: sobe de `font-size: 11px`/`font-weight: 400`/`opacity 0.7` para `font-size: 13px`/`font-weight: 600`/`color: rgba(255,255,255,0.92)` — ainda hierarquicamente abaixo do logo, mas legível.
- **Card compacto de relacionados**: novo bloco de markup inline em `DetalheView.vue` (não um componente novo — é específico dessa seção), mostrando só código (badge) + título (1-2 linhas, truncado) + status, sem os meta-items de partido/data que o `ProposicaoCard` completo tem — reduz a altura consideravelmente. Mantém `@click` navegando para `/proposicao/:id` da proposição sugerida, igual ao `ProposicaoCard` original. Alternativa descartada: criar um novo componente reutilizável `ProposicaoCardCompact.vue` — desnecessário, já que esse layout compacto só é usado nessa seção por ora; extrair como componente fica para se houver um segundo uso futuro.
- **Sobre mais interessante**: mantém as informações factuais já corretas (fonte de dados, contexto acadêmico), mas reorganiza em uma seção de "hero" com título/subtítulo maiores, adiciona uma seção "Como funciona" (coleta → classificação por tema → disponibilização) e usa ícones/cards com leve identidade visual (cores institucionais) em vez de blocos de texto puro — sem inventar números ou funcionalidades que o produto não tem.

## Risks / Trade-offs

- [Risco] Altura fixa de 260px pode cortar/apertar gráficos com muitas categorias (ex: muitos subtemas) → Mitigação: Chart.js com `maintainAspectRatio:false` ainda ajusta a largura das barras dentro da altura disponível; se o número de subtemas crescer muito, um scroll ou paginação do gráfico fica como melhoria futura, fora de escopo agora.
- [Risco] Card compacto de relacionados sem meta-informação (partido/data) pode parecer "menos informativo" → Mitigação: código + status + título já dão contexto suficiente para decidir se vale clicar; é uma lista de sugestões, não a visão principal.

## Migration Plan

1. Gráficos: altura fixa + `maintainAspectRatio:false` nos 3 componentes; `GraficoSubtemas` volta a vertical.
2. `DashboardView.vue`: reordenar grid (`Evolução Temporal` volta a `--wide`).
3. `Navbar.vue`: `logo-badge` branco atrás do `<img>`; subtítulo mais legível.
4. `DetalheView.vue`: card compacto de relacionados.
5. `SobreView.vue`: conteúdo e visual reformulados.
6. Validar com `npm run build`.

Rollback: reverter os arquivos alterados via git; nenhuma mudança de backend/dado envolvida.

## Open Questions

Nenhuma.
