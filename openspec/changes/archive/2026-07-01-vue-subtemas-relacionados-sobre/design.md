## Context

A API já retorna mais dado do que o frontend usa hoje: `categorias` (array completo com `nome` e `cor` hex) em `/api/proposicoes` e `/api/proposicoes/<id>`; `id` da proposição, que é o próprio ID oficial da API da Câmara (usável para montar a URL pública da ficha de tramitação); e os filtros `subtema`/`partido` já suportados em `/api/proposicoes`, nunca usados para popular "Projetos relacionados". Por outro lado, `nome_autor` é sempre `null` — não há coleta de autor no ETL (confirmado em investigação anterior desta sessão) — e não há previsão de curto prazo para isso mudar, então exibi-lo no frontend hoje é sempre um "Não informado" sem função real.

O logo real do projeto é `docs/assets/images/logo-legiskids.png` (2MB, 1536×1024) — não existe versão SVG em nenhum lugar do repositório ou do histórico do git. Decisão do usuário: usar esse PNG mesmo assim.

## Goals / Non-Goals

**Goals:**
- Badges de subtema (plural, com cor real por categoria) visíveis em `ProposicaoCard`, `BuscaView` e `DetalheView`.
- Link funcional para a ficha real da proposição no site da Câmara, construído só com o `id` já disponível — sem exigir mudança de backend.
- "Autor" removido de toda superfície visível do frontend.
- "Projetos relacionados" com dado real (mesma API já usada pela busca), com fallback subtema → partido.
- Gráfico "Proposições por Subtema" horizontal, com cor real por categoria.
- Logo real na navbar.
- Página "Sobre" com conteúdo institucional real, link do rodapé funcional.

**Non-Goals:**
- Não alterar o backend/ETL para coletar autor — fora de escopo (exigiria 2 chamadas extras por proposição à API da Câmara, já investigado e registrado anteriormente como pendência separada).
- Não otimizar/comprimir o PNG do logo — troca de asset é só a etapa atual; otimização de imagem fica para uma mudança futura se necessário.
- Não criar endpoint de "proposições relacionadas" no backend — o filtro combinado (excluir proposição atual, priorizar subtema, fallback partido) é feito no frontend reaproveitando `/api/proposicoes`.

## Decisions

- **Cor de badge a partir de hex único**: cada categoria tem só uma cor (`cor`, ex: `#7C3AED`). Para manter o padrão visual dos badges existentes (fundo claro + texto colorido), a função utilitária `corBadge(hex)` gera `background: hex + '1A'` (hex com alpha ~10% via canal alpha de 2 dígitos) e `color: hex`. Se `cor` for nulo/ausente, usa o par `--purple-bg`/`--purple-text` já existente como fallback — mesmo visual de hoje.
- **Link da ficha oficial construído no frontend**: `https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=${proposicao.id}` — função utilitária simples, sem chamada de API adicional. Exibido em dois lugares: (1) como ação de destaque no cabeçalho do `DetalheView` (ao lado dos badges/título), e (2) dentro do card "Documentos e anexos" (que deixa de simular ícone de PDF/tamanho de arquivo — já que não é mais um "documento" simulado, é um link externo real).
- **Remoção de Autor**: remove a prop `autor` de `ProposicaoCard.vue` (e o `meta-item` correspondente), a passagem `:autor="..."` em `BuscaView.vue`, e o `info-cell` "Autor" + `autorLabel` em `DetalheView.vue`. Não mexe no filtro "Parlamentar" da `FilterBar` (campo de busca distinto, fora do pedido explícito do usuário) — mas registrado como observação de que também está com o mesmo problema de dado ausente, para decisão futura do usuário.
- **Projetos relacionados**: em `DetalheView.vue`, ao carregar a proposição, dispara uma segunda chamada `fetchProposicoes({ subtema: <primeiro subtema>, }, 1, 4)`; filtra fora o `id` da proposição atual e limita a 3 itens. Se não houver subtema OU o resultado (após excluir a atual) tiver menos de 1 item, tenta `fetchProposicoes({ partido: <sigla_partido> }, 1, 4)` com o mesmo filtro de exclusão. Se nenhum critério disponível ou nenhum resultado, mantém `.empty-state` (comportamento já implementado).
- **GraficoSubtemas horizontal + cor real**: `DashboardView.vue` passa a chamar `fetchTemas()` (já usado pela `FilterBar`) em paralelo a `fetchEstatisticas()`, monta um mapa `nome → cor`, e passa um array `cores` para `GraficoSubtemas`, alinhado por índice com `labels`. O componente usa `indexAxis: 'y'` (Chart.js) e `backgroundColor: cores` (com fallback ao azul atual para subtemas sem cor cadastrada). Alternativa descartada: manter vertical — rejeitada por nomes de subtema longos ficarem cortados/rotacionados.
- **Logo real**: `docs/assets/images/logo-legiskids.png` copiado para `src/frontend/src/assets/images/logo-legiskids.png` (fica dentro do pipeline de build do Vite, com hash/otimização automática de asset). `Navbar.vue` troca o SVG inline do `.logo-icon` por `<img>` referenciando o import do asset, mantendo `logo-text` (título/subtítulo) ao lado como já é hoje.
- **Página Sobre**: conteúdo estático institucional (missão do LegisKids, fonte de dados — API de Dados Abertos da Câmara dos Deputados —, contexto acadêmico do projeto), sem chamada de API. Rota `/sobre`, link do rodapé em `App.vue` passa de `href="#"` para `RouterLink to="/sobre"`.

## Risks / Trade-offs

- [Risco] PNG de 2MB pesa no carregamento da navbar (renderizada em toda página) → Mitigação: fora de escopo otimizar agora (decisão do usuário foi usar o asset como está); Vite ainda assim faz cache-busting via hash de build, então o custo de download só ocorre uma vez por sessão do navegador.
- [Risco] `fetchProposicoes` extra em `DetalheView` para relacionados adiciona uma chamada de rede a mais por página de detalhe → Mitigação: chamada é leve (`por_pagina=4`), roda em paralelo/depois do carregamento principal sem bloquear a renderização do resto da página.
- [Risco] Categorias sem `cor` cadastrada (campo é opcional no schema) quebrando visual do gráfico/badges → Mitigação: fallback já definido (roxo padrão para badges, azul padrão para o gráfico).

## Migration Plan

1. Utilitários de cor de badge e link da Câmara (funções puras, reaproveitadas em múltiplos componentes).
2. `ProposicaoCard.vue`, `BuscaView.vue`: subtemas plurais + remoção de Autor.
3. `DetalheView.vue`: subtemas plurais no cabeçalho, link da ficha oficial, remoção de Autor, projetos relacionados reais.
4. `GraficoSubtemas.vue` + `DashboardView.vue`: horizontal + cores reais.
5. Logo: copiar asset, atualizar `Navbar.vue`.
6. `SobreView.vue` + rota `/sobre` + link do rodapé em `App.vue`.
7. Validar com `npm run build`.

Rollback: reverter os arquivos alterados via git; nenhuma mudança de backend/banco envolvida.

## Open Questions

Nenhuma — decisões acima cobrem os pontos esclarecidos com o usuário (logo com PNG existente, gráfico horizontal com cor real, relacionados priorizando subtema com fallback para partido).
