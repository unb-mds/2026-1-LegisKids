## MODIFIED Requirements

### Requirement: Componente ProposicaoCard
O sistema SHALL possuir `src/components/ProposicaoCard.vue` que recebe via props os campos `titulo`, `partido`, `data`, `status`, `subtemas` (array de `{nome, cor}`), `id`, `sigla_tipo`, `numero` e `ano`, e os renderiza como card clicável que navega para `/proposicao/:id`. O card SHALL exibir o código legível da proposição no formato `sigla_tipo numero/ano` (ex.: "PL 1234/2023") em vez do `id` numérico interno. O card SHALL exibir todos os subtemas da proposição como badges coloridos com a cor real de cada categoria (fallback para a cor roxa padrão quando a categoria não tiver `cor` cadastrada). O card NÃO SHALL exibir autor.

#### Scenario: Card renderizado com dados completos
- **WHEN** o componente recebe todos os campos da proposição, incluindo múltiplos subtemas
- **THEN** exibe o código no formato `sigla_tipo numero/ano`, título, partido, data formatada, badge de status e um badge colorido para cada subtema

#### Scenario: Campo ausente tratado com fallback
- **WHEN** o campo `partido` não está presente nos dados
- **THEN** o card não quebra a renderização e omite o meta-item de partido

#### Scenario: Clique no card navega para detalhes
- **WHEN** o usuário clica no card
- **THEN** o Vue Router navega para `/proposicao/:id` sem reload da página

#### Scenario: Subtema sem cor cadastrada
- **WHEN** um subtema da proposição não tem `cor` definida no backend
- **THEN** o badge desse subtema usa a cor roxa padrão já usada como fallback visual

### Requirement: Componente Navbar responsivo
O sistema SHALL possuir `src/components/Navbar.vue` com o logo real do projeto (`src/frontend/src/assets/images/logo-legiskids.png`), links de navegação, ícones de ação para Configurações e Notificações (navegando para `/configuracoes` e `/notificacoes`), e comportamento responsivo (menu hambúrguer em telas menores que 768px) conforme design no Figma (US17).

#### Scenario: Logo real exibido
- **WHEN** a Navbar é renderizada em qualquer página
- **THEN** exibe o logo real do LegisKids (imagem PNG), não mais o ícone SVG genérico

#### Scenario: Links de navegação ativos
- **WHEN** o usuário está na rota `/busca`
- **THEN** o link "Busca" na Navbar tem classe ativa via `RouterLink` com `active-class`

#### Scenario: Menu responsivo em mobile
- **WHEN** a largura da tela é menor que 768px
- **THEN** os links de navegação ficam ocultos e um ícone de menu hambúrguer é exibido; ao clicar, o menu expande

#### Scenario: Navegação por teclado na Navbar
- **WHEN** o usuário navega pela Navbar usando Tab e Enter
- **THEN** todos os links são acessíveis e ativáveis via teclado (conformidade WCAG AA — US17)

#### Scenario: Ícones de ação para Configurações e Notificações
- **WHEN** o usuário clica no ícone de Configurações (ou Notificações) na Navbar
- **THEN** o Vue Router navega para `/configuracoes` (ou `/notificacoes`) sem reload da página, e o ícone possui `aria-label` descritivo
