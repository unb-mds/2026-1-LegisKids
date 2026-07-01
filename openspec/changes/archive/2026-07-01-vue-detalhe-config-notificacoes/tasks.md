## 1. Rotas e navbar

- [x] 1.1 Em `src/frontend/src/router/index.js`, registrar as rotas `/configuracoes` → `ConfiguracoesView.vue` e `/notificacoes` → `NotificacoesView.vue` (lazy-loaded, como as demais rotas)
- [x] 1.2 Em `src/frontend/src/components/Navbar.vue`, adicionar 2 ícones de ação (engrenagem para Configurações, sino para Notificações) com `RouterLink` para as novas rotas e `aria-label` descritivo

## 2. Páginas placeholder

- [x] 2.1 Criar `src/frontend/src/views/ConfiguracoesView.vue`: título "Configurações" + card/estado "em construção", reaproveitando `.empty-state`/tokens de `main.css`
- [x] 2.2 Criar `src/frontend/src/views/NotificacoesView.vue`: título "Notificações" + card/estado "em construção", mesmo padrão visual

## 3. DetalheView — estrutura e paleta

- [x] 3.1 Em `DetalheView.vue`, adicionar bloco de tokens locais `--d-*` (paleta navy `#2B3FBF`, fundo `#DDE3EE`) escopado em `.detalhe-page`, sem alterar `main.css`
- [x] 3.2 Implementar top bar: link "Voltar" (reaproveita o existente), botão "Compartilhar" (Web Share API com fallback de clipboard) e botão "Salvar" (mensagem "em breve" ao clicar, sem quebrar a página)
- [x] 3.3 Implementar cabeçalho: badges (código da proposição, status via `StatusBadge`, subtema/tópico), título (ementa/título) e metadados (data de apresentação, situação)
- [x] 3.4 Implementar navegação por abas: Visão geral, Tramitação, Análise, Documentos, Comentários — troca de aba sem reload, acessível por teclado

## 4. DetalheView — conteúdo principal

- [x] 4.1 Card "Sobre o projeto": ementa real com expand/collapse ("Ver mais"/"Ver menos")
- [x] 4.2 Card "Informações pessoais": grid com autor, partido, data de apresentação, situação (campos sem dado real exibem "Não informado")
- [x] 4.3 Card "Objetivos do projeto": estado vazio (`.empty-state`) — sem dado real disponível
- [x] 4.4 Card "Documentos e anexos": lista com o link oficial existente (`url_documento`/`url`) quando presente, ou estado vazio
- [x] 4.5 Card "Projetos relacionados": estado vazio — sem endpoint de relacionados disponível

## 5. DetalheView — sidebar

- [x] 5.1 Card "Status da tramitação": timeline construída a partir de `tramitacoes` real (reaproveita dado já buscado por `fetchProposicao`), estado vazio se não houver tramitações
- [x] 5.2 Card "Análise e indicadores": estado vazio — sem dado real de relevância/impacto/apoio popular
- [x] 5.3 Card "Compartilhar": mesmos botões de compartilhamento social do spec (link, WhatsApp, Twitter/X, Facebook) usando a URL da proposição atual

## 6. DashboardView — elementos do spec sem Biblioteca Legislativa

- [x] 6.1 Adicionar banner de alerta institucional (estático, sem dado dinâmico de "prazo") com CTA de navegação
- [x] 6.2 Adicionar campo de busca rápida que navega para `/busca?q=<termo>` ao submeter
- [x] 6.3 Adicionar seção de ações rápidas (ex: "Análises e Relatórios" → `/busca` ou âncora para a seção de gráficos; "Configurar Alertas" → `/configuracoes`)
- [x] 6.4 Confirmar que nenhuma referência à seção "Biblioteca Legislativa" foi adicionada
- [x] 6.5 Confirmar que os cards de estatística reais e os 3 gráficos Chart.js existentes permanecem inalterados

## 7. Validação

- [x] 7.1 `npm run dev` iniciado e servidor respondeu HTTP 200 em `/`. **Validação parcial**: sem browser disponível neste ambiente para clicar manualmente em cada fluxo (ícones da navbar, troca de abas, compartilhar); recomenda-se validação visual manual antes do merge
- [x] 7.2 Rodar `npm run build` (ou lint equivalente) para garantir ausência de erros de template — build concluído sem erros (67 módulos, todos os chunks gerados incluindo `DetalheView`, `ConfiguracoesView`, `NotificacoesView`)
- [ ] 7.3 **PENDENTE — validação manual**: confirmar visualmente no navegador que `DashboardView.vue` mantém os gráficos Chart.js funcionando após as adições (build não falhou, mas renderização visual não foi inspecionada)
