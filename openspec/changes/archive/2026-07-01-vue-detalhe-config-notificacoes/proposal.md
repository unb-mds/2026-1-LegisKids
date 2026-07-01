## Why

A migração do frontend para Vue (change `2026-06-27-migracao-frontend-vuejs`) recriou as telas de dashboard e busca, mas a tela de detalhe da proposição (`DetalheView.vue`) ficou bem mais simples que o protótipo visual já especificado em `openspec/changes/dashboard-projeto-detalhado/spec.json` (top bar de ações, abas, timeline de tramitação, indicadores, documentos, projetos relacionados). O dashboard principal (`DashboardView.vue`) também não reflete elementos do spec visual original (`dashboard-principal/specs/dashboard/spec.json`) como banner de alerta, busca rápida e ações rápidas. Além disso, a navbar nunca ganhou os ícones de "Configurações" e "Notificações" previstos no mesmo spec, e essas duas páginas nunca chegaram a existir.

## What Changes

- Reconstruir `DetalheView.vue` para seguir visualmente `dashboard-projeto-detalhado/spec.json` (paleta navy, top bar com Voltar/Compartilhar/Salvar, cabeçalho com badges, abas Visão geral/Tramitação/Análise/Documentos/Comentários, cards de conteúdo e sidebar com timeline de tramitação, indicadores e compartilhamento), usando dados reais da API onde já existem (autor, partido, ementa, tramitações) e estado vazio explícito (não dado fictício) onde a API ainda não fornece a informação (objetivos, documentos, indicadores, projetos relacionados, comentários).
- Adicionar a `DashboardView.vue` os elementos do spec visual ainda ausentes — banner de alerta, busca rápida e ações rápidas — **sem remover** os cards de estatística reais nem os 3 gráficos Chart.js já integrados ao backend, e **sem incluir** a seção "Biblioteca Legislativa" do spec original (removida por decisão explícita).
- Adicionar à `Navbar.vue` os ícones de ação "Configurações" e "Notificações" do spec, com rotas novas `/configuracoes` e `/notificacoes`.
- Criar `ConfiguracoesView.vue` e `NotificacoesView.vue` como páginas placeholder ("em construção"), reaproveitando o design system atual (`main.css`), sem inventar funcionalidade de backend inexistente (preferências de conta, alertas reais) — isso fica para uma change futura quando houver requisitos definidos.

## Capabilities

### New Capabilities
- `vue-detalhe-visual-parity`: cobre a reconstrução visual de `DetalheView.vue` seguindo o spec `dashboard-projeto-detalhado`, incluindo o tratamento de estado vazio para seções sem dado real da API.
- `vue-settings-notifications-pages`: cobre as novas páginas placeholder de Configurações e Notificações e seus ícones/rotas de acesso pela navbar.

### Modified Capabilities
- `vue-router-pages`: adiciona as rotas `/configuracoes` e `/notificacoes`, e amplia a descrição da rota `/proposicao/:id` para cobrir o layout de abas/sidebar do novo `DetalheView`.
- `vue-components-ui`: `Navbar.vue` passa a incluir os ícones de ação "Configurações" e "Notificações" além dos links de navegação existentes.

## Impact

- Arquivos afetados: `src/frontend/src/views/DetalheView.vue`, `src/frontend/src/views/DashboardView.vue`, `src/frontend/src/components/Navbar.vue`, `src/frontend/src/router/index.js`
- Arquivos novos: `src/frontend/src/views/ConfiguracoesView.vue`, `src/frontend/src/views/NotificacoesView.vue`
- Nenhuma mudança de backend/API — todas as seções sem endpoint hoje (objetivos, documentos, indicadores, projetos relacionados, notificações, configurações de conta) usam estado vazio explícito, não dado inventado
- Reuso dos tokens de cor/tipografia já definidos em `src/frontend/src/assets/main.css`; a paleta navy específica do spec de detalhe (`#2B3FBF`, fundo `#DDE3EE`) é aplicada como override escopado ao componente, sem alterar os tokens globais usados pelas demais páginas
