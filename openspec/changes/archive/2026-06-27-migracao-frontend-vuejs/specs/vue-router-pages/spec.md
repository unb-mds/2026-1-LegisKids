## ADDED Requirements

### Requirement: Roteamento client-side com Vue Router 4
O sistema SHALL usar Vue Router 4 no modo `history` (HTML5 History API) para navegação entre páginas sem reload completo.

#### Scenario: Navegação sem reload
- **WHEN** o usuário clica em um link de navegação (ex: "Busca")
- **THEN** a URL muda para `/busca` e o conteúdo é atualizado sem recarregar a página inteiramente

#### Scenario: Rota inexistente
- **WHEN** o usuário acessa uma URL não mapeada (ex: `/rota-invalida`)
- **THEN** o sistema redireciona para `/` ou exibe componente 404

### Requirement: Rota de Dashboard Principal
O sistema SHALL registrar a rota `/` mapeada para o componente `views/DashboardView.vue`, exibindo estatísticas resumidas de proposições (US13).

#### Scenario: Acesso ao dashboard
- **WHEN** o usuário acessa `/`
- **THEN** o componente `DashboardView` é renderizado com cards de estatísticas e área reservada para gráficos

### Requirement: Rota de Busca e Filtros
O sistema SHALL registrar a rota `/busca` mapeada para o componente `views/BuscaView.vue`, permitindo busca por palavra-chave e filtros combinados (US08, US09, US10).

#### Scenario: Acesso à busca
- **WHEN** o usuário navega para `/busca`
- **THEN** o componente `BuscaView` é renderizado com campo de busca, painel de filtros e área de resultados

#### Scenario: Parâmetros de busca na URL
- **WHEN** o usuário aplica filtros e realiza uma busca
- **THEN** os parâmetros relevantes (palavra-chave, filtros ativos, página) são refletidos na URL como query params

### Requirement: Rota de Detalhes da Proposição
O sistema SHALL registrar a rota `/proposicao/:id` mapeada para o componente `views/DetalheView.vue`, exibindo informações completas de uma proposição específica (US15).

#### Scenario: Acesso aos detalhes com ID válido
- **WHEN** o usuário navega para `/proposicao/123`
- **THEN** o componente `DetalheView` busca e exibe os dados da proposição com id 123

#### Scenario: ID inválido ou não encontrado
- **WHEN** o usuário acessa `/proposicao/99999` e o backend retorna 404
- **THEN** o componente exibe mensagem de erro informativa sem quebrar a aplicação

### Requirement: Navbar persistente entre rotas
O sistema SHALL renderizar o componente `Navbar` em `App.vue`, fora do `<RouterView>`, para que seja exibido em todas as páginas sem ser remontado a cada navegação.

#### Scenario: Navbar visível em todas as páginas
- **WHEN** o usuário navega entre `/`, `/busca` e `/proposicao/:id`
- **THEN** a Navbar permanece visível e o link da página atual é marcado como ativo via `RouterLink`
