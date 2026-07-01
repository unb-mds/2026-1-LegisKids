## ADDED Requirements

### Requirement: Rota de Configurações
O sistema SHALL registrar a rota `/configuracoes` mapeada para o componente `views/ConfiguracoesView.vue`, acessível via ícone de ação na Navbar.

#### Scenario: Acesso às configurações
- **WHEN** o usuário navega para `/configuracoes`
- **THEN** o componente `ConfiguracoesView` é renderizado

### Requirement: Rota de Notificações
O sistema SHALL registrar a rota `/notificacoes` mapeada para o componente `views/NotificacoesView.vue`, acessível via ícone de ação na Navbar.

#### Scenario: Acesso às notificações
- **WHEN** o usuário navega para `/notificacoes`
- **THEN** o componente `NotificacoesView` é renderizado

## MODIFIED Requirements

### Requirement: Rota de Detalhes da Proposição
O sistema SHALL registrar a rota `/proposicao/:id` mapeada para o componente `views/DetalheView.vue`, exibindo informações completas de uma proposição específica (US15) no layout de top bar, cabeçalho com badges, abas (Visão geral, Tramitação, Análise, Documentos, Comentários) e sidebar (status de tramitação, indicadores, compartilhamento) definido em `openspec/changes/dashboard-projeto-detalhado/spec.json`, com estado vazio explícito nas seções sem dado disponível na API.

#### Scenario: Acesso aos detalhes com ID válido
- **WHEN** o usuário navega para `/proposicao/123`
- **THEN** o componente `DetalheView` busca e exibe os dados da proposição com id 123 no layout de abas/sidebar do spec visual

#### Scenario: ID inválido ou não encontrado
- **WHEN** o usuário acessa `/proposicao/99999` e o backend retorna 404
- **THEN** o componente exibe mensagem de erro informativa sem quebrar a aplicação
