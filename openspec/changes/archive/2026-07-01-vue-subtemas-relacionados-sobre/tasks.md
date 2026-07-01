## 1. Utilitários compartilhados

- [x] 1.1 Criar helper `corBadge(hex)` (retorna `{ background, color }` a partir de um hex, com fallback para o roxo padrão quando `hex` é nulo/ausente) — local em `src/frontend/src/utils/` ou inline reaproveitado nos componentes que precisam
- [x] 1.2 Criar helper `linkFichaCamara(id)` retornando `https://www.camara.leg.br/proposicoesWeb/fichadetramitacao?idProposicao=${id}`

## 2. ProposicaoCard e BuscaView

- [x] 2.1 Em `ProposicaoCard.vue`, trocar prop `subtema: String` por `subtemas: Array` (itens `{nome, cor}`), renderizar um badge colorido por subtema usando `corBadge`
- [x] 2.2 Em `ProposicaoCard.vue`, remover a prop `autor` e o `meta-item` de autor
- [x] 2.3 Em `BuscaView.vue`, passar `:subtemas="p.categorias"` (ou equivalente) para `ProposicaoCard` em vez de `:subtema`, e remover a passagem `:autor="..."`

## 3. DetalheView — subtemas, link oficial, remoção de Autor

- [x] 3.1 No cabeçalho de `DetalheView.vue`, exibir todos os subtemas (`proposicao.categorias`) como badges coloridos via `corBadge`, no lugar do badge único de subtema atual
- [x] 3.2 Adicionar link para a ficha oficial da Câmara (`linkFichaCamara`) em destaque no cabeçalho/top bar
- [x] 3.3 Atualizar o card "Documentos e anexos" para incluir o link da ficha oficial como item real (sem estilo de PDF simulado, já que é um link externo, não um arquivo)
- [x] 3.4 Remover o `info-cell` "Autor" e o computed `autorLabel` do card "Informações do projeto"

## 4. Projetos relacionados reais

- [x] 4.1 Em `DetalheView.vue`, ao carregar a proposição, buscar relacionados via `fetchProposicoes({ subtema: <primeiro subtema> }, 1, 4)`, excluindo o `id` da proposição atual dos resultados, limitando a 3
- [x] 4.2 Se não houver subtema ou o resultado (pós-exclusão) tiver 0 itens, tentar `fetchProposicoes({ partido: <sigla_partido> }, 1, 4)` com a mesma exclusão
- [x] 4.3 Renderizar os relacionados encontrados como cards clicáveis (reaproveitando `ProposicaoCard` ou uma versão compacta) navegando para `/proposicao/:id`; manter `.empty-state` quando não houver nenhum

## 5. Gráfico "Proposições por Subtema"

- [x] 5.1 Em `DashboardView.vue`, chamar `fetchTemas()` em paralelo a `fetchEstatisticas()`, montar mapa `nome → cor`
- [x] 5.2 Passar array `cores` (alinhado aos `labels` do gráfico) para `GraficoSubtemas.vue`, com fallback ao azul atual quando a categoria não tiver cor
- [x] 5.3 Em `GraficoSubtemas.vue`, mudar para barra horizontal (`indexAxis: 'y'`) e usar `backgroundColor` por barra a partir da prop `cores`

## 6. Logo real

- [x] 6.1 Copiar `docs/assets/images/logo-legiskids.png` para `src/frontend/src/assets/images/logo-legiskids.png`
- [x] 6.2 Em `Navbar.vue`, trocar o SVG inline do `.logo-icon` por `<img>` referenciando o asset importado, com `alt` descritivo

## 7. Página Sobre

- [x] 7.1 Criar `src/frontend/src/views/SobreView.vue` com conteúdo institucional real (missão do LegisKids, fonte de dados — API de Dados Abertos da Câmara —, contexto do projeto acadêmico)
- [x] 7.2 Registrar rota `/sobre` em `router/index.js`
- [x] 7.3 Em `App.vue`, trocar o link "Sobre" do rodapé de `href="#"` para `RouterLink to="/sobre"`

## 8. Validação

- [x] 8.1 Rodar `npm run build` e garantir ausência de erros de template — build concluído sem erros (71 módulos), sem referências residuais a `autor`/`documentoUrl` no código
- [ ] 8.2 **PENDENTE — validação manual**: subtemas coloridos aparecem em card/busca/detalhe, link da ficha oficial abre a página real da Câmara, Autor não aparece em nenhuma tela, projetos relacionados mostram proposições reais, gráfico de subtema fica horizontal e colorido, logo real aparece na navbar (com a caixa cinza de fundo, aceita pelo usuário), `/sobre` acessível pelo rodapé
