# vue-settings-notifications-pages Specification

## Purpose
TBD - created by archiving change vue-detalhe-config-notificacoes. Update Purpose after archive.
## Requirements
### Requirement: Páginas de Configurações e Notificações acessíveis pela navbar
O sistema SHALL expor as rotas `/configuracoes` e `/notificacoes`, acessíveis por ícones de ação na `Navbar`, renderizando `ConfiguracoesView.vue` e `NotificacoesView.vue` respectivamente.

#### Scenario: Acesso via ícone da navbar
- **WHEN** o usuário clica no ícone de Configurações (ou Notificações) na navbar
- **THEN** a URL muda para `/configuracoes` (ou `/notificacoes`) e a view correspondente é renderizada, sem reload completo da página

### Requirement: Conteúdo placeholder sem funcionalidade simulada
`ConfiguracoesView.vue` e `NotificacoesView.vue` SHALL exibir um estado "em construção" claro para o usuário, reaproveitando o design system atual (`.empty-state`/cards institucionais), e NÃO SHALL simular preferências de conta, alertas ou notificações que não existem de fato no backend.

#### Scenario: Usuário acessa Configurações
- **WHEN** o usuário navega para `/configuracoes`
- **THEN** a página exibe um título "Configurações" e uma mensagem informando que a funcionalidade está em construção, sem formulários ou opções que não têm efeito real

#### Scenario: Usuário acessa Notificações
- **WHEN** o usuário navega para `/notificacoes`
- **THEN** a página exibe um título "Notificações" e uma mensagem informando que a funcionalidade está em construção, sem lista de notificações fictícias

