## MODIFIED Requirements

### Requirement: Componente Navbar responsivo
O sistema SHALL possuir `src/components/Navbar.vue` com o logo real do projeto (`src/frontend/src/assets/images/logo-legiskids.png`) exibido sobre um pequeno retângulo branco para garantir legibilidade contra o fundo azul da navbar, subtítulo "Monitoramento Legislativo" com contraste e tamanho legíveis, links de navegação, ícones de ação para Configurações e Notificações (navegando para `/configuracoes` e `/notificacoes`), e comportamento responsivo (menu hambúrguer em telas menores que 768px) conforme design no Figma (US17).

#### Scenario: Logo legível sobre fundo branco
- **WHEN** a Navbar é renderizada em qualquer página
- **THEN** o logo (imagem PNG com fundo cinza) é exibido sobre um retângulo branco pequeno, garantindo contraste e legibilidade do texto do logo

#### Scenario: Subtítulo legível
- **WHEN** a Navbar é renderizada
- **THEN** o texto "Monitoramento Legislativo" é exibido com tamanho e contraste suficientes para leitura confortável sobre o fundo azul

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
